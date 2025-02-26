from flask import Flask, request, jsonify, render_template
import os
import pdfplumber  # For extracting text from PDFs
import spacy  # For NLP processing
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load NLP model
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF resume."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def analyze_resume(text):
    """Analyze resume using NLP."""
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']  # Example skill extraction
    return {"skills": skills, "word_count": len(doc)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    text = extract_text_from_pdf(file_path)
    analysis = analyze_resume(text)
    
    return jsonify({"filename": filename, "analysis": analysis})

if __name__ == '__main__':
    app.run(debug=True)
