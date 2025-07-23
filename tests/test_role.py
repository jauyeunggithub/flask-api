from app import app, db
from flask_app.models import User, Role
from flask_login import login_user
import pytest

# Fixture to setup the test client and handle DB context
@pytest.fixture
def client():
    with app.app_context():  # Ensure the app context is available for DB interactions
        with app.test_client() as client:
            db.create_all()  # Create tables before each test
            yield client  # Provide the test client to the test
            db.session.remove()  # Remove the session to avoid lingering DB connections
            db.drop_all()  # Drop all tables after each test to clean up

# Test role assignment functionality
def test_assign_role(client):
    # Create a new user and add to DB
    user = User(username='testuser', email='test@example.com', password='testpassword')

    with app.app_context():  # Ensure DB interaction is done within app context
        db.session.add(user)
        db.session.commit()

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
