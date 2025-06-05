import streamlit as st

st.set_page_config(page_title="PDF Page Selector for Door Detection")
st.title("Step 1: Upload a PDF and Select Relevant Pages")

# Upload the PDF
pdf_file = st.file_uploader("Upload a multi-page shop drawing (PDF)", type=["pdf"])