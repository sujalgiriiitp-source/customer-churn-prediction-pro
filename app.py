import streamlit as st
import os
import sys

# Page Configuration
st.set_page_config(
    page_title="Customer Churn Prediction Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS globally
def load_css():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'style.css')
    try:
        with open(css_path, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Import page modules
from dashboard.main_dashboard import render_dashboard
from analytics.customer_analytics import render_analytics
from prediction.churn_prediction import render_prediction
from business_insights.insights import render_insights
from reports.report_generator import render_reports
from admin.admin_panel import render_admin

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00d4ff;'>📈 Churn Pro</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    selected_page = st.radio(
        "Navigation",
        ["📊 Executive Dashboard", "👥 Customer Analytics", "🔮 Churn Prediction", "💡 Business Insights", "📄 Reports & Exports", "⚙️ Admin Panel"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>Version 1.0.0<br>Customer Churn Prediction Pro</p>", unsafe_allow_html=True)

# Main Page Routing
if selected_page == "📊 Executive Dashboard":
    render_dashboard()
elif selected_page == "👥 Customer Analytics":
    render_analytics()
elif selected_page == "🔮 Churn Prediction":
    render_prediction()
elif selected_page == "💡 Business Insights":
    render_insights()
elif selected_page == "📄 Reports & Exports":
    render_reports()
elif selected_page == "⚙️ Admin Panel":
    render_admin()
