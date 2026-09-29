# 👕 T-Shirts Retail Store — Enterprise Database Q&A Tool

> **Natural Language → SQL → Enterprise Database → Verified Answer**

An enterprise-grade **Natural Language to SQL (NL2SQL)** application that allows users to query a retail database using plain English.

The system combines **Streamlit, LangChain, Groq LLMs, FAISS, Hugging Face Embeddings, SQLAlchemy, pyodbc, and Microsoft SQL Server** to transform natural-language questions into executable and validated **T-SQL queries**.

Users can ask questions about **inventory, sales, discounts, revenue, products, and transactions** without needing to manually write SQL.

---

## 📸 Application Preview

<img width="1832" height="795" alt="T-Shirts Retail Store Q&A Tool" src="https://github.com/user-attachments/assets/346249ef-5e19-49ea-9713-33242846b43a" />

---

## 🌟 Key Features

### 🗣️ Natural Language to SQL

Users can ask questions in plain English, such as:

> "Which brand has the highest total sales revenue?"

> "How many black T-shirts are currently in stock?"

> "What is the average price of Nike T-shirts?"

The application converts these questions into valid **Microsoft SQL Server T-SQL queries**.

---

### ⚡ Fast LLM Inference with Groq

The application uses the **Groq API** for low-latency LLM inference.

**Model:**

```text
openai/gpt-oss-120b
```

Groq provides fast inference, allowing generated SQL queries and responses to be returned quickly through the Streamlit interface.

---

### 🧠 Dynamic Few-Shot Learning

The system uses a retrieval-based few-shot prompting strategy.

Relevant SQL examples are stored in a **FAISS vector database** and retrieved dynamically based on the user's question.

The embedding model used is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This allows the application to provide the LLM with examples that are semantically similar to the current question.

### Retrieval Flow

```text
User Question
      │
      ▼
Hugging Face Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Relevant SQL Examples
      │
      ▼
Dynamic Prompt
      │
      ▼
Groq LLM
```

---

### 🛡️ SQL Security Guardrails

Generated SQL queries are validated before they are sent to the database.

The application blocks potentially destructive SQL operations including:

* `DROP`
* `DELETE`
* `UPDATE`
* `INSERT`
* `ALTER`
* `TRUNCATE`

This ensures that the NL2SQL system operates as a **read-only analytical interface**.

---

### 🧹 Robust SQL Cleaning & Validation

LLMs may return SQL inside Markdown code blocks or structured JSON.

The application includes preprocessing logic to:

* Remove Markdown code fences
* Extract SQL from structured responses
* Clean generated SQL
* Validate SQL before execution
* Reject forbidden SQL operations
* Handle database execution errors

This creates an additional validation layer between the LLM and the enterprise database.

---

### 📊 Interactive Streamlit Dashboard

The application provides an interactive user interface built with **Streamlit**.

Key interface capabilities include:

* Natural-language question input
* Sample question quick triggers
* Database schema exploration
* Generated SQL inspection
* Query results
* Session history
* Error messages and validation feedback

---

# 🏗️ System Architecture

The application follows a retrieval-augmented NL2SQL pipeline.

```text
                         ┌─────────────────────┐
                         │    User Question    │
                         │   Natural Language  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  FAISS Vector Store │
                         │                     │
                         │ Similarity Search   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ Dynamic Prompt Construction   │
                    │                               │
                    │ • Database Schema             │
                    │ • Few-Shot SQL Examples      │
                    │ • User Question               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Groq LLM       │
                         │                     │
                         │  SQL Generation     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   SQL Cleaning & Guardrails   │
                    │                               │
                    │ • Remove Markdown             │
                    │ • Extract SQL                 │
                    │ • Validate Query              │
                    │ • Block Destructive SQL       │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │      Microsoft SQL Server     │
                    │                               │
                    │       Read-Only Query         │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Streamlit UI      │
                         │                     │
                         │ • SQL Query         │
                         │ • Results            │
                         │ • Session History    │
                         └─────────────────────┘
```

---

# 🔄 End-to-End Query Workflow

When a user submits a question, the application follows this workflow:

### 1. User submits a natural-language question

Example:

```text
Which T-shirt brand generated the highest revenue?
```

### 2. Relevant examples are retrieved

The question is converted into an embedding using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

FAISS then searches for semantically similar SQL examples.

---

### 3. Dynamic prompt is constructed

The application combines:

