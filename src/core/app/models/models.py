from flask_sqlalchemy import SQLAlchemy
from src.core.app.app import app

db = SQLAlchemy(app)


class User(db.Model):
    """
    User model for storing user details.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)


class OAuthClient(db.Model):
    """
    OAuthClient model for storing OAuth client details.
    """
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(120), unique=True, nullable=False)
    client_secret = db.Column(db.String(120), nullable=False)


class OAuthToken(db.Model):
    """
    OAuthToken model for storing OAuth tokens.
    """
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
