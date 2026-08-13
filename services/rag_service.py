import os
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import save_uploaded_file

def process_pdf_document(uploaded_file):
  file_path, filename = save_uploaded_file(uploaded_file)
  extracted_text = ""
  with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
      txt = page.extract_text()
      if txt:
        extracted_text += txt + "\n"

  # Break the document into manageable text blocks
  splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
  chunks = splitter.split_text(extracted_text)
  return chunks, filename