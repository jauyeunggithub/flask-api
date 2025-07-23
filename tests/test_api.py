import pytest
from app import app, db
from flask import json
from flask_login import login_user
from flask_app.models import User, Role
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
    user = User(username='testuser', email='test@example.com', password=generate_password_hash('testpassword', method='sha256'))

    with app.app_context():  # Ensure we're in the app context for DB operations
        db.session.add(user)
        db.session.commit()  # Commit the user to the database

        # After committing, reload the user to ensure it's in the current session
        user = db.session.query(User).filter_by(id=user.id).first()

    # Now attempt to login
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    # Check that login succeeded (expecting a 200 or redirect)
    assert response.status_code == 302  # Expect a redirect (302) after login

    # Optionally check if user was logged in (e.g., check for user ID in the session or some user-specific data)
    assert b'Logout' in response.data  # Or check something else to confirm user is logged in

# Test if the user is correctly assigned a role
def test_assign_role(client):
    # Create a new user and add to DB
    user = User(username='testuser', email='test@example.com', password=generate_password_hash('testpassword', method='sha256'))

    with app.app_context():  # Ensure DB interaction is done within app context
        db.session.add(user)
        db.session.commit()

        # Create a role for this user (make sure Role model is set up correctly)
        role = Role(role_name='Admin', user_id=user.id)
        db.session.add(role)
        db.session.commit()

    # Now simulate user login
    login_user(user)

    # Test the role assignment (this could be a simple assertion to check role assignment)
    assigned_role = db.session.query(Role).filter_by(user_id=user.id).first()
    assert assigned_role.role_name == 'Admin'  # Check if the role is correctly assigned
