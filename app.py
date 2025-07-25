from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

# Initialize the extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

# Initialize the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

# Initialize the extensions with app
db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
migrate.init_app(app, db)

# Login manager configuration
login_manager.login_view = "auth.login"

# Import the routes at the end to avoid circular imports
from flask_app.routes import *

# Create all tables (optional, only needed once)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
