import streamlit as st
import os

def load_css():
    """Load the custom CSS file."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'style.css')
    try:
        with open(css_path, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Falling back to default styling.")

def metric_card(title, value, delta=None, delta_text=""):
    """Render a modern glassmorphism metric card."""
    
    delta_html = ""
    if delta is not None:
        if delta > 0:
            delta_html = f'<p class="text-success">↑ {delta}% {delta_text}</p>'
        elif delta < 0:
            delta_html = f'<p class="text-danger">↓ {abs(delta)}% {delta_text}</p>'
        else:
            delta_html = f'<p class="text-muted">No change {delta_text}</p>'

    html = f"""
    <div class="glass-card metric-card">
        <p class="metric-title">{title}</p>
        <h2 class="metric-value">{value}</h2>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def section_header(title, subtitle=None):
    """Render a section header."""
    st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='text-muted'>{subtitle}</p>", unsafe_allow_html=True)
        
def glass_container(content_html):
    """Render a generic glassmorphism container."""
    html = f"""
    <div class="glass-card">
        {content_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
