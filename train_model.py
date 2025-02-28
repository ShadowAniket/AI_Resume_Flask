import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import joblib

# Load and preprocess the dataset
data = pd.read_csv('resume_data.csv')  # Ensure you have a dataset with resumes and scores
X = data['resume_text']
y = data['score']

# Vectorize the resume text
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X_vectorized = vectorizer.fit_transform(X)

# Train the model
model = LinearRegression()
model.fit(X_vectorized, y)

# Save the model and vectorizer
joblib.dump(model, 'resume_scoring_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
