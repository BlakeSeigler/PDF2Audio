# This file contains all the logic involved in the PDF2Audio website for taking the file
# and returning the audio file that reads the content of the file. This file contains functions to read, filter, and generate
# the discussed pdf file


# Imports
import PyPDF2
from TTS.api import TTS
import sys
import requests
import os
import zipfile
from dotenv import load_dotenv
import re

# Load the api key and model name
load_dotenv()
HF_API_KEY = os.getenv('HF_API_KEY')


def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file.

    Arguments:
    pdf_path: Path to the PDF file

    Returns:
    text: All text extracted from the PDF as a single string
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""  # Avoid NoneType
    return text



def chunk_and_filter_main_content(text, model_url="https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1", max_chars=3000):
    """
    Splits the raw PDF text into chunks, then uses an LLM to remove anything that isn't core content
    (titles, footers, headers, copyright, etc), while preserving main content verbatim.

    Arguments:
    - text: Full extracted raw text from a PDF
    - model_url: Hugging Face model inference endpoint
    - max_chars: Max character size per prompt (based on model token limits)

    Returns:
    - filtered_content: Full cleaned version of the text
    """
    if not HF_API_KEY:
        raise ValueError("Missing HF_TOKEN in environment variables.")

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    # Split by sentence and reassemble into chunks
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    filtered_chunks = []

    for chunk in chunks:
        prompt = (
            "Remove any page numbers, titles, copyright info, headers, and non-content text. "
            "Return only the main body content *exactly as written*, without rewording or summarizing.\n\n"
            f"Text:\n{chunk}"
        )

        response = requests.post(
            model_url,
            headers=headers,
            json={"inputs": prompt}
        )

        if response.status_code != 200:
            print(f"Error from HF API: {response.status_code} — {response.text}")
            continue

        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            filtered_chunks.append(data[0]["generated_text"])
        elif isinstance(data, list) and "summary_text" in data[0]:  # fallback
            filtered_chunks.append(data[0]["summary_text"])
        else:
            print("Unexpected response:", data)

    return " ".join(filtered_chunks)




def pdf_to_audio_bundle(pdf_path):
    """
    Full pipeline: extract, filter, TTS, and zip output files.
    Returns path to the .zip file containing audio + cleaned text.
    """
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    audio_path = f"{base}-audio.wav"
    text_path = f"{base}-text.txt"
    zip_path = f"{base}.zip"

    print("Extracting text...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("Filtering content...")
    clean_text = chunk_and_filter_main_content(raw_text)

    print("Saving text...")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print("Generating audio...")
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
    tts.tts_to_file(text=clean_text, file_path=audio_path)

    print("Creating zip file...")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(audio_path)
        zipf.write(text_path)

    print(f"Packaged result in: {zip_path}")
    return zip_path



if __name__ == "__main__":
    """
    CLI entry point, will be called by the server. Called with:
        python3 PDF2Audio.py <pdf_path> <output_audio_path> <output_text_path>
    """
    if len(sys.argv) != 4:
        print("Usage: python3 PDF2Audio.py <pdf_path> <output_audio_path> <output_text_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_audio = sys.argv[2]
    output_text = sys.argv[3]

    pdf_to_audio(pdf_path, output_audio, output_text)
