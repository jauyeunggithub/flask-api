from app import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# User model
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    roles = relationship('Role', back_populates='user', lazy='subquery')

    def __repr__(self):
        return f'<User {self.username}>'

# Role model
class Role(db.Model):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='roles')

    def __repr__(self):
        return f'<Role {self.role_name}>'

# Notification model
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    message = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'notification',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f'<Notification {self.message}>'

# EmailNotification inherits from Notification
class EmailNotification(Notification):
    __tablename__ = 'email_notifications'

    id = Column(Integer, ForeignKey('notifications.id'), primary_key=True)
    email_subject = Column(String(150), nullable=False)
    email_body = Column(String(500), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'email'
    }

    def __repr__(self):
        return f'<EmailNotification {self.email_subject}>'
