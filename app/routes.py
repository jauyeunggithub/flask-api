from flask import request, jsonify
from app import app, db, mail
from app.models import User, Role, EmailNotification
from flask_login import login_user, login_required, current_user
from flask_mail import Message


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'],
                    email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created!"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:  # Simplified check
        login_user(user)
        return jsonify({"message": "Logged in successfully!"})
    return jsonify({"message": "Invalid credentials!"}), 401


@app.route('/send_email', methods=['POST'])
@login_required
def send_email():
    data = request.get_json()
    msg = Message(data['subject'], recipients=[data['to']])
    msg.body = data['body']
    mail.send(msg)

    email_notification = EmailNotification(
        message="Email sent",
        user_id=current_user.id,
        email_subject=data['subject'],
        email_body=data['body']
    )
    db.session.add(email_notification)
    db.session.commit()
    return jsonify({"message": "Email sent!"}), 200
