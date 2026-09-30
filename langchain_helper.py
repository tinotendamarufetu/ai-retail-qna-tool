import os
import re
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from few_shots import few_shots


# 1. Load environment variables
load_dotenv()

# Load Groq API Key
# Read from st.secrets on Streamlit Cloud, fallback to .env locally
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# Initialize Database Connection
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "retail_store_db")

# Connection string for MS SQL Server (commented out)
#db_uri = f"mssql+pyodbc://@{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes"
#db = SQLDatabase.from_uri(db_uri)

# Connect to local SQLite database file inside repository
db_uri = "sqlite:///app.db"
db = SQLDatabase.from_uri(db_uri)


@st.cache_resource
def get_few_shot_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    to_vectorize = [
        " ".join([example["Question"], example["SQLQuery"]])
        for example in few_shots
    ]
    vectorstore = FAISS.from_texts(
        to_vectorize, embeddings, metadatas=few_shots
    )
    return vectorstore


def validate_sql_query(query: str) -> bool:
    """Security Guardrail: Blocks dangerous non-SELECT queries."""
    forbidden_keywords = [
        r"\bDROP\b",
        r"\bDELETE\b",
        r"\bUPDATE\b",
        r"\bINSERT\b",
        r"\bALTER\b",
        r"\bTRUNCATE\b",
    ]
    for keyword in forbidden_keywords:
        if re.search(keyword, query, re.IGNORECASE):
            return False
    return True


@st.cache_resource
def get_few_shot_db_chain():

    # Fetch key inside function scope
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

    if not GROQ_API_KEY:
        st.error("❌ GROQ_API_KEY is missing from your .env file!")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",  # Valid active model from your list
        api_key=GROQ_API_KEY,
        temperature=0.2,
    )

    vectorstore = get_few_shot_vectorstore()

    # Define Example Prompt Format
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery"],
        template="\nUser Question: {Question}\nSQL Query: {SQLQuery}",
    )

    # Dynamic Few Shot Prompt Template
    prompt_template = FewShotPromptTemplate(
        example_prompt=example_prompt,
        examples=[],  # Handled dynamically by vector store lookup
        prefix="""You are a SQLite Server expert. Given an input question, create a syntactically correct SQLite query.

        Database Schema / Guidelines:
        - Table: sales
        - Columns: payment_method (varchar), transaction_id, sales_amount, etc.
        - Example: "UPI payment method" -> WHERE payment_method = 'UPI'
        - Always finish the entire SQL query string completely. Do not leave trailing operators like '=' or 'WHERE'.

        Return ONLY the plain SQL query text without any explanations.
        """,
        suffix="\nUser Question: {input}\nSQL Query:",
        input_variables=["input"],
    )

    return llm, vectorstore, prompt_template


def clean_sql_response(raw_response: str) -> str:
    """Extracts pure SQL text from LLM outputs, removing markdown and JSON wrappers."""
    text = raw_response.strip()

    # Handle JSON object or dictionary strings returned by the LLM
    if text.startswith("{") and "text" in text:
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict) and "text" in parsed:
                text = parsed["text"]
        except Exception:
            match = re.search(r"'text':\s*['\"]([^'\"]+)['\"]", text)
            if match:
                text = match.group(1)

    # Clean markdown code blocks
    text = text.replace("```sql", "").replace("```", "").strip()
    return text


def process_question(user_question: str):
    llm, vectorstore, prompt_template = get_few_shot_db_chain()

    # 1. Retrieve Relevant Few-Shot Examples via Vector Search
    similar_docs = vectorstore.similarity_search(user_question, k=2)
    retrieved_examples = [doc.metadata for doc in similar_docs]

    # 2. Formulate Dynamic System Prompt
    example_str = "\n".join(
        [
            f"Question: {ex['Question']}\nSQLQuery: {ex['SQLQuery']}"
            for ex in retrieved_examples
        ]
    )
    full_prompt = f"{prompt_template.prefix}\n{example_str}\n\nSchema Info:\n{db.get_table_info()}\n\nUser Question: {user_question}\nSQL Query:"

    # 3. Generate SQL from Groq LLM
    response = llm.invoke(full_prompt)

    # Handle list or Message response structures from LangChain
    if isinstance(response.content, list):
        raw_content = "".join(
            [str(getattr(item, "text", item)) for item in response.content]
        )
    else:
        raw_content = str(response.content)

    # Clean and extract pure SQL string
    generated_sql = clean_sql_response(raw_content)

    # Check for incomplete trailing syntax
    if generated_sql.strip().endswith("="):
        return (
            "Error: LLM generated an incomplete SQL query. Please try rephrasing your question.",
            generated_sql,
            None,
        )

    # 4. Security Guardrail Check
    if not validate_sql_query(generated_sql):
        return (
            "⚠️ Security Alert: Destructive SQL query generation blocked by execution guardrails.",
            generated_sql,
            None,
        )

    # 5. Execute Safe SQL Query
    try:
        query_result = db.run(generated_sql)
        return None, generated_sql, query_result
    except Exception as e:
        return f"Database Execution Error: {str(e)}", generated_sql, None