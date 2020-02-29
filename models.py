"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    first_name = db.Column(
        db.Text,
        nullable=False)
    last_name = db.Column(
        db.Text,
        nullable=False)
    image_url = db.Column(
        db.Text,
        nullable=False)
    post = db.relationship('Post', backref='users')



class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True)
    title = db.Column(
        db.Text,
        nullable=False)
    content = db.Column(
        db.Text,
        nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.now())
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'))


class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True)
    name = db.Column(
        db.Text,
        unique=True)
    posts = db.relationship('Post',secondary='posttags',backref='tags')
    
class PostTag(db.Model):
    """PostTag."""

    __tablename__ = "posttags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'), 
        primary_key=True)

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'), 
        primary_key=True)
