from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from typing import Optional
import os

DB_LOCATION = "./chroma_langchain_db"
COLLECTION_NAME = "DOCUMENTS"
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

def init_vector_store(documents: Optional[list[Document]] = None, ids: Optional[list[str]] = None) -> Chroma:
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=DB_LOCATION,
        embedding_function=embeddings
    )

    if documents:
        vector_store.add_documents(documents=documents, ids=ids or [str(i) for i in range(len(documents))])

    return vector_store

def get_retriever(k: int = 5):
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=DB_LOCATION,
        embedding_function=embeddings
    )
    return vector_store.as_retriever(search_kwargs={"k": k})