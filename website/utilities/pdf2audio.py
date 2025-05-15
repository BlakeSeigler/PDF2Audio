import PyPDF2
from TTS.api import TTS
import torch
import transformers

# Read PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Filter Text (Basic filtering prot) -- Will need to add more advanced filtering functionality likely
def filter_text(text):
    lines = text.split('\n')
    filtered_lines = [line for line in lines if line.strip() and not line.strip().isdigit()] # removes lines with only spaces or digits
    return ' '.join(filtered_lines)

# Main Pipeline
def pdf_to_audio(pdf_path, output_audio, text_save):
    print("Extracting text from PDF...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("Filtering text...")
    clean_text = filter_text(raw_text)
    print(clean_text)
    with open(text_save, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print("Converting to audio...")
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
    tts.tts_to_file(text=clean_text,  file_path=output_audio)

    print(f"Audiobook saved as {output_audio}")


if __name__ == "__main__":
    import sys
    pdf_to_audio(pdf_path=sys.argv[1], output_audio=sys.argv[2], text_save=sys.argv[3])
