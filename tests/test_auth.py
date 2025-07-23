from app import db
from flask_app.models import User
from flask_login import login_user, logout_user
import pytest

# Fixture to setup the test client
@pytest.fixture
def client():
    with app.app_context():  # Ensure app context for DB interactions
        with app.test_client() as client:
            db.create_all()  # Create the database tables before each test
            yield client  # Provide the test client
            db.session.remove()  # Remove any pending session data
            db.drop_all()  # Drop all tables after the test to clean up

# Test user registration
def test_user_registration(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    # Expect redirect after successful registration
    assert response.status_code == 302  # 302 indicates a redirect
    assert b'Login' in response.data  # Ensure the response contains 'Login'

# Test user login
def test_user_login(client):
    # First, create the user in the database
    user = User(username='testuser', email='test@example.com', password='testpassword')

    with app.app_context():  # Ensure DB interaction is done within the app context
        db.session.add(user)
        db.session.commit()  # Commit the user to the database

    # Now attempt to log in with the created user
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    # Expect a redirect (status code 302) after a successful login
    assert response.status_code == 302  # 302 indicates a redirect

    # After login, user should be redirected to the dashboard or home page
    assert b'Dashboard' in response.data  # Adjust based on your actual dashboard route content
