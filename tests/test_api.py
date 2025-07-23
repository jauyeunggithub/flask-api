import pytest
from app import app, db
from flask import json


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_register(client):
    response = client.post('/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert b"User created!" in response.data


def test_send_email(client):
    response = client.post('/send_email', json={
        "subject": "Test Email",
        "to": "recipient@example.com",
        "body": "This is a test email."
    })
    assert response.status_code == 200
    assert b"Email sent!" in response.data
