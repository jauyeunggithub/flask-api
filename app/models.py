from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # Polymorphic relationship
    roles = db.relationship('Role', backref='user', lazy=True)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'notification',
        'polymorphic_on': 'type'
    }


class EmailNotification(Notification):
    __tablename__ = 'email_notifications'
    id = db.Column(db.Integer, db.ForeignKey(
        'notifications.id'), primary_key=True)
    email_subject = db.Column(db.String(150), nullable=False)
    email_body = db.Column(db.String(500), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'email'
    }
