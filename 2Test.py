import streamlit as st
import requests
import yaml
from utils.uploader import validate_and_extract_files

# Load dropdown config
with open("configs/frontend_config.yaml", "r") as f:
    config = yaml.safe_load(f)

st.title("GenAI Document Processor")

# Dropdown
option = st.selectbox("Select Action", [opt["name"] for opt in config["dropdown_options"]])

# File uploader
uploaded_file = st.file_uploader("Upload ZIP or Single PDF/DOCX", type=["zip", "pdf", "docx"])

if uploaded_file:
    files = validate_and_extract_files(uploaded_file)
    if st.button("Submit"):
        with st.spinner("Processing..."):
            res = requests.post("http://localhost:8000/process", files=files, data={"action": option})
            st.success("Done")
            st.json(res.json())
