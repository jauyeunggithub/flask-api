from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, mail
from app.models import User, Role, EmailNotification
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

# Route for the home page


@app.route('/')
def home():
    return render_template('index.html')  # Simple home page

# Route for user registration


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        # Create a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'], method='sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')  # Registration form

# Route for user login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        return 'Login Failed. Check your credentials and try again.'
    return render_template('login.html')  # Login form

# Route for user logout


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Protected route for dashboard (only logged-in users can access this)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Route to send an email


@app.route('/send_email', methods=['POST'])
@login_required
def send_email():
    if request.method == 'POST':
        subject = request.form['subject']
        to = request.form['to']
        body = request.form['body']

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

        return jsonify({"message": "Email sent!"}), 200
    return render_template('send_email.html')  # Email sending form

# Route to manage user roles (assign a role to a user)


@app.route('/assign_role', methods=['POST'])
@login_required
def assign_role():
    if request.method == 'POST':
        user_id = request.form['user_id']
        role_name = request.form['role_name']
        user = User.query.get(user_id)
        if user:
            new_role = Role(role_name=role_name, user_id=user.id)
            db.session.add(new_role)
            db.session.commit()
            return jsonify({"message": f"Role '{role_name}' assigned to user!"}), 200
    return render_template('assign_role.html')  # Role assignment form

# Route to change user's password (optional feature for password change)


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        current_user.password = generate_password_hash(
            new_password, method='sha256')
        db.session.commit()
        return jsonify({"message": "Password updated!"}), 200
    return render_template('change_password.html')  # Password change form
