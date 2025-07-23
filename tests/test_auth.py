from app import app, db
from app.models import User
from flask_login import login_user, logout_user
import pytest

# Test user registration and login


def test_user_registration(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    # Expect redirect after successful registration
    assert response.status_code == 302
    assert b'Login' in response.data


def test_user_login(client):
    user = User(username='testuser', email='test@example.com',
                password='testpassword')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 302  # Expect redirect after login
    # After login, user should be redirected to the dashboard
    assert b'Dashboard' in response.data
