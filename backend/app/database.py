import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    config = {
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'employee_db'),
    }
    return mysql.connector.connect(**config)

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            department VARCHAR(100),
            salary DECIMAL(10, 2)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
