from summarizer import summarize_text
from vector import get_retriever
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize once
model = OllamaLLM(model="llama3.2")
retriever = get_retriever(k=5)

template = """
You are an intelligent assistant. Use relevant information from documents and previous conversation to answer concisely.

Conversation so far:
{history}

Relevant information:
{context}

User's question:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def get_response(question: str, history: str = "") -> tuple[str, str]:
    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs]) if isinstance(retrieved_docs, list) else str(retrieved_docs)

    # Generate response
    result = chain.invoke({"history": history, "context": context, "question": question})

    updated_history = f"{history}\nUser: {question}\nAssistant: {result}\n"
    return result, updated_history

def get_document_summary(documents: list, max_words: int = 300) -> str:
    """
    Summarize all uploaded documents into a single concise summary.
    """
    full_text = "\n\n".join([doc.page_content for doc in documents])
    summary = summarize_text(full_text, max_length=max_words)
    return summary