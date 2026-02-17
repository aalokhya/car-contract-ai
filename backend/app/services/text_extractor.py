import os
import re
from docx import Document
import pdfplumber


def clean_text(text: str) -> str:
    """Normalize spacing and remove extra line breaks"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".docx":
        text = extract_docx(file_path)
    elif ext == ".pdf":
        text = extract_pdf(file_path)
    else:
        return "Unsupported file type"

    return clean_text(text)


def extract_docx(path):
    doc = Document(path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)


def extract_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
