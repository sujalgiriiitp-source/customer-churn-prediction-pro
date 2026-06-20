import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import load_customers
from utils.ui_helpers import section_header, glass_container
from utils.config import COLORS

def render_insights():
    """Render the Business Insights page."""
    st.markdown("<h1>💡 Business Insights</h1>", unsafe_allow_html=True)
    
    df = load_customers()
    if df.empty:
        st.warning("No data available.")
        return
        
    churned_df = df[df['churn'] == 1]
    active_df = df[df['churn'] == 0]

    # Revenue Impact Analysis
    section_header("Revenue Impact")
    col1, col2 = st.columns(2)
    
    lost_revenue = churned_df['monthly_charges'].sum()
    recurring_revenue = active_df['monthly_charges'].sum()
    
    with col1:
        st.markdown(f"<div class='glass-card metric-card'><p class='metric-title text-danger'>Lost Monthly Revenue</p><h2 class='metric-value text-danger'>${lost_revenue:,.0f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='glass-card metric-card'><p class='metric-title text-success'>Active MRR</p><h2 class='metric-value text-success'>${recurring_revenue:,.0f}</h2></div>", unsafe_allow_html=True)

    # Key Churn Drivers
    section_header("Key Churn Drivers")
    
    # Analyze Contract Type Impact
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Churn Rate by Contract Type</h3>", unsafe_allow_html=True)
    
    contract_churn = df.groupby('contract_type')['churn'].mean().reset_index()
    contract_churn['churn'] = contract_churn['churn'] * 100
    
    fig_contract = px.bar(
        contract_churn, 
        x='contract_type', 
        y='churn',
        color='contract_type',
        labels={'churn': 'Churn Rate (%)', 'contract_type': 'Contract Type'}
    )
    fig_contract.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color=COLORS['text'], margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_contract, use_container_width=True)
    
    st.info("💡 **Insight**: Customers on Month-to-month contracts have a significantly higher churn rate. Consider offering discounts for annual upgrades.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Analyze Support Tickets
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Impact of Support Tickets on Churn</h3>", unsafe_allow_html=True)
    
    ticket_bins = pd.cut(df['num_support_tickets'], bins=[-1, 2, 5, 10], labels=['Low (0-2)', 'Medium (3-5)', 'High (>5)'])
    df['Ticket Group'] = ticket_bins
    ticket_churn = df.groupby('Ticket Group')['churn'].mean().reset_index()
    ticket_churn['churn'] = ticket_churn['churn'] * 100
    
    fig_tickets = px.bar(
        ticket_churn,
        x='Ticket Group',
        y='churn',
        color='Ticket Group',
        labels={'churn': 'Churn Rate (%)'}
    )
    fig_tickets.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color=COLORS['text'], margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_tickets, use_container_width=True)
    
    st.warning("⚠️ **Warning**: Customers with more than 5 support tickets are highly likely to churn. Proactive account management is required for these users.")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_insights()
