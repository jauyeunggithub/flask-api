from app import app, mail
from app.models import User, EmailNotification
from flask_mail import Message
from flask import current_app
import pytest

# Test email sending service


def test_send_email_service(client):
    with app.app_context():
        msg = Message(subject='Test Subject', recipients=[
                      'recipient@example.com'])
        msg.body = 'Test email body'
        mail.send(msg)

        # Check if email has been added to the outgoing emails list
        # Flask-Mail stores emails in `outbox`
        assert len(current_app.mail.outbox) == 1
        assert current_app.mail.outbox[0].subject == 'Test Subject'
        assert current_app.mail.outbox[0].body == 'Test email body'
