# app.py

import streamlit as st
import tempfile
from pathlib import Path
from extractor import extract_text_from_file
from main import process_document  # Assuming your backend logic is here

st.set_page_config(page_title="📄 Document Text Extractor", layout="centered")
st.title("📄 Document Text Extractor")

# Step 1: Upload
uploaded_file = st.file_uploader(
    "Upload a PDF, Word Document (.docx), or ZIP file (containing PDFs and Word docs):",
    type=["pdf", "docx", "zip"]
)

# Step 2: Choose action
action = st.selectbox("Select Action", ["Extract Text", "Run Analysis", "Summarize"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info(f"Processing file: {uploaded_file.name}")

    try:
        # Extract text from file (or ZIP contents)
        extracted_data = extract_text_from_file(tmp_path)

        # Preview the text
        if isinstance(extracted_data, str):
            st.success("✅ Text extracted successfully")
            st.text_area("📜 Extracted Text", extracted_data, height=500)

        elif isinstance(extracted_data, dict):
            st.success("✅ Extracted multiple documents from ZIP")

            file_list = list(extracted_data.keys())
            selected_file = st.selectbox("Choose a file to preview", file_list)
            st.text_area("📜 Extracted Text", extracted_data[selected_file], height=500)

        # Step 3: Process the document
        process_document(tmp_path, action)

        # Step 4: Notify user
        st.info("✅ Your document is under processing. You'll receive the response via email after analysis.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
