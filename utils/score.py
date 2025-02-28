import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
import joblib
import os

# Ensure NLTK data is downloaded
nltk.download('punkt', quiet=True)

# Load the model and vectorizer
model_path = 'resume_scoring_model.pkl'
vectorizer_path = 'vectorizer.pkl'

if os.path.exists(model_path) and os.path.exists(vectorizer_path):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
else:
    model = None
    vectorizer = None

def extract_text_from_pdf(filepath):
    text = extract_text(filepath)
    return text

def analyze_content(text):
    tokens = nltk.word_tokenize(text)
    return tokens

def analyze_skills(text, job_description):
    vectorizer = CountVectorizer().fit_transform([text, job_description])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1]

def analyze_resume(filepath):
    if model is None or vectorizer is None:
        raise FileNotFoundError("Model or vectorizer file not found. Please ensure 'resume_scoring_model.pkl' and 'vectorizer.pkl' are present.")

    text = extract_text_from_pdf(filepath)
    content_tokens = analyze_content(text)
    job_description = "example job description"  # Replace with actual job description
    skills_score = analyze_skills(text, job_description)
    
    # Vectorize the resume text
    resume_vectorized = vectorizer.transform([text])
    
    # Predict the score
    score = model.predict(resume_vectorized)[0]
    
    # Dummy issues for demonstration
    issues = ["Spelling mistake in 'experience'", "Too many bullet points in 'Work Experience' section"]
    
    return score, issues