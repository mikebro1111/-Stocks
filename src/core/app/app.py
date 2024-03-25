from flask import Flask
from models.models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

if __name__ == '__main__':
    """
    Run web-application
    """
    app.run(debug=True)
