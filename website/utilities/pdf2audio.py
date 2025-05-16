# This file contains all the logic involved in the PDF2Audio website for taking the file
# and returning the audio file that reads the content of the file. This file contains functions to read, filter, and generate
# the discussed pdf file


# Imports
import PyPDF2
from TTS.api import TTS
import sys
import os 
import zipfile

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



def pdf_to_audio_bundle(pdf_path, tempdir):
    """
    Full pipeline: extract, filter, TTS, and zip output files.
    Returns path to the .zip file containing audio + cleaned text.
    """
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    audio_path = os.path.join(tempdir, f"{base}-audio.wav")
    text_path = os.path.join(tempdir, f"{base}-text.txt")
    zip_path = os.path.join(tempdir, f"{base}.zip")

    print("Extracting text...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("Filtering content...")
    clean_text = filter_text(raw_text)

    print("Saving text...")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print("Generating audio...")
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
    tts.tts_to_file(text=clean_text, file_path=audio_path)

    print("Creating zip file...")
    folder_name = base  # e.g., "mydocument"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(audio_path, arcname=os.path.join(folder_name, os.path.basename(audio_path)))
        zipf.write(text_path, arcname=os.path.join(folder_name, os.path.basename(text_path)))

    print(f"Packaged result in: {zip_path}")
    return zip_path



if __name__ == "__main__":
    """
    CLI entry point, will be called by the server. Called with:
        python3 PDF2Audio.py <pdf_path> <output_audio_path> <output_text_path>
    """

    if len(sys.argv) != 3:
        print("Usage: python3 PDF2Audio.py <pdf_path> <tempdir>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    tempdir = sys.argv[2]
    zip_file = pdf_to_audio_bundle(pdf_path=pdf_path, tempdir=tempdir)
