import PyPDF2
from gtts import gTTS

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
    filtered_lines = [line for line in lines if line.strip() and not line.strip().isdigit()]
    return ' '.join(filtered_lines)

# Convert Text to Audio
def text_to_speech(text, output_file):
    tts = gTTS(text)
    tts.save(output_file)

# Main Pipeline
def pdf_to_audio(pdf_path, output_audio):
    print("Extracting text from PDF...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("Filtering text...")
    clean_text = filter_text(raw_text)

    print("Converting to audio...")
    text_to_speech(clean_text, output_audio)

    print(f"Audiobook saved as {output_audio}")


# Function Call
if __name__ == "__main__":
    pdf_path = "book.pdf"        # Replace with your PDF file
    output_audio = "audiobook.mp3"  # Output audio file name
    pdf_to_audio(pdf_path, output_audio)