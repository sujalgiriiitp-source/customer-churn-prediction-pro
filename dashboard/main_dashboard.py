import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import load_customers
from utils.ui_helpers import metric_card, section_header, load_css
from utils.config import COLORS

def render_dashboard():
    """Render the main dashboard page."""
    load_css()
    
    st.markdown("<h1>📊 Executive Dashboard</h1>", unsafe_allow_html=True)
    
    df = load_customers()
    if df.empty:
        st.warning("No data available. Please check the database.")
        return

    # Calculate KPIs
    total_customers = len(df)
    churned_customers = df['churn'].sum()
    active_customers = total_customers - churned_customers
    churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0
    total_revenue = df['total_charges'].sum()
    monthly_recurring_revenue = df[df['churn'] == 0]['monthly_charges'].sum()

    # Layout for KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Customers", f"{total_customers:,}", delta=None)
    with col2:
        metric_card("Active Customers", f"{active_customers:,}", delta=None)
    with col3:
        metric_card("Churn Rate", f"{churn_rate:.1f}%", delta=None)
    with col4:
        metric_card("Total Revenue", f"${total_revenue:,.0f}", delta=None)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Customer Status</h3>", unsafe_allow_html=True)
        
        status_counts = pd.DataFrame({
            'Status': ['Active', 'Churned'],
            'Count': [active_customers, churned_customers]
        })
        
        fig_status = px.pie(
            status_counts, 
            values='Count', 
            names='Status',
            hole=0.6,
            color='Status',
            color_discrete_map={'Active': COLORS['success'], 'Churned': COLORS['danger']}
        )
        fig_status.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=COLORS['text'],
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_status, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Revenue by Contract Type</h3>", unsafe_allow_html=True)
        
        rev_by_contract = df.groupby('contract_type')['total_charges'].sum().reset_index()
        fig_rev = px.bar(
            rev_by_contract, 
            x='contract_type', 
            y='total_charges',
            color='contract_type',
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success']]
        )
        fig_rev.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=COLORS['text'],
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis_title="",
            yaxis_title="Total Revenue ($)"
        )
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Recent Customers Table
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Recent Customer Data</h3>", unsafe_allow_html=True)
    display_df = df.copy()
    display_df['Status'] = display_df['churn'].apply(lambda x: 'Churned' if x == 1 else 'Active')
    st.dataframe(display_df[['customer_id', 'gender', 'age', 'contract_type', 'Status', 'monthly_charges']].head(10), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()
