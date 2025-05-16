from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename
import os
import tempfile
import zipfile
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

        subprocess.run([
            "python3", "utilities/PDF2Audio.py", filepath, tempdir
        ])

        base_name = os.path.splitext(filename)[0]
        zip_path = os.path.join(tempdir, f"{base_name}.zip")

        if not os.path.exists(zip_path):
            return "Zip file was not generated", 500

        # Return the zip file for download
        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"{base_name}.zip"
        )

@app.route('/')
def index():
    with open('public/index.html') as f:
        return render_template_string(f.read())
