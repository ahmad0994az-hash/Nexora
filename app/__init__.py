from flask import Flask

from .database import db
from .extensions import login_manager
from .routes import register_routes
from .auth import register_auth


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "nexora-secret"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nexora.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    register_auth(app)

    return app
