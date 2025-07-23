import pytest
from app import app, db
from flask import json
from flask_login import login_user
from flask_app.models import User, Role

# Setup the test client


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test user registration


def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    # Expecting redirect after successful registration
    assert response.status_code == 302
    assert b'Login' in response.data  # Ensure the response contains the login text

# Test user login


def test_login(client):
    # First, create the user
    user = User(username='testuser', email='test@example.com',
                password='testpassword')
    db.session.add(user)
    db.session.commit()

    response = clien
