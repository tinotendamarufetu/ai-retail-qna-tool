few_shots = [
    {
        "Question": "How many white Nike T-shirts do we have in stock?",
        "SQLQuery": "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White';"
    },
    {
        "Question": "How much revenue will our store generate if we sell all Levi's T-shirts post discounts?",
        "SQLQuery": """SELECT SUM(t.price * t.stock_quantity * (1 - COALESCE(d.pct_discount, 0) / 100)) 
                        FROM t_shirts t 
                        LEFT JOIN discounts d ON t.t_shirt_id = d.t_shirt_id 
                        WHERE t.brand = 'Levi''s';"""
    },
    {
        "Question": "What is the total value of all S size t-shirts in stock?",
        "SQLQuery": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE size = 'S';"
    },
    {
        "Question": "Which t-shirt brand generated the highest total sales volume?",
        "SQLQuery": """SELECT TOP 1 t.brand, SUM(si.quantity) AS total_sold 
                        FROM sales_items si 
                        JOIN t_shirts t ON si.t_shirt_id = t.t_shirt_id 
                        GROUP BY t.brand 
                        ORDER BY total_sold DESC;"""
    },
    {
        "Question": "What is our total sales revenue for this current month?",
        "SQLQuery": """SELECT SUM(total_amount) 
                        FROM sales 
                        WHERE MONTH(sale_date) = MONTH(GETDATE()) 
                        AND YEAR(sale_date) = YEAR(GETDATE());"""
    },
    {
        "Question": "How many transactions were completed using UPI payment method?",
        "SQLQuery": "SELECT COUNT(*) FROM sales WHERE payment_method = 'UPI';"
    }
]