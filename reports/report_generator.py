import streamlit as st
import pandas as pd
from fpdf import FPDF
import io
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import load_customers, get_prediction_history
from utils.ui_helpers import section_header

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Customer Churn Prediction Pro - Executive Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(df, predictions_df):
    """Generate a PDF report using FPDF."""
    pdf = PDFReport()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Overview', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    total_customers = len(df)
    churn_rate = (df['churn'].sum() / total_customers * 100) if total_customers > 0 else 0
    total_revenue = df['total_charges'].sum()
    
    pdf.cell(0, 10, f'Total Customers: {total_customers}', 0, 1)
    pdf.cell(0, 10, f'Overall Churn Rate: {churn_rate:.2f}%', 0, 1)
    pdf.cell(0, 10, f'Total Revenue: ${total_revenue:,.2f}', 0, 1)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Recent Predictions', 0, 1)
    
    pdf.set_font('Arial', '', 10)
    if not predictions_df.empty:
        # Table Header
        pdf.cell(40, 10, 'Customer ID', 1)
        pdf.cell(40, 10, 'Probability', 1)
        pdf.cell(40, 10, 'Risk Level', 1)
        pdf.ln()
        
        # Table Rows
        for _, row in predictions_df.head(20).iterrows():
            pdf.cell(40, 10, str(row['customer_id']), 1)
            pdf.cell(40, 10, f"{row['churn_probability']:.2f}", 1)
            pdf.cell(40, 10, str(row['risk_category']), 1)
            pdf.ln()
    else:
        pdf.cell(0, 10, 'No predictions available yet.', 0, 1)

    return pdf.output(dest='S').encode('latin-1')

def render_reports():
    """Render the Reports page."""
    st.markdown("<h1>📄 Reports & Exports</h1>", unsafe_allow_html=True)
    
    df = load_customers()
    predictions_df = get_prediction_history()
    
    if df.empty:
        st.warning("No data available to generate reports.")
        return
        
    section_header("Download Full Dataset")
    st.markdown("<p class='text-muted'>Export the complete customer dataset as a CSV file.</p>", unsafe_allow_html=True)
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Customers CSV",
        data=csv_data,
        file_name='customer_data_export.csv',
        mime='text/csv',
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    section_header("Download Prediction History")
    if not predictions_df.empty:
        pred_csv = predictions_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Predictions CSV",
            data=pred_csv,
            file_name='prediction_history.csv',
            mime='text/csv',
        )
    else:
        st.info("No predictions have been made yet.")
        
    st.markdown("<hr>", unsafe_allow_html=True)
    
    section_header("Executive Summary PDF")
    st.markdown("<p class='text-muted'>Generate a PDF report summarizing key metrics and recent predictions.</p>", unsafe_allow_html=True)
    
    if st.button("Generate PDF Report"):
        with st.spinner("Generating PDF..."):
            try:
                pdf_bytes = create_pdf(df, predictions_df)
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name="executive_summary.pdf",
                    mime="application/pdf"
                )
                st.success("PDF generated successfully! Click the download button above.")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

if __name__ == "__main__":
    render_reports()
