import os


class Config:
    """
    Configuration base, for all environments.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///yourdatabase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'noreply@example.com'

    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    REMEMBER_COOKIE_DURATION = 3600

    OAUTH2_REFRESH_TOKEN_GENERATOR = True

    ITEMS_PER_PAGE = 10
