import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import MODEL_PATH, FEATURE_COLUMNS, COLORS
from utils.ui_helpers import section_header
from database.db_manager import save_prediction

def load_model():
    """Load the trained machine learning model."""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def process_upload(df, model_data):
    """Process uploaded CSV and generate predictions."""
    model = model_data['model']
    scaler = model_data['scaler']
    features = model_data['features']
    
    # Fill missing values and ensure columns match
    df = df.copy()
    if 'contract_type' in df.columns:
        df = pd.get_dummies(df, columns=['contract_type'])
        
    for col in features:
        if col not in df.columns:
            df[col] = 0
            
    X = df[features]
    
    try:
        X_scaled = scaler.transform(X)
    except Exception as e:
        st.error(f"Error transforming data: {e}")
        return None
    
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X_scaled)[:, 1]
    else:
        # Fallback if model doesn't support probability
        predictions = model.predict(X_scaled)
        probabilities = [0.9 if p == 1 else 0.1 for p in predictions]
        
    df['Churn Probability'] = probabilities
    
    def get_risk(prob):
        if prob > 0.7: return "High Risk"
        elif prob > 0.4: return "Medium Risk"
        else: return "Low Risk"
        
    df['Risk Category'] = df['Churn Probability'].apply(get_risk)
    
    # Save predictions to database (limit to 100 for performance)
    for _, row in df.head(100).iterrows():
        save_prediction(row.to_dict(), row['Churn Probability'], row['Risk Category'])
        
    return df

def render_prediction():
    """Render the Churn Prediction page."""
    st.markdown("<h1>🔮 Churn Prediction Model</h1>", unsafe_allow_html=True)
    
    model_data = load_model()
    
    if not model_data:
        st.warning("Model not found. Please train the model first from the Admin panel or by running model_trainer.py.")
        return
        
    st.markdown("<p class='text-muted'>Upload a CSV file containing customer data to predict their churn probability.</p>", unsafe_allow_html=True)
    
    # Sample format info
    with st.expander("View Expected CSV Format"):
        st.write("Your CSV should contain the following columns:")
        sample_df = pd.DataFrame({
            'customer_id': ['CUST-001'],
            'Age': [35],
            'Tenure': [24],
            'MonthlyCharges': [55.5],
            'TotalCharges': [1332.0],
            'NumSupportTickets': [2],
            'NumDevices': [1],
            'HasInternet': [1],
            'contract_type': ['Month-to-month']
        })
        st.dataframe(sample_df)

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded {len(df)} records.")
            
            with st.spinner("Analyzing and generating predictions..."):
                results_df = process_upload(df, model_data)
                
            if results_df is not None:
                st.markdown("<br>", unsafe_allow_html=True)
                section_header("Prediction Results")
                
                # Summary metrics
                high_risk = len(results_df[results_df['Risk Category'] == 'High Risk'])
                med_risk = len(results_df[results_df['Risk Category'] == 'Medium Risk'])
                low_risk = len(results_df[results_df['Risk Category'] == 'Low Risk'])
                
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"<div class='glass-card metric-card'><p class='metric-title text-danger'>High Risk Customers</p><h2 class='metric-value text-danger'>{high_risk}</h2></div>", unsafe_allow_html=True)
                col2.markdown(f"<div class='glass-card metric-card'><p class='metric-title text-warning'>Medium Risk Customers</p><h2 class='metric-value text-warning'>{med_risk}</h2></div>", unsafe_allow_html=True)
                col3.markdown(f"<div class='glass-card metric-card'><p class='metric-title text-success'>Low Risk Customers</p><h2 class='metric-value text-success'>{low_risk}</h2></div>", unsafe_allow_html=True)
                
                # Chart
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                risk_counts = pd.DataFrame({
                    'Category': ['High Risk', 'Medium Risk', 'Low Risk'],
                    'Count': [high_risk, med_risk, low_risk]
                })
                fig = px.bar(
                    risk_counts, 
                    x='Category', 
                    y='Count',
                    color='Category',
                    color_discrete_map={'High Risk': COLORS['danger'], 'Medium Risk': COLORS['warning'], 'Low Risk': COLORS['success']}
                )
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color=COLORS['text'], margin=dict(t=20, b=20, l=20, r=20))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Data Table
                st.markdown("<h3>Detailed Results</h3>", unsafe_allow_html=True)
                display_cols = ['customer_id', 'Churn Probability', 'Risk Category']
                available_cols = [c for c in display_cols if c in results_df.columns]
                
                # Add a few feature columns to display
                for c in ['Age', 'Tenure', 'MonthlyCharges']:
                    if c in results_df.columns: available_cols.append(c)
                    
                st.dataframe(
                    results_df[available_cols].style.background_gradient(subset=['Churn Probability'], cmap='Reds'),
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    render_prediction()
