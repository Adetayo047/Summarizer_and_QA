from langchain_ollama.llms import OllamaLLM

# Initialize once
model = OllamaLLM(model="llama3.2")

def summarize_text(text: str, max_length: int = 300) -> str:
    """
    Summarize the given text concisely.
    """
    prompt = f"""
    Summarize the following text concisely (max {max_length} words):

    {text}
    """
    return model.invoke(prompt)