import pytest
from app import app, db
from flask import json
from flask_login import login_user
from flask_app.models import User, Role
from werkzeug.security import generate_password_hash, check_password_hash

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
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    # Expecting a JSON response with a success message
    assert response.status_code == 201  # Created status code
    response_json = json.loads(response.data)
    assert response_json['message'] == "User registered successfully!"  # Check the success message

# Test user login
def test_login(client):
    user = User(username='testuser', email='test@example.com', password=generate_password_hash('testpassword', method='sha256'))

    with app.app_context():
        db.session.add(user)
        db.session.commit()
        user = db.session.query(User).filter_by(id=user.id).first()

    # Now attempt to login
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    # Check that login succeeded (expecting a 200 status code)
    assert response.status_code == 200  # Expecting a success message in JSON

    # Check if the response contains the login success message
    response_json = json.loads(response.data)
    assert response_json['message'] == "Login successful!"  # Check the success message
    assert 'user_id' in response_json  # Ensure user ID is returned

# Test if the user is correctly assigned a role
def test_assign_role(client):
    # Create a new user and add to DB
    user = User(username='testuser', email='test@example.com', password=generate_password_hash('testpassword', method='sha256'))

    with app.app_context():  # Ensure DB interaction is done within app context
        db.session.add(user)
        db.session.commit()

        # Create a role for this user
        role = Role(role_name='Admin', user_id=user.id)
        db.session.add(role)
        db.session.commit()

    # Now simulate user login
    login_user(user)

    # Test the role assignment
    response = client.post('/assign_role', json={
        'user_id': user.id,
        'role_name': 'Admin'
    })

    # Check for successful role assignment (expecting status 200)
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json['message'] == "Role 'Admin' assigned to user successfully!"  # Check the success message

    # Ensure role assignment in the DB
    assigned_role = db.session.query(Role).filter_by(user_id=user.id).first()
    assert assigned_role.role_name == 'Admin'  # Check if the role is correctly assigned

# Test changing user's password
def test_change_password(client):
    user = User(username='testuser', email='test@example.com', password=generate_password_hash('testpassword', method='sha256'))

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # Now login user
    login_user(user)

    # Test password change
    response = client.post('/change_password', json={
        'new_password': 'newpassword'
    })

    # Check for successful password change (expecting status 200)
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert response_json['message'] == "Password updated successfully!"  # Check the success message

    # Ensure password was updated in the database
    user = db.session.query(User).filter_by(id=user.id).first()
    assert check_password_hash(user.password, 'newpassword')  # Verify the password hash is updated

