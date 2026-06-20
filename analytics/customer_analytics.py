import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import load_customers
from utils.ui_helpers import section_header, glass_container
from utils.config import COLORS

def render_analytics():
    """Render the Customer Analytics page."""
    st.markdown("<h1>👥 Customer Analytics</h1>", unsafe_allow_html=True)
    
    df = load_customers()
    if df.empty:
        st.warning("No data available.")
        return

    # Demographics Section
    section_header("Demographic Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Gender Distribution</h3>", unsafe_allow_html=True)
        fig_gender = px.pie(
            df, 
            names='gender', 
            color='gender',
            color_discrete_map={'Male': COLORS['primary'], 'Female': COLORS['secondary']},
            hole=0.4
        )
        fig_gender.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color=COLORS['text'], margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Age Distribution by Churn</h3>", unsafe_allow_html=True)
        fig_age = px.histogram(
            df, 
            x='age', 
            color='churn',
            barmode='overlay',
            color_discrete_map={0: COLORS['success'], 1: COLORS['danger']}
        )
        fig_age.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color=COLORS['text'], margin=dict(t=20, b=20, l=20, r=20))
        # Update legend
        for trace in fig_age.data:
            trace.name = 'Churned' if trace.name == '1' else 'Active'
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Customer Segmentation
    section_header("Customer Segmentation")
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Tenure vs Monthly Charges</h3>", unsafe_allow_html=True)
    fig_scatter = px.scatter(
        df, 
        x='tenure', 
        y='monthly_charges', 
        color='churn',
        opacity=0.7,
        color_discrete_map={0: COLORS['success'], 1: COLORS['danger']}
    )
    fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color=COLORS['text'], margin=dict(t=20, b=20, l=20, r=20))
    for trace in fig_scatter.data:
            trace.name = 'Churned' if trace.name == '1' else 'Active'
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_analytics()
