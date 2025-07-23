import pytest
from app import app, db
from flask_app.models import User
from flask_login import login_user
from werkzeug.security import generate_password_hash
from flask import json

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
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    # Expect a JSON response with a success message
    assert response.status_code == 201  # 201 indicates successful creation
    response_json = json.loads(response.data)
    assert response_json['message'] == "User registered successfully!"  # Check the success message

# Test user login
def test_user_login(client):
    # First, create the user in the database with a hashed password
    user = User(
        username='testuser',
        email='test@example.com',
        password=generate_password_hash('testpassword', method='sha256')
    )

    with app.app_context():  # Ensure DB interaction is done within app context
        db.session.add(user)
        db.session.commit()  # Commit the user to the database

        # After committing, reload the user to ensure it's in the current session
        user = db.session.query(User).filter_by(id=user.id).first()

    # Now attempt to log in with the created user
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    # Check if login was successful (status code 200 for success)
    assert response.status_code == 200

    # Parse the JSON response and check for success message
    response_json = json.loads(response.data)
    assert response_json['message'] == "Login successful!"  # Check the success message
    assert 'user_id' in response_json  # Ensure the user ID is returned in the response

    # You can also check for additional things (like checking if user is logged in by verifying session or cookies)