```text
Database Schema
        +
Retrieved Few-Shot Examples
        +
User Question
```

into a structured prompt for the LLM.

---

### 4. Groq generates T-SQL

The LLM generates a SQL Server-compatible query.

Example:

```sql
SELECT
    t.brand,
    SUM(si.quantity * si.price) AS total_revenue
FROM sales_items si
JOIN t_shirts t
    ON si.t_shirt_id = t.t_shirt_id
GROUP BY t.brand
ORDER BY total_revenue DESC;
```

---

### 5. Generated SQL is cleaned

The application removes unnecessary formatting such as:

````text
```sql
...
````

````

and extracts the actual SQL statement.

---

### 6. Security validation is performed

The SQL query is inspected for forbidden operations.

If a destructive operation is detected, execution is immediately stopped.

---

### 7. Query executes against SQL Server

Validated queries are executed against:

```text
retail_store_db
````

using:

```text
SQLAlchemy
+
pyodbc
+
Microsoft SQL Server
```

---

### 8. Results are displayed

The resulting dataset is returned to the Streamlit interface where users can inspect the results and generated SQL.

---

# 🗄️ Database Schema

The application connects to a Microsoft SQL Server database named:

```text
retail_store_db
```

The database contains four primary tables.

## 1. `t_shirts`

Stores product and inventory information.

| Column           | Description                |
| ---------------- | -------------------------- |
| `t_shirt_id`     | Unique product identifier  |
| `brand`          | T-shirt brand              |
| `color`          | Product color              |
| `size`           | Product size               |
| `price`          | Product price              |
| `stock_quantity` | Current inventory quantity |

---

## 2. `discounts`

Stores discount information associated with individual T-shirts.

| Concept       | Description                               |
| ------------- | ----------------------------------------- |
| Product       | T-shirt associated with the discount      |
| Discount Rate | Percentage or rate applied to the product |

---

## 3. `sales`

Stores high-level transaction information.

| Concept        | Description                             |
| -------------- | --------------------------------------- |
| Transaction    | Unique sales transaction                |
| Date           | Transaction date                        |
| Total Amount   | Total transaction value                 |
| Payment Method | Method used to complete the transaction |

---

## 4. `sales_items`

Stores granular line-item information for individual transactions.

This table connects:

```text
Sales Transaction
        │
        ▼
Sales Items
        │
        ▼
T-Shirt Inventory
```

This structure allows analytical questions involving:

* Revenue
* Units sold
* Product performance
* Brand performance
* Inventory
* Transaction history
* Discounts

---

# 🧠 Technology Stack

| Technology                | Purpose                            |
| ------------------------- | ---------------------------------- |
| **Python**                | Core application language          |
| **Streamlit**             | Interactive web application        |
| **LangChain**             | LLM orchestration and prompting    |
| **Groq API**              | LLM inference                      |
| **GPT-OSS-120B**          | Natural-language-to-SQL generation |
| **FAISS**                 | Vector similarity search           |
| **Hugging Face**          | Text embeddings                    |
| **Sentence Transformers** | Embedding model                    |
| **SQLAlchemy**            | Database connectivity              |
| **pyodbc**                | SQL Server connectivity            |
| **Microsoft SQL Server**  | Enterprise relational database     |
| **python-dotenv**         | Environment configuration          |

---

# 🔐 Security & Guardrails

A major design goal of the application is to prevent the LLM from directly performing destructive database operations.

The application uses a SQL validation layer before database execution.

### Validation Logic

```python
def validate_sql_query(query: str) -> bool:
    forbidden_keywords = [
        r"\bDROP\b",
        r"\bDELETE\b",
        r"\bUPDATE\b",
        r"\bINSERT\b",
        r"\bALTER\b",
        r"\bTRUNCATE\b"
    ]

    for keyword in forbidden_keywords:
        if re.search(keyword, query, re.IGNORECASE):
            return False

    return True
```

The validator rejects queries containing potentially destructive **DDL** or **DML** operations.

### Blocked Operations

```text
DROP
DELETE
UPDATE
INSERT
ALTER
TRUNCATE
```

The intended operating mode is therefore:

```text
Natural Language
       │
       ▼
     LLM
       │
       ▼
Generated SQL
       │
       ▼
Security Validation
       │
       ├──── ❌ Forbidden → Block
       │
       └──── ✅ SELECT → Execute
```

