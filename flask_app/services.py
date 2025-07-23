from flask_mail import Message
from app import mail


def send_email(subject, to, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)
