import sqlite3
import pandas as pd
import os
import sys
from datetime import datetime

# Add parent directory to path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import DB_PATH

def get_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def init_db():
    """Initialize the database with necessary tables."""
    conn = get_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Create customers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id TEXT PRIMARY KEY,
                    gender TEXT,
                    age INTEGER,
                    tenure INTEGER,
                    monthly_charges REAL,
                    total_charges REAL,
                    num_support_tickets INTEGER,
                    num_devices INTEGER,
                    has_internet INTEGER,
                    contract_type TEXT,
                    churn INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create predictions history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id TEXT,
                    age INTEGER,
                    tenure INTEGER,
                    monthly_charges REAL,
                    total_charges REAL,
                    num_support_tickets INTEGER,
                    num_devices INTEGER,
                    has_internet INTEGER,
                    contract_type TEXT,
                    churn_probability REAL,
                    risk_category TEXT,
                    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create analytics logs table (for Admin Panel)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

def log_action(action, details=""):
    """Log an action to the database."""
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (action, details) VALUES (?, ?)", (action, details))
        conn.commit()
        conn.close()

def load_customers():
    """Load all customers into a pandas DataFrame."""
    conn = get_connection()
    if conn is not None:
        df = pd.read_sql_query("SELECT * FROM customers", conn)
        conn.close()
        return df
    return pd.DataFrame()

def save_customers(df):
    """Save a pandas DataFrame of customers to the database."""
    conn = get_connection()
    if conn is not None:
        df.to_sql('customers', conn, if_exists='append', index=False)
        conn.close()

def save_prediction(customer_data, probability, risk_category):
    """Save a prediction result to the history."""
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (
                customer_id, age, tenure, monthly_charges, total_charges,
                num_support_tickets, num_devices, has_internet, contract_type,
                churn_probability, risk_category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_data.get('customer_id', 'UNKNOWN'),
            customer_data.get('Age', 0),
            customer_data.get('Tenure', 0),
            customer_data.get('MonthlyCharges', 0.0),
            customer_data.get('TotalCharges', 0.0),
            customer_data.get('NumSupportTickets', 0),
            customer_data.get('NumDevices', 0),
            customer_data.get('HasInternet', 0),
            customer_data.get('ContractType', 'Unknown'),
            probability,
            risk_category
        ))
        conn.commit()
        conn.close()

def get_prediction_history():
    """Fetch prediction history."""
    conn = get_connection()
    if conn is not None:
        df = pd.read_sql_query("SELECT * FROM predictions ORDER BY predicted_at DESC", conn)
        conn.close()
        return df
    return pd.DataFrame()

def get_logs():
    """Fetch system logs."""
    conn = get_connection()
    if conn is not None:
        df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
        conn.close()
        return df
    return pd.DataFrame()

def clear_data():
    """Clear all data from tables (for testing/admin)."""
    conn = get_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM predictions")
        cursor.execute("DELETE FROM logs")
        conn.commit()
        conn.close()

# Initialize DB on import
init_db()
