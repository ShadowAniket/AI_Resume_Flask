from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
import nltk
nltk.download('punkt_tab')
import os
import joblib

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the 'uploads' folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize the database
from models import db, User

db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints AFTER initializing db
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

def create_database():
    """Create database tables if they don't exist."""
    with app.app_context():
        db.create_all()
        print("✅ Database created successfully!")

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/upload_resume', methods=['POST'])
@login_required
def upload_resume():
    if 'resume' not in request.files:
        flash("No file uploaded", "danger")
        return redirect(url_for('home'))

    file = request.files['resume']
    if file.filename == '':
        flash("No selected file", "danger")
        return redirect(url_for('home'))

    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        flash("Resume uploaded successfully!", "success")
        
        # Analyze the resume and get the score
        from utils.score import analyze_resume
        score, issues = analyze_resume(filepath)
        
        return render_template('homepage.html', score=score, issues=issues, issues_count=len(issues))
    
    flash("Invalid file format. Upload a PDF.", "danger")
    return redirect(url_for('home'))

# Run the app
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
