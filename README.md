# Customer Churn Prediction Pro

A production-ready Customer Churn Prediction & Business Analytics Platform built with Python, Streamlit, Pandas, Scikit-Learn, and Plotly.

## 🌟 Overview

**Customer Churn Prediction Pro** analyzes customer data, predicts churn probability using Machine Learning, identifies risk factors, generates actionable business insights, and provides an executive dashboard for decision-making. 

## 🚀 Features

- **📊 Executive Dashboard**: High-level KPIs, total customers, churn rates, and revenue metrics.
- **👥 Customer Analytics**: Segment customers by demographics, contract types, and revenue breakdown.
- **🔮 Churn Prediction**: Upload a CSV file, run predictions using trained ML models, and view risk classifications (High, Medium, Low).
- **💡 Business Insights**: Actionable recommendations based on key churn drivers like contract types and support tickets.
- **📄 Reports**: Export full customer data, prediction history, and generate an Executive Summary PDF.
- **⚙️ Admin Panel**: Manage datasets, retrain ML models, and view system logs.

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit, Custom CSS (Premium Dark Theme with Glassmorphism)
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn (Logistic Regression, Random Forest, Decision Tree), Joblib
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Database**: SQLite
- **Reporting**: fpdf2

## 📁 Project Structure

```text
Customer Churn Prediction Pro/
├── app.py                      # Main entrypoint
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── database/                   # SQLite database & DB manager
├── models/                     # Saved ML models & training script
├── utils/                      # Configs, UI helpers, Data generator
├── assets/                     # Custom CSS & assets
├── dashboard/                  # Dashboard page module
├── analytics/                  # Analytics page module
├── prediction/                 # Prediction page module
├── business_insights/          # Insights page module
├── reports/                    # Reports page module
└── admin/                      # Admin Panel module
```

## ⚙️ Installation & Setup

1. **Clone the repository** (if applicable) or navigate to the project folder.

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database & Train Initial Model**:
   *The system is configured to auto-initialize, but you can also do it manually:*
   ```bash
   python utils/data_generator.py
   python models/model_trainer.py
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📝 Sample Data Format

To use the prediction tool, your CSV should include the following columns (case-sensitive):

- `customer_id` (String)
- `Age` (Numeric)
- `Tenure` (Numeric - Months)
- `MonthlyCharges` (Numeric)
- `TotalCharges` (Numeric)
- `NumSupportTickets` (Numeric)
- `NumDevices` (Numeric)
- `HasInternet` (1 or 0)
- `contract_type` (String: 'Month-to-month', 'One year', 'Two year')

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
# customer-churn-prediction-pro
