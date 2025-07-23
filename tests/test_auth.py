from app import app, db
from flask_app.models import User
from flask_login import login_user
import pytest
from werkzeug.security import generate_password_hash

# Setup the test client and ensure database context is handled
@pytest.fixture
def client():
    with app.app_context():  # Ensure we're within the app context
        with app.test_client() as client:
            db.create_all()  # Set up the database before the test
            yield client  # Provide the client for the test to use
            db.session.remove()  # Clean up after test
            db.drop_all()  # Drop all tables after the test

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
    # First, create the user in the database with a hashed password
    user = User(
        username='testuser',
        email='test@example.com',
        password=generate_password_hash('testpassword', method='sha256')
    )

    with app.app_context():  # Ensure DB interaction is done within the app context
        db.session.add(user)
        db.session.commit()  # Commit the user to the database

        # After committing, reload the user to ensure it's in the current session
        user = db.session.query(User).filter_by(id=user.id).first()

    # Now attempt to log in with the created user
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    # Expect a redirect (status code 302) after a successful login
    assert response.status_code == 302  # 302 indicates a redirect

    # After login, user should be redirected to the dashboard or home page
    assert b'Dashboard' in response.data  # Adjust based on your actual dashboard route content
