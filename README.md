Simply copy the Markdown block below and paste it directly into a file named README.md at the root of your GitHub repository.

Markdown
# 👕 T-Shirts Retail Store: Enterprise Database Q&A Tool

An enterprise-grade, Natural Language to SQL (NL2SQL) system built with **Streamlit**, **LangChain**, **Groq LLM**, and **Microsoft SQL Server**. This application allows users to ask plain English questions about retail inventory, sales transactions, discounts, and revenue, and receive immediate, execution-verified answers directly from an enterprise relational database.

---

<img width="1832" height="795" alt="image" src="https://github.com/user-attachments/assets/346249ef-5e19-49ea-9713-33242846b43a" />


## 🌟 Key Features

* **Natural Language to T-SQL Translation:** Translates complex retail questions into valid Microsoft SQL Server (T-SQL) queries.
* **Powered by Groq LPUs:** Utilizes fast, low-latency LLM inference (`openai/gpt-oss-120b`) via the Groq API.
* **Dynamic Few-Shot Learning:** Leverages **FAISS** vector store and **HuggingFace Embeddings** (`sentence-transformers/all-MiniLM-L6-v2`) to dynamically retrieve relevant SQL query examples for high-accuracy prompting.
* **Security Guardrails:** Includes a built-in SQL validator that detects and blocks destructive non-`SELECT` operations (e.g., `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`).
* **Robust Error Handling & Cleaning:** Automatically cleans LLM markdown code blocks, extracts structured JSON strings, and validates SQL syntax before database execution.
* **Interactive Streamlit Dashboard:** Features database schema exploration, sample question quick-triggers, SQL inspection accordions, and session history logging.

---

## 🏗️ Architecture & Data Pipeline

                                                  [ User Question ]
                                                          │
                                                          ▼
                          [ FAISS Vector Store ] ──► (Retrieves Similar Few-Shot Examples)
                                                          │
                                                          ▼
                  [ Dynamic Prompt Construction ] ──► (Combines Schema Info + Few-Shot + User Prompt)
                                                          │
                                                          ▼
                               [ Groq LLM Inference ] ──► (Generates Raw T-SQL String)
                                                          │
                                                          ▼
                   [ Clean & Validate Guardrails ] ──► (Strips Markdown/JSON, Blocks Destructive SQL)
                                                          │
                                                          ▼
                          [ MS SQL Server Execution ] ──► (Executes via pyodbc & SQLAlchemy)
                                                          │
                                                          ▼
                          [ Streamlit UI Output ] ──► (Displays Result Set & Session Logs)


---

## 📊 Database Schema Summary

The application interfaces with `retail_store_db` containing four primary tables:

* `t_shirts`: Product inventory details (`brand`, `color`, `size`, `price`, `stock_quantity`).
* `discounts`: Discount rates linked directly to specific T-shirt IDs.
* `sales`: High-level transaction receipts (`date`, `total_amount`, `payment_method`).
* `sales_items`: Granular line-item sales records connected to transactions and inventory.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* Microsoft SQL Server (with `ODBC Driver 18 for SQL Server` installed)
* Active [Groq API Key](https://console.groq.com/)

---

### Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/ai-retail-qna-tool.git](https://github.com/YOUR_USERNAME/ai-retail-qna-tool.git)
   cd ai-retail-qna-tool
Create and Activate a Virtual Environment:

Windows (PowerShell):

PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Mac/Linux:

Bash
python3 -m venv .venv
source .venv/bin/activate
Install Dependencies:

Bash
pip install -r requirements.txt
Configuration
Create a .env file in the root directory of your project and configure your environment variables:

Code snippet
GROQ_API_KEY=your_groq_api_key_here

# Database Configuration
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_NAME=retail_store_db
Running the Application
Launch the Streamlit web app:

Bash
streamlit run app.py
The application will open automatically in your browser at http://localhost:8501.

🛡️ Security & Guardrails
To protect enterprise databases against unauthorized modifications or prompt injection attacks, the application inspects generated queries prior to execution using regex pattern matching:

Python
def validate_sql_query(query: str) -> bool:
    forbidden_keywords = [r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b", r"\bALTER\b", r"\bTRUNCATE\b"]
    for keyword in forbidden_keywords:
        if re.search(keyword, query, re.IGNORECASE):
            return False
    return True
Any generated query containing data definition (DDL) or data manipulation (DML) statements other than SELECT is immediately intercepted and blocked.

📂 Project Structure
├── app.py                      # Main Streamlit UI and core execution pipeline
├── few_shots.py                # Few-shot example training dataset for RAG
├── check_available_models.py   # Utility script to inspect active Groq API models
├── .env                        # Environment variables (API keys & DB config) - GitIgnored
├── .gitignore                  # Git tracking rules
└── README.md                   # Project documentation
🤝 Contributing
Contributions are welcome! Please feel free to open an issue or submit a pull request if you'd like to add extra guardrails, extend table schemas, or enhance UI visualizations.
