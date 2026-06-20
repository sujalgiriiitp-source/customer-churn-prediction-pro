import os

# Project Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'churn_data.db')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.pkl')
DATA_DIR = os.path.join(BASE_DIR, 'database')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# App Constants
APP_TITLE = "Customer Churn Prediction Pro"
APP_ICON = "📈"

# UI Colors (Premium Dark Theme with accents)
COLORS = {
    'primary': '#00d4ff',
    'secondary': '#8a2be2',
    'background': '#0f172a',
    'card_bg': 'rgba(30, 41, 59, 0.7)',
    'text': '#f8fafc',
    'muted': '#94a3b8',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444'
}

# Feature Columns expected by the model
FEATURE_COLUMNS = [
    'Age', 'Tenure', 'MonthlyCharges', 'TotalCharges',
    'NumSupportTickets', 'NumDevices', 'HasInternet',
    'ContractType_Month-to-month', 'ContractType_One year', 'ContractType_Two year'
]

# Mapping for categorical features if needed
CONTRACT_TYPES = ['Month-to-month', 'One year', 'Two year']
