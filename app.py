import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="PDF Page Selector for Door Detection")
st.title("Step 1: Upload a PDF and Select Relevant Pages")

# Upload the PDF
pdf_file = st.file_uploader("Upload a multi-page shop drawing (PDF)", type=["pdf"])

if pdf_file:
    st.info("Converting PDF pages to images. This may take a few seconds...")

    # Open the PDF with PyMuPDF
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pages = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        pages.append(img)

    selected_pages = []
    st.write("### Select the pages that are relevant for door detection:")

    for i, page in enumerate(pages):
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.checkbox(f"Select Page {i+1}", key=f"check_{i}"):
                selected_pages.append(i)
        with col2:
            st.image(page, caption=f"Page {i+1}", width=400)

    if selected_pages:
        st.success(f"You selected {len(selected_pages)} page(s): {', '.join(str(p+1) for p in selected_pages)}")
        st.session_state['selected_pages'] = selected_pages
        st.session_state['pages'] = pages
        st.session_state['pdf_uploaded'] = True
    else:
        st.warning("Please select at least one page to continue.")
