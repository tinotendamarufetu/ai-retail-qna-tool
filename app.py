import streamlit as st
import pandas as pd
from langchain_helper import process_question, db

st.set_page_config(
    page_title="AtliQ Retail Q&A Assistant",
    page_icon="👕",
    layout="wide"
)

st.title("👕 T-Shirts Retail Store: Enterprise Database Q&A Tool")
st.caption("Ask natural language questions about inventory, discounts, sales revenue, and transactions.")

# Sidebar - Schema Viewer
with st.sidebar:
    st.header("🗄️ Database Schema")
    st.markdown("""
    **Tables in `retail_store_db`:**
    - `t_shirts`: Inventory details (brand, color, size, price, stock)
    - `discounts`: Percentage discounts linked to t-shirts
    - `sales`: Transaction receipts (date, total_amount, payment_method)
    - `sales_items`: Granular line items per transaction
    """)
    if st.checkbox("Show Table Metadata"):
        st.text(db.get_table_info())

# Session State for Query History
if "history" not in st.session_state:
    st.session_state.history = []

# Quick Ask Chips
st.subheader("💡 Quick Sample Questions")
col1, col2, col3, col4 = st.columns(4)

selected_query = None
if col1.button("White Nike Stock"):
    selected_query = "How many white Nike T-shirts do we have in stock?"
if col2.button("Levi's Post-Discount Revenue"):
    selected_query = "How much revenue will our store generate if we sell all Levi's T-shirts post discounts?"
if col3.button("Top Selling Brand"):
    selected_query = "Which t-shirt brand generated the highest total sales volume?"
if col4.button("UPI Transactions Count"):
    selected_query = "How many transactions were completed using UPI payment method?"

# Question Input Box
user_input = st.text_input("Enter your question for the database:", value=selected_query if selected_query else "")

if st.button("Submit Question", type="primary") and user_input:
    with st.spinner("Analyzing question & generating SQL..."):
        error, generated_sql, result = process_question(user_input)

        if error:
            st.error(error)
            with st.expander("Inspect Generated SQL"):
                st.code(generated_sql, language="sql")
        else:
            st.success("Query Executed Successfully!")
            
            # Display Results
            st.subheader("📊 Query Result")
            st.write(result)

            # Technical SQL Expander
            with st.expander("🔍 View Generated SQL Statement"):
                st.code(generated_sql, language="sql")

            # Save to Session History
            st.session_state.history.append({
                "question": user_input,
                "sql": generated_sql,
                "result": result
            })

# Query History Tab
if st.session_state.history:
    st.divider()
    st.subheader("📜 Session Query History")
    for idx, item in enumerate(reversed(st.session_state.history)):
        st.markdown(f"**Q: {item['question']}**")
        st.caption(f"SQL: `{item['sql']}` | Result: `{item['result']}`")