from app import app, db
from flask_app.models import User, Role
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

# Test role assignment functionality
def test_assign_role(client):
    # Create a new user with a hashed password and add to DB
    user = User(
        username='testuser',
        email='test@example.com',
        password=generate_password_hash('testpassword', method='sha256')
    )

    with app.app_context():  # Ensure DB interaction is done within app context
        db.session.add(user)
        db.session.commit()

        # After committing, reload the user to ensure it's in the current session
        user = db.session.query(User).filter_by(id=user.id).first()

    # Simulate user login
    login_user(user)

    # Assign the 'admin' role to the user
    response = client.post('/assign_role', data={
        'user_id': user.id,
        'role_name': 'admin'
    })

    # Check if the role assignment was successful
    assert response.status_code == 200
    assert b"Role 'admin' assigned to user!" in response.data

    # Verify that the 'admin' role was added to the user
    role = Role.query.filter_by(role_name='admin').first()
    assert role is not None  # Ensure the role exists in the DB
    assert role.user_id == user.id  # Ensure the correct user is assigned the role
