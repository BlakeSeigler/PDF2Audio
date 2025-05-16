# This file contains all the logic involved in the PDF2Audio website for taking the file
# and returning the audio file that reads the content of the file. This file contains functions to read, filter, and generate
# the discussed pdf file


# Imports
import PyPDF2
from TTS.api import TTS
import sys

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



def filter_text(text):
    """
    Cleans up raw PDF text by removing empty lines and lines with only digits.

    Arguments:
    text: Raw string of extracted text from the PDF

    Returns:
    filtered_text: A cleaned string with meaningful content only
    """
    lines = text.split('\n')  # Split the full text into individual lines
    filtered_lines = [
        line for line in lines
        if line.strip() and not line.strip().isdigit()
    ]  # Keep non-empty, non-numeric lines
    return ' '.join(filtered_lines)  # Join lines into a single string



def pdf_to_audio(pdf_path, output_audio, text_save):
    """
    Complete pipeline to convert a PDF to an audio file using text-to-speech.

    Arguments:
    pdf_path: Path to the input PDF file
    output_audio: Path where the generated audio file will be saved
    text_save: Path where the cleaned text will be saved as a .txt file
    """
    print("Extracting text from PDF...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("Filtering text...")
    clean_text = filter_text(raw_text)
    print(clean_text)  # Optional: remove in production for long PDFs

    with open(text_save, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print("Converting to audio...")
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
    tts.tts_to_file(text=clean_text, file_path=output_audio)

    print(f"Audiobook saved as {output_audio}")



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
