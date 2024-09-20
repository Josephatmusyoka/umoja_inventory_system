from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(15), unique=True)
    profile_picture = db.Column(db.String(100))  # Path to the image
    role = db.Column(db.String(50))
    password = db.Column(db.String(200))

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
        flash('Please fill out all fields.', 'error')
        return redirect(url_for('home'))

    if not validate_email(email):
        flash('Please enter a valid email address.', 'error')
        return redirect(url_for('home'))

    new_message = ContactMessage(name=name, email=email, message=message)
    try:
        db.session.add(new_message)
        db.session.commit()
        flash('Thank you for your message. We will get back to you soon!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'error')
    return redirect(url_for('home'))

def validate_email(email):
    import re
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        title = request.form['title']
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        profile_picture = request.files['profile_picture']
        role = request.form['role']
        password = request.form['password']

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Save the profile picture if provided
        if profile_picture:
            picture_path = os.path.join('static/images', profile_picture.filename)
            profile_picture.save(picture_path)
        else:
            picture_path = None

        new_user = User(
            title=title,
            first_name=first_name,
            second_name=second_name,
            username=username,
            email=email,
            phone=phone,
            profile_picture=picture_path,
            role=role,
            password=hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'error')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return jsonify({"message": "Login successful!"}), 200
        return jsonify({"message": "Invalid username or password."}), 401

    return render_template('login.html')  # Display login form for GET request


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
