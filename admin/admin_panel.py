import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import get_logs, clear_data
from utils.data_generator import setup_database
from models.model_trainer import train_and_evaluate_models
from utils.ui_helpers import section_header

def render_admin():
    """Render the Admin Panel."""
    st.markdown("<h1>⚙️ Admin Panel</h1>", unsafe_allow_html=True)
    
    # Dataset Management
    section_header("Dataset Management")
    st.warning("⚠️ These actions will modify the underlying database.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regenerate Dummy Dataset"):
            with st.spinner("Generating new dataset..."):
                setup_database(1000)
                st.success("Successfully generated new dataset!")
    
    with col2:
        if st.button("Clear All Data", type="primary"):
            with st.spinner("Clearing database..."):
                clear_data()
                st.success("All data cleared successfully.")

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Model Management
    section_header("Model Management")
    st.info("Train a new model based on the current data in the database.")
    
    if st.button("Train ML Models"):
        with st.spinner("Training models (Logistic Regression, Random Forest, Decision Tree)..."):
            results_df = train_and_evaluate_models()
            if results_df is not None:
                st.success("Models trained successfully. Best model saved.")
                st.dataframe(results_df)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # System Logs
    section_header("System Logs")
    logs_df = get_logs()
    
    if not logs_df.empty:
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("No system logs available.")

if __name__ == "__main__":
    render_admin()
