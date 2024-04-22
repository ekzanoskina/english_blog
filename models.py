import os
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

# create the extension
db = SQLAlchemy()

# CONFIGURE TABLES
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='profile.png')
    password = db.Column(db.String(60), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    def __repr__(self):
        return f"User <{self.username}>"

    @property
    def full_name(self):
        return f'{self.first_name.title()} {self.last_name.title()}'


categories = db.Table(
    "categories",
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    content = db.Column(db.Text, nullable=False)
    categories = db.relationship("Category", secondary=categories, backref="posts", lazy="select")
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)

    @property
    def description(self):
        truncate = lambda text, limit: text if len(text) <= limit else text[:limit - 3] + '...'
        return truncate(self.content, 120)

    @property
    def date_posted_str(self):
        return self.date_posted.strftime('%B %d, %Y')


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"{self.title.title()}"



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    @property
    def date_posted_str(self):
        return self.date_posted.strftime('%B %d, %Y')
    def __repr__(self):
        return f"Comment('{self.author}', '{self.text}')"



class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
