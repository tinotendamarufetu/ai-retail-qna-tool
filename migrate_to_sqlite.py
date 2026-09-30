import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "retail_store_db")

mssql_uri = f"mssql+pyodbc://@{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes"

print("Connecting to MS SQL Server...")
mssql_engine = create_engine(mssql_uri)

sqlite_file = "app.db"
if os.path.exists(sqlite_file):
    os.remove(sqlite_file)

sqlite_engine = create_engine(f"sqlite:///{sqlite_file}")
inspector = inspect(mssql_engine)
tables = inspector.get_table_names()

print(f"Found tables in MS SQL Server: {tables}")

with mssql_engine.connect() as mssql_conn:
    for table_name in tables:
        print(f"Migrating table: {table_name}...")
        df = pd.read_sql_table(table_name, mssql_conn)
        df.to_sql(table_name, sqlite_engine, if_exists="replace", index=False)

print(f"✅ Success! Created '{sqlite_file}' in project root.")