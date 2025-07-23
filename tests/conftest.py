import pytest
from app import app, db  # Assuming the app is in the 'app.py' file

@pytest.fixture
def client():
    """Fixture for the test client."""
    with app.test_client() as client:
        with app.app_context():  # Ensures the app context is pushed
            db.create_all()  # You can create your DB tables here if needed
        yield client
    with app.app_context():
        db.session.remove()  # Clean up after each test
        db.drop_all()  # Drop tables if necessary
