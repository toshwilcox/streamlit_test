import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="PDF Page Selector for Door Detection")
st.title("Step 1: Upload a PDF and Select Relevant Pages")

# Upload the PDF
pdf_file = st.file_uploader("Upload a multi-page shop drawing (PDF)", type=["pdf"])

if pdf_file:
    try:
        st.info("Converting PDF pages to images. This may take a few seconds...")

        # Open the PDF with PyMuPDF
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        total_pages = len(doc)

        # Page selection range to limit memory use
        st.write("### Preview a subset of pages")
        page_start = st.number_input("Start page (1-based)", min_value=1, max_value=total_pages, value=1)
        page_end = st.number_input("End page", min_value=page_start, max_value=total_pages, value=min(page_start + 9, total_pages))

        selected_pages = []
        pages_to_display = []

        for i in range(page_start - 1, page_end):
            page = doc.load_page(i)
            pix = page.get_pixmap(dpi=100)  # Lower DPI for memory efficiency
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            pages_to_display.append((i, img))

        st.write("### Select the pages that are relevant for door detection:")

        for i, page_img in pages_to_display:
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.checkbox(f"Select Page {i+1}", key=f"check_{i}"):
                    selected_pages.append(i)
            with col2:
                st.image(page_img, caption=f"Page {i+1}", width=400)

        if selected_pages:
            st.success(f"You selected {len(selected_pages)} page(s): {', '.join(str(p+1) for p in selected_pages)}")
            st.session_state['selected_pages'] = selected_pages
            st.session_state['pdf_uploaded'] = True
        else:
            st.warning("Please select at least one page to continue.")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