> **Important:** The regex validator is an application-level safeguard, not a complete database security boundary. Production deployments should additionally use a dedicated read-only database user, least-privilege permissions, query timeouts, and other database-level controls.

---

# 🎯 Example Questions

The application can support questions such as:

### Inventory

```text
How many T-shirts are currently in stock?
```

```text
Which brand has the most inventory?
```

```text
How many black T-shirts are available?
```

### Product Analysis

```text
What is the average price of each brand?
```

```text
Which brand has the most expensive T-shirts?
```

```text
What sizes are available for each brand?
```

### Sales Analysis

```text
What was the total revenue last month?
```

```text
Which brand generated the most revenue?
```

```text
What is the average transaction value?
```

### Discount Analysis

```text
Which products currently have discounts?
```

```text
What is the average discount rate by brand?
```

---

# 🚀 Getting Started

## Prerequisites

Before running the application, make sure you have:

* Python **3.10+**
* Microsoft SQL Server
* ODBC Driver 18 for SQL Server
* A Groq API key
* Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-retail-qna-tool.git

cd ai-retail-qna-tool
```

> Replace `YOUR_USERNAME` with your GitHub username.

---

## 2. Create a Virtual Environment

### Windows — PowerShell

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuration

Create a `.env` file in the root directory of the project.

```env
GROQ_API_KEY=your_groq_api_key_here

# Database Configuration
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_NAME=retail_store_db
```

### Environment Variables

| Variable       | Description                  |
| -------------- | ---------------------------- |
| `GROQ_API_KEY` | Groq API authentication key  |
| `DB_USER`      | SQL Server database username |
| `DB_PASSWORD`  | SQL Server database password |
| `DB_HOST`      | SQL Server host              |
| `DB_NAME`      | Database name                |

### 🔒 Security Notice

Never commit your `.env` file to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application should open in your browser at:

```text
http://localhost:8501
```

---

# 📂 Project Structure

```text
ai-retail-qna-tool/
│
├── app.py
│   └── Main Streamlit UI and application pipeline
│
├── few_shots.py
│   └── Few-shot SQL examples used for retrieval
│
├── check_available_models.py
│   └── Utility for checking available Groq models
│
├── requirements.txt
│   └── Python dependencies
│
├── .env
│   └── Environment variables
│
├── .gitignore
│   └── Git tracking exclusions
│
└── README.md
    └── Project documentation
```

---

# 🧩 Core Architecture Components

## Streamlit

Provides the interactive frontend and allows users to interact with the NL2SQL system without writing SQL manually.

---

## LangChain

Used for:

* Prompt construction
* LLM orchestration
* Few-shot prompting
* Integration between application components

---

## Groq

Provides fast LLM inference for natural-language understanding and SQL generation.

---

## FAISS

Provides efficient similarity search over the few-shot SQL examples.

Instead of sending every example to the LLM, the system retrieves the most relevant examples for the current question.

---

## Hugging Face Embeddings

The application uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to convert questions and examples into numerical vector representations.

These vectors are then indexed in FAISS.

---

## Microsoft SQL Server

Acts as the enterprise relational database containing the retail data.

The generated SQL is executed against SQL Server after passing the application's validation layer.

---

# 📈 Why This Architecture?

Traditional database applications require users to understand SQL before they can retrieve information.

This project introduces a natural-language interface:

```text
Traditional Approach

User
 │
 ▼
Learn SQL
 │
 ▼
Write Query
 │
 ▼
Database
 │
 ▼
Results
```

The NL2SQL approach simplifies this:

```text
User
 │
 │ Natural Language
 ▼
AI / LLM
 │
 │ Generated SQL
 ▼
Security Layer
 │
 ▼
SQL Server
 │
 ▼
Results
```

This makes enterprise data more accessible to users who understand the business domain but may not know SQL.

---

# 🔄 Retrieval-Augmented Few-Shot Strategy

A key part of the application is the use of **retrieval-based few-shot learning**.

Instead of relying entirely on the LLM's ability to generate SQL from scratch, the system retrieves similar SQL examples.

```text
                    User Question
                          │
                          ▼
                ┌──────────────────┐
                │ Embedding Model  │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ FAISS Vector DB  │
                └────────┬─────────┘
                         │
                  Similar Examples
                         │
                         ▼
                ┌──────────────────┐
                │ Prompt Builder   │
                └────────┬─────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Groq LLM  │
                  └──────┬──────┘
                         │
                         ▼
                    T-SQL Query
