from langchain_core.documents import Document
import pandas as pd
from PyPDF2 import PdfReader
import os

def load_documents(file_path: str) -> list[Document]:
    documents = []

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if line.strip():
                documents.append(Document(page_content=line.strip(), metadata={"source": file_path}))

    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        for i, row in df.iterrows():
            content = " ".join([str(row[col]) for col in df.columns])
            documents.append(Document(page_content=content.strip(), metadata={"source": file_path, "row": i}))

    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                documents.append(Document(page_content=text.strip(), metadata={"source": file_path, "page": i}))

    else:
        raise ValueError("Unsupported file format. Supported: TXT, CSV, PDF")

    return documents