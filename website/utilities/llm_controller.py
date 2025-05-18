from llama_cpp import Llama
from pathlib import Path

# Path Setup
file_path = Path(__file__).parent

# Path to your downloaded GGUF model
model_file_path = file_path.parent / "resources/tinyllama-1.1b-chat-v1.0.Q5_K_S.gguf"

# Define the model
llm = Llama(model_path=model_file_path.as_posix(), n_ctx=512) # as_posix() to convert path object to strings


def llm_text_filter(raw_text):
        """
        Uses a local TinyLlama model to clean raw PDF-extracted text.
        Removes headers, footers, and irrelevant lines.
        """
        prompt = f"""
            You are a helpful assistant that filters raw text extracted from a PDF file.
            Your task is to keep only the main readable body content and remove:

            - Page numbers
            - Headers and footers
            - Repeated titles
            - Irrelevant whitespace or numbers
            - Any other text sections that don't add to the main content of the section

            Please don't say anything but the filtered main content. Any additive words that aren't the main content will mess up the procedure.

            Raw text:
            \"\"\"{raw_text}\"\"\"

            Cleaned main content:
        """

        response = llm(prompt, max_tokens=1024, stop=["\n\n", "Raw text:", "Cleaned:"])

        with open('response.txt', "w", encoding="utf-8") as f:
            f.write(f"{response}")
        f.close()

        return response["choices"][0]["text"].strip()