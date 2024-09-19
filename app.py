from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/umoja.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash('Please fill out all fields.')
        return redirect(url_for('home'))

    if not validate_email(email):
        flash('Please enter a valid email address.')
        return redirect(url_for('home'))

    new_message = ContactMessage(name=name, email=email, message=message)
    try:
        db.session.add(new_message)
        db.session.commit()
        flash('Thank you for your message. We will get back to you soon!')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}')
    return redirect(url_for('home'))

def validate_email(email):
    import re
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

if __name__ == '__main__':
    # Ensure the database directory exists
    db_directory = 'database'
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
    
    # Ensure the database file exists
    db_file = os.path.join(db_directory, 'umoja.db')
    if not os.path.exists(db_file):
        open(db_file, 'w').close()  # Create an empty file
    
    with app.app_context():
        db.create_all()  # Create database tables
    
    app.run(debug=True)
