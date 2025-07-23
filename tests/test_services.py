from flask_mail import Message
from app import app, mail
import pytest


@pytest.fixture
def client():
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'

    with app.app_context():
        with app.test_client() as client:
            mail.init_app(app)
            yield client

def test_send_email_service(client):
    msg = Message(
        subject='Test Subject',
        recipients=['recipient@example.com'],
        body='Test email body'
    )

    with mail.record_messages() as outbox:
        mail.send(msg)

        assert len(outbox) == 1
        assert outbox[0].subject == 'Test Subject'
        assert outbox[0].recipients == ['recipient@example.com']
        assert outbox[0].body == 'Test email body'
