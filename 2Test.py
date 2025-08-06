# extractor.py

import os
import zipfile
from pathlib import Path
from typing import Union, Dict
import fitz  # PyMuPDF
from docx import Document
import tempfile

def extract_text_from_pdf(file_path: Union[str, Path]) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path: Union[str, Path]) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_file(file_path: Union[str, Path]) -> Union[str, Dict[str, str]]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found")

    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(path)

    elif path.suffix.lower() == ".docx":
        return extract_text_from_docx(path)

    elif path.suffix.lower() == ".zip":
        return extract_text_from_zip(path)

    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

def extract_text_from_zip(zip_path: Union[str, Path]) -> Dict[str, str]:
    file_texts = {}
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                try:
                    if file_path.suffix.lower() in [".pdf", ".docx"]:
                        text = extract_text_from_file(file_path)
                        file_texts[file] = text
                except Exception as e:
                    print(f"Failed to extract {file}: {e}")
    return file_texts
