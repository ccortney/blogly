"""Models for Blogly."""
from enum import unique
from flask_sqlalchemy import SQLAlchemy
import datetime

from jinja2.runtime import unicode_join

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
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

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
        return f"<Post {p.user_id} {p.title} {p.content} {p.created_at}>"

class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    name = db.Column(db.String(50), nullable = False, unique = True)


    def __repr__(self):
        """Show information about tag"""
        t = self
        return f"<Tag {t.id} {t.name}>"

    posts = db.relationship('Post', secondary = "posts_tags", backref = 'tags')

class PostTag(db.Model):
    """Post/Tag."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)