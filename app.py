import streamlit as st
from loader import load_documents
from vector import init_vector_store
from chat import get_response, get_document_summary

st.set_page_config(page_title="Intelligent Document Chat", layout="wide")
st.title("📄 Intelligent Document Summarizer & Chatbot")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a document (TXT, CSV, PDF)", type=["txt", "csv", "pdf"])

if uploaded_file:
    # Save uploaded file temporarily
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load documents
    documents = load_documents(uploaded_file.name)
    st.success(f"✅ Loaded {len(documents)} document(s)")

    # Initialize vector store
    vector_store = init_vector_store(documents=documents)
    st.info("Chroma vector store initialized")

    # Generate summary
    with st.spinner("Generating document summary..."):
        summary = get_document_summary(documents)
        st.subheader("📄 Document Summary")
        st.write(summary)

    # Initialize chat history
    if "history" not in st.session_state:
        st.session_state.history = ""

    # --- Chat Section ---
    st.subheader("💬 Chat with your document")
    user_input = st.text_input("Your question:")

    if st.button("Ask") and user_input:
        answer, updated_history = get_response(user_input, st.session_state.history)
        st.session_state.history = updated_history

        st.markdown(f"**Assistant:** {answer}")
        st.markdown("---")

    # Optionally show conversation history
    with st.expander("Conversation History"):
        st.text(st.session_state.history)