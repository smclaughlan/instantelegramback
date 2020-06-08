from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    bio = db.Column(db.String(100), default="", nullable=False)

    user_flwr = db.relationship("Follow", back_populates="follower")
    user_flwd = db.relationship("Follow", back_populates="followed")
    user_pstr = db.relationship("Post", back_populates="poster")
    user_cmntr = db.relationship("Comment", back_populates="commenter")
    user_liker = db.relationship("PostLike", back_populates="post_liker")
    user_liker_c = db.relationship("CommentLike", back_populates="comment_liker")

    @property
    def password(self):
        return hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Follow(db.Model):
    __tablename__ = "follows"
    id = db.Column(db.Integer, primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    __table_args__ = (db.UniqueConstraint('followed_id', 'follower_id'))


    # possibly different syntax?
    follower = db.relationship("User", back_populates="user_flwr")
    followed = db.relationship("User", back_populates="user_flwd")


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False)
    caption = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    poster = db.relationship("User", back_populates="user_pstr")

    comment = db.relationship("Post", back_populates="post_cmnt")
    like_post = db.relationship("PostLike", back_populates="post_liked")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text, nullable=False)

    post_cmnt = db.relationship("Post", back_populates="comment")
    commenter = db.relationship("User", back_populates="user_cmntr")

    like_comment = db.relationship("CommentLike", back_populates="comment_liked")


class PostLike(db.Model):
    __tablename__ = "postlikes"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id'))

    post_liked = db.relationship("Post", back_populates="like_post")
    post_liker = db.relationship("User", back_populates="user_liker")


class CommentLike(db.Model):
    __tablename__ = "commentlikes"
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    __table_args__ = (db.UniqueConstraint('comment_id', 'user_id'))

    comment_liked = db.relationship("Comment", back_populates="like_comment")
    comment_liker = db.relationship("User", back_populates="user_liker_c")
