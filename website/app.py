from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename
import os
import tempfile
import subprocess

app = Flask(__name__)

# Limit file size to 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.route('/submit', methods=['POST'])
def submit_pdf():
    if 'pdfFile' not in request.files:
        return "No file uploaded", 400

    file = request.files['pdfFile']
    if file.filename == '':
        return "No file selected", 400

    if not file.filename.lower().endswith('.pdf'):
        return "Only PDFs allowed", 400

    # Save file to temp dir
    with tempfile.TemporaryDirectory() as tempdir:
        filename = secure_filename(file.filename)
        filepath = os.path.join(tempdir, filename)
        file.save(filepath)

        # Construct expected zip output path
        base_name = os.path.splitext(filename)[0]
        zip_output = os.path.join(tempdir, f"{base_name}.zip")

        # Run PDF-to-audio conversion
        result = subprocess.run(
            ["python3", "utilities/PDF2Audio.py", filepath],
            capture_output=True,
            text=True
        )

        print(result.returncode, os.path.exists(zip_output))
        if result.returncode != 0 or not os.path.exists(zip_output):
            print("Error:", result.stderr)
            return "PDF processing failed", 500

        # Return the zip file
        return send_file(zip_output, as_attachment=True, download_name=f"{base_name}.zip")

@app.route('/')
def index():
    with open('public/index.html') as f:
        return render_template_string(f.read())
