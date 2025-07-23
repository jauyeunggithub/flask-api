import pytest
from app import app, db
from flask import json
from flask_login import login_user
from flask_app.models import User, Role

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
    user = User(username='testuser', email='test@example.com', password='testpassword')

    with app.app_context():  # Ensure we're in the app context for DB operations
        db.session.add(user)
        db.session.commit()  # Commit the user to the database

    # Now attempt to login
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    # Check that login succeeded (expecting a 200 or redirect)
    assert response.status_code == 200  # Adjust this as per your app's response code

    # Optionally check if user was logged in (e.g., check for user ID in the session or some user-specific data)
    assert b'Logout' in response.data  # Or check something else to confirm user is logged in