```

This approach helps provide the model with examples of the expected:

* Database structure
* SQL syntax
* Table relationships
* Aggregation patterns
* Business question → SQL patterns

---

# 🛡️ Defense-in-Depth Design

The system separates **AI generation** from **database execution**.

```text
┌─────────────────────────────┐
│        User Input           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       LLM Generation        │
│                             │
│  Natural Language → SQL     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      SQL Cleaning           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      SQL Validation         │
│                             │
│   Security Guardrails       │
└──────────────┬──────────────┘
               │
          ┌────┴────┐
          │         │
        BLOCK     ALLOW
          │         │
          ▼         ▼
       Reject    SQL Server
                    │
                    ▼
                 Results
```

This architecture helps reduce the risk of directly executing unsafe LLM-generated SQL.

---

# 🧪 Error Handling

The application is designed to handle common failure scenarios including:

* Invalid LLM output
* Markdown-wrapped SQL
* Malformed JSON responses
* Invalid SQL syntax
* Forbidden SQL operations
* Database connection errors
* SQL execution errors
* Empty query results

Instead of allowing an error to terminate the application, the Streamlit interface provides feedback to the user.

---

# 💡 Example Use Case

Imagine a retail manager wants to know:

> **"Which T-shirt brand generated the most revenue?"**

Without the application, the user would need to understand:

```sql
SELECT
    t.brand,
    SUM(si.quantity * si.price) AS revenue
FROM sales_items si
JOIN t_shirts t
    ON si.t_shirt_id = t.t_shirt_id
GROUP BY t.brand
ORDER BY revenue DESC;
```

With the application, the user simply asks:

```text
Which T-shirt brand generated the most revenue?
```

The system handles:

```text
Natural Language
       ↓
Semantic Retrieval
       ↓
Few-Shot Prompting
       ↓
LLM SQL Generation
       ↓
SQL Cleaning
       ↓
Security Validation
       ↓
SQL Server Execution
       ↓
Business Answer
```

---

# 🚧 Future Improvements

Potential future enhancements include:

* [ ] Add database-level read-only credentials
* [ ] Add query timeout controls
* [ ] Add SQL query cost estimation
* [ ] Add more sophisticated SQL parsing
* [ ] Add role-based access control
* [ ] Add query logging and monitoring
* [ ] Add evaluation metrics for NL2SQL accuracy
* [ ] Add automated SQL correctness testing
* [ ] Expand the few-shot example library
* [ ] Add support for multiple databases
* [ ] Add visualization generation from query results
* [ ] Add conversational follow-up questions
* [ ] Add query caching
* [ ] Add production deployment with Docker
* [ ] Add automated CI/CD testing

---

# 🤝 Contributing

Contributions are welcome!

If you would like to improve the project, you can:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit your changes
5. Push the branch
6. Open a Pull Request

Example:

```bash
git checkout -b feature/new-guardrail

git add .

git commit -m "Add additional SQL security guardrail"

git push origin feature/new-guardrail
```

You can contribute improvements such as:

* Additional SQL guardrails
* New database schemas
* Better few-shot examples
* Improved prompt engineering
* UI enhancements
* Query evaluation
* Performance improvements
* Visualization capabilities

---

# 📄 License

This project is intended for educational, portfolio, and demonstration purposes.

Add your preferred license here if you plan to distribute the project publicly.

---

# 👨‍💻 Project Overview

This project demonstrates how **Generative AI, Retrieval-Augmented Generation concepts, Natural Language to SQL, vector search, and enterprise databases** can be combined into a practical business intelligence application.

The core idea is simple:

> **Make enterprise data accessible through natural language while maintaining a validation layer between AI-generated SQL and the database.**

### Key Concepts Demonstrated

```text
Generative AI
      │
      ├── LLMs
      ├── Prompt Engineering
      └── Natural Language Understanding
      │
      ▼
Retrieval
      │
      ├── Embeddings
      ├── FAISS
      └── Few-Shot Examples
      │
      ▼
Data Engineering
      │
      ├── SQL
      ├── SQL Server
      ├── SQLAlchemy
      └── pyodbc
      │
      ▼
Application Engineering
      │
      ├── Streamlit
      ├── Error Handling
      └── Security Guardrails
```

---

## ⭐ If You Find This Project Useful

Feel free to **star ⭐ the repository**, explore the code, and contribute improvements through issues or pull requests.
