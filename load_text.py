"""

This is the main file containing the software to scan a given PDF and create a recording with that audio.

by Blake Seigler

"""
import PyPDF2
from TTS.api import TTS
from pydub import AudioSegment
import io
from tqdm import tqdm
import numpy as np

# Read PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Filter Text (Basic Placeholder) -- Will need to add more advanced filtering functionality likely
def filter_text(text):
    lines = text.split('\n')
    filtered_lines = [line for line in lines if line.strip() and not line.strip().isdigit()] # removes lines with only spaces or digits
    return ' '.join(filtered_lines)

# Convert Text to Audio in batches
def process_in_batches(text, output_audio, batch_size=1000):
    chunks = [text[i:i+batch_size] for i in range(0, len(text), batch_size)]
    total_batches = len(chunks)
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True, gpu=False)
    combined_audio = AudioSegment.empty() 

    for idx, chunk in enumerate(tqdm(chunks, desc="Processing Batches"), start=1):

        audio_data_list = tts.tts(text=chunk)
        audio_data = np.array(audio_data_list)

        # Convert raw audio to AudioSegment
        audio_segment = AudioSegment(
            audio_data.tobytes(), 
            frame_rate=22050,  # Default for many TTS models
            sample_width=2,    # 16-bit audio (2 bytes per sample)
            channels=1         # Mono audio
        )

        # Append the batch's audio to the combined audio
        combined_audio += audio_segment

    # Save the final audio to the file
    combined_audio.export(output_audio, format="wav")
    print(f"Audiobook saved as {output_audio}")

        

# Main Pipeline
def pdf_to_audio(pdf_path, output_audio):
    print("Extracting text from PDF...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("Filtering text...")
    clean_text = filter_text(raw_text)

    print("Converting to audio...")
    process_in_batches(clean_text, output_audio)

    print(f"Audiobook saved as {output_audio}")


# Function Call
if __name__ == "__main__":
    pdf_path = "test.pdf"        # Replace with your PDF file
    output_audio = "test.wav"  # Output audio file name
    pdf_to_audio(pdf_path, output_audio)