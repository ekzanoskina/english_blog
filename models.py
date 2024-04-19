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
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)


    def __repr__(self):
        return f"User <{self.username}>"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)


    def __repr__(self):
        return f"Comment('{self.author}', '{self.text}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

# class User(UserMixin, db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(250), unique=True, nullable=False)
#     password = db.Column(db.String(250), nullable=False)
#     name = db.Column(db.String(250), nullable=False)
#     # back_populates "author" refers to the author property in the BlogPost class.
#     posts = relationship("BlogPost", back_populates="author")
#     comments = relationship("Comment", back_populates="comment_author")
#
#
# class BlogPost(db.Model):
#     __tablename__ = "blog_posts"
#     id = db.Column(db.Integer, primary_key=True)
#     # create foreign key, "user.id" the users refers to the table name of User
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     # create reference to the User object, the "posts" refers to the posts property in tht User class.
#     author = relationship("User", back_populates="posts")
#
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     subtitle = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     img_url = db.Column(db.String(250), nullable=False)
#
#     comments = relationship("Comment", back_populates="parent_post")
#
#
# class Comment(db.Model):
#     __tablename__ = "comments"
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     # "users.id" The users refers to the table name of the Users class.
#     # "comments" refers to the comments property in the User class.
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     comment_author = relationship("User", back_populates="comments")
#
#     blog_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
#     parent_post = relationship("BlogPost", back_populates="comments")
#
# # class User(db.Model):
# #     __tablename__ = 'users'
# #
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(80), unique=True, nullable=False)
# #     email = db.Column(db.String(120), unique=True, nullable=False)
# #     comments = db.relationship('Comment', backref='author', lazy=True)
# #
# #     def __repr__(self):
# #         return f'<User {self.username}>'
# #
# # class BlogPost(db.Model):
# #     __tablename__ = 'blog_posts'
# #
# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String(100), nullable=False)
# #     body = db.Column(db.Text, nullable=False)
# #     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# #     comments = db.relationship('Comment', backref='blog_post', lazy=True)
# #
# #     def __repr__(self):
# #         return f'<BlogPost {self.title}>'
# #
# # class Comment(db.Model):
# #     __tablename__ = 'comments'
# #
# #     id = db.Column(db.Integer, primary_key=True)
# #     body = db.Column(db.Text, nullable=False)
# #     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     blog_post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
# #
# #     def __repr__(self):
# #         return f'<Comment {self.body}>'