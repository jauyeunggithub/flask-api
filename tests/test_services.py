from app import app, mail
from flask_mail import Message
from flask import current_app
import pytest

# Test email sending service
@pytest.fixture
def client():
    with app.app_context():  # Ensure the app context is active during tests
        with app.test_client() as client:
            yield client  # Provide the test client for the test

def test_send_email_service(client):
    with app.app_context():  # Ensure app context is available for mail handling
        msg = Message(
            subject='Test Subject',
            recipients=['recipient@example.com'],
            body='Test email body'
        )

        # Send the email through Flask-Mail
        mail.send(msg)

        # Check if the email has been added to the outgoing emails list
        assert len(current_app.mail.outbox) == 1  # Ensure one email is in the outbox
        assert current_app.mail.outbox[0].subject == 'Test Subject'  # Verify the subject
        assert current_app.mail.outbox[0].body == 'Test email body'  # Verify the body
