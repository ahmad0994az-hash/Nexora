from datetime import datetime

from flask_login import UserMixin

from .database import db
from .extensions import login_manager


class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    files = db.relationship(
        "File",
        backref="owner",
        lazy=True
    )


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


class File(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    token = db.Column(
        db.String(32),
        unique=True,
        nullable=False
    )

    original_name = db.Column(
        db.String(255),
        nullable=False
    )

    saved_name = db.Column(
        db.String(255),
        nullable=False
    )

    file_size = db.Column(
        db.Integer,
        default=0
    )

    downloads = db.Column(
        db.Integer,
        default=0
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<File {self.original_name}>"
