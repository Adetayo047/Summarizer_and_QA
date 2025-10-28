from loader import load_documents
from vector import init_vector_store
from chat import get_response, get_document_summary

# === Example: Upload a document ===
file_path = "example.pdf"  # TXT, CSV, PDF
documents = load_documents(file_path)

# Add documents to vector store
vector_store = init_vector_store(documents=documents)

# === Generate summary ===
summary = get_document_summary(documents)
print("📄 Document Summary:\n", summary)

# === Start multi-turn chat ===
history = ""
while True:
    question = input("\nYour question (type 'exit' to quit): ")
    if question.lower() in ["exit", "quit"]:
        break
    answer, history = get_response(question, history)
    print("Assistant:", answer)