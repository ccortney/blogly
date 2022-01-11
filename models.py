"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """connect this database to provided Flask app"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = True)
    image_url = db.Column(db.String, nullable = False, default = 'https://cvhrma.org/wp-content/uploads/2015/07/default-profile-photo.jpg')

    def __repr__(self):
        """Show information about user"""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}"

class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())

    users = db.relationship('User', backref = 'posts')

    def __repr__(self):
        """Show information about post"""
        p = self
        return f"<User {p.id} {p.title}"