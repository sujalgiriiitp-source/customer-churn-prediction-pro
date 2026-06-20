import pandas as pd
import numpy as np
import random
import string
import os
import sys

# Add parent directory to path to import db_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import save_customers, clear_data, log_action

def generate_customer_id():
    """Generate a random customer ID like 'CUST-1234A'"""
    return f"CUST-{''.join(random.choices(string.digits, k=4))}{random.choice(string.ascii_uppercase)}"

def generate_mock_data(num_records=1000):
    """Generates synthetic customer churn data."""
    np.random.seed(42)
    random.seed(42)

    customer_ids = set()
    while len(customer_ids) < num_records:
        customer_ids.add(generate_customer_id())
    
    data = {
        'customer_id': list(customer_ids),
        'gender': np.random.choice(['Male', 'Female'], num_records),
        'age': np.random.randint(18, 80, num_records),
        'tenure': np.random.randint(1, 72, num_records), # in months
        'monthly_charges': np.round(np.random.uniform(20.0, 120.0, num_records), 2),
        'num_support_tickets': np.random.randint(0, 10, num_records),
        'num_devices': np.random.randint(1, 5, num_records),
        'has_internet': np.random.choice([1, 0], num_records, p=[0.8, 0.2]),
        'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], num_records, p=[0.5, 0.3, 0.2])
    }

    df = pd.DataFrame(data)
    
    # Calculate total charges
    df['total_charges'] = df['monthly_charges'] * df['tenure']
    
    # Introduce some logic for churn to make model training meaningful
    # Higher churn probability for:
    # - Month-to-month contract
    # - High monthly charges
    # - Low tenure
    # - High support tickets
    
    churn_prob = np.zeros(num_records)
    churn_prob += np.where(df['contract_type'] == 'Month-to-month', 0.4, 0.0)
    churn_prob += np.where(df['tenure'] < 12, 0.3, 0.0)
    churn_prob += np.where(df['monthly_charges'] > 80, 0.2, 0.0)
    churn_prob += np.where(df['num_support_tickets'] > 5, 0.3, 0.0)
    churn_prob -= np.where(df['contract_type'] == 'Two year', 0.4, 0.0)
    churn_prob -= np.where(df['age'] > 60, 0.1, 0.0)
    
    # Normalize and clip
    churn_prob = np.clip(churn_prob, 0.05, 0.95)
    
    # Generate actual churn labels based on probability
    df['churn'] = np.random.binomial(1, churn_prob)

    return df

def setup_database(num_records=1000):
    """Clear existing data and generate new data for the DB."""
    print("Clearing existing data...")
    clear_data()
    print(f"Generating {num_records} synthetic customer records...")
    df = generate_mock_data(num_records)
    print("Saving to database...")
    save_customers(df)
    log_action("Database Initialization", f"Generated {num_records} synthetic records.")
    print("Database setup complete.")
    return df

if __name__ == "__main__":
    setup_database()
