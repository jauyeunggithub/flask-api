from flask import jsonify, request
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, mail
from flask_app.models import User, Role, EmailNotification
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Home page!"})

# Route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data:
        # Create a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'], method='sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    return jsonify({"message": "Bad request. Please provide valid data."}), 400

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data:
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "Login successful!", "user_id": user.id}), 200
        return jsonify({"message": "Login failed. Check your credentials."}), 401
    return jsonify({"message": "Bad request. Please provide email and password."}), 400

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful!"}), 200

# Protected route for dashboard (only logged-in users can access this)
@app.route('/dashboard')
@login_required
def dashboard():
    return jsonify({"message": "Welcome to your dashboard", "user_id": current_user.id, "username": current_user.username})

# Route to send an email
@app.route('/send_email', methods=['POST'])
@login_required
def send_email():
    data = request.get_json()
    if data:
        subject = data['subject']
        to = data['to']
        body = data['body']

        # Send the email using Flask-Mail
        msg = Message(subject, recipients=[to])
        msg.body = body
        mail.send(msg)

        # Create an EmailNotification record in the database
        email_notification = EmailNotification(
            message="Email sent",
            user_id=current_user.id,
            email_subject=subject,
            email_body=body
        )
        db.session.add(email_notification)
        db.session.commit()

        return jsonify({"message": "Email sent successfully!"}), 200
    return jsonify({"message": "Bad request. Please provide the necessary fields."}), 400

# Route to manage user roles (assign a role to a user)
@app.route('/assign_role', methods=['POST'])
@login_required
def assign_role():
    data = request.get_json()
    if data:
        user_id = data['user_id']
        role_name = data['role_name']
        user = User.query.get(user_id)
        if user:
            new_role = Role(role_name=role_name, user_id=user.id)
            db.session.add(new_role)
            db.session.commit()
            return jsonify({"message": f"Role '{role_name}' assigned to user successfully!"}), 200
        return jsonify({"message": "User not found."}), 404
    return jsonify({"message": "Bad request. Please provide user_id and role_name."}), 400

# Route to change user's password
@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    if data:
        new_password = data['new_password']
        current_user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        return jsonify({"message": "Password updated successfully!"}), 200
    return jsonify({"message": "Bad request. Please provide the new password."}), 400
