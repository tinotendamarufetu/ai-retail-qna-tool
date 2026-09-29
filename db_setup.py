import pyodbc
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "Tino")
DB_USER = os.getenv("DB_USER", "Tino\\tinot")
DB_NAME = os.getenv("DB_NAME", "retail_store_db")

def setup_database():
    # 1. Connect using Windows Authentication (Trusted Connection) or SQL Credentials
    conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_HOST};DATABASE=master;Trusted_Connection=yes;TrustServerCertificate=yes;"
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    # Create Database if not exists
    cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{DB_NAME}') CREATE DATABASE {DB_NAME}")
    cursor.close()
    conn.close()

    # Reconnect directly to the target DB
    conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_HOST};DATABASE={DB_NAME};Trusted_Connection=yes;TrustServerCertificate=yes;"
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # 2. Drop existing tables safely in SQL Server
    cursor.execute("""
    IF OBJECT_ID('sales_items', 'U') IS NOT NULL DROP TABLE sales_items;
    IF OBJECT_ID('sales', 'U') IS NOT NULL DROP TABLE sales;
    IF OBJECT_ID('discounts', 'U') IS NOT NULL DROP TABLE discounts;
    IF OBJECT_ID('t_shirts', 'U') IS NOT NULL DROP TABLE t_shirts;
    """)

    # 3. Create Tables (T-SQL Syntax)
    cursor.execute("""
    CREATE TABLE t_shirts (
        t_shirt_id INT IDENTITY(1,1) PRIMARY KEY,
        brand VARCHAR(50) NOT NULL,
        color VARCHAR(30) NOT NULL,
        size VARCHAR(5) CHECK (size IN ('XS', 'S', 'M', 'L', 'XL')) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        stock_quantity INT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE discounts (
        discount_id INT IDENTITY(1,1) PRIMARY KEY,
        t_shirt_id INT UNIQUE,
        pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
        FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE sales (
        sale_id INT IDENTITY(1,1) PRIMARY KEY,
        sale_date DATETIME NOT NULL,
        total_amount DECIMAL(10, 2) NOT NULL,
        payment_method VARCHAR(20) CHECK (payment_method IN ('Cash', 'Credit Card', 'UPI')) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE sales_items (
        item_id INT IDENTITY(1,1) PRIMARY KEY,
        sale_id INT NOT NULL,
        t_shirt_id INT NOT NULL,
        quantity INT NOT NULL,
        unit_price DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales(sale_id) ON DELETE CASCADE,
        FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id) ON DELETE CASCADE
    );
    """)

    # 4. Populate t_shirts
    brands = ['Nike', 'Adidas', 'Puma', "Levi's"]
    colors = ['Red', 'Blue', 'Black', 'White']
    sizes = ['XS', 'S', 'M', 'L', 'XL']

    for brand in brands:
        for color in colors:
            for size in sizes:
                price = round(random.uniform(15.0, 50.0), 2)
                stock = random.randint(10, 100)
                cursor.execute(
                    "INSERT INTO t_shirts (brand, color, size, price, stock_quantity) VALUES (?, ?, ?, ?, ?)",
                    (brand, color, size, price, stock)
                )

    # 5. Populate discounts
    cursor.execute("SELECT TOP 20 t_shirt_id FROM t_shirts ORDER BY NEWID()")
    discounted_ids = [row[0] for row in cursor.fetchall()]
    for tid in discounted_ids:
        pct = round(random.choice([10.0, 15.0, 20.0, 25.0, 30.0]), 2)
        cursor.execute("INSERT INTO discounts (t_shirt_id, pct_discount) VALUES (?, ?)", (tid, pct))

    # 6. Populate sales & sales_items
    payment_methods = ['Cash', 'Credit Card', 'UPI']
    start_date = datetime.now() - timedelta(days=60)

    for _ in range(150):
        sale_date = start_date + timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
        payment = random.choice(payment_methods)
        
        # Use OUTPUT INSERTED.sale_id to fetch the generated primary key instantly
        cursor.execute(
            "INSERT INTO sales (sale_date, total_amount, payment_method) OUTPUT INSERTED.sale_id VALUES (?, ?, ?)",
            (sale_date, 0.0, payment)
        )
        sale_id = int(cursor.fetchone()[0])

        num_items = random.randint(1, 4)
        sale_total = 0.0

        for _ in range(num_items):
            # Fetch a random valid t_shirt_id from the database
            cursor.execute("SELECT TOP 1 t_shirt_id, price FROM t_shirts ORDER BY NEWID()")
            t_shirt_id, u_price = cursor.fetchone()
            u_price = float(u_price)
            qty = random.randint(1, 3)
            
            cursor.execute(
                "INSERT INTO sales_items (sale_id, t_shirt_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (sale_id, t_shirt_id, qty, u_price)
            )
            sale_total += qty * u_price

        cursor.execute("UPDATE sales SET total_amount = ? WHERE sale_id = ?", (sale_total, sale_id))

    conn.commit()
    conn.close()
    print("✅ MS SQL Server database 'retail_store_db' setup completed successfully!")

if __name__ == "__main__":
    setup_database()