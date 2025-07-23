from app import app, db
from flask_app.models import User, Role
from flask_login import login_user
import pytest

# Test role assignment functionality


def test_assign_role(client):
    user = User(username='testuser', email='test@example.com',
                password='testpassword')
    db.session.add(user)
    db.session.commit()

    # Simulate login
    login_user(user)

    response = client.post('/assign_role', data={
        'user_id': user.id,
        'role_name': 'admin'
    })
    assert response.status_code == 200
    assert b"Role 'admin' assigned to user!" in response.data

    # Verify role was added to the user
    role = Role.query.filter_by(role_name='admin').first()
    assert role is not None
    assert role.user_id == user.id
