from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#generates a users table with id, avatarUrl, username, hashed_password,
#email and bio
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    avatarUrl = db.Column(db.Text, default="https://res.cloudinary.com/dgzcv1mcs/image/upload/v1589817904/bw2djxdddpa1mjpshity.jpg")
    username = db.Column(db.String(20), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    bio = db.Column(db.String(100), default="", nullable=False)

    #a user could have many followings and many followers
    followings = db.relationship("Follow", back_populates="followed", foreign_keys='Follow.followed_id')
    followers = db.relationship("Follow", back_populates="follower", foreign_keys='Follow.follower_id')
    #a user could have many posts, comments 
    user_pstr = db.relationship("Post", back_populates="poster")
    user_cmntr = db.relationship("Comment", back_populates="commenter")
    #a user could have only one like for a comment or/and post
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

#generates a follows table with id, followed_id and follower_id 
class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #making sure (followed_id, follower_id) are unique
    db.UniqueConstraint(followed_id, follower_id)

    follower = db.relationship("User", foreign_keys=[follower_id])
    followed = db.relationship("User", foreign_keys=[followed_id])

#generates a posts table wiht id, image, caption, user_id and time
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=False)
    caption = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    poster = db.relationship("User", back_populates="user_pstr")

    #a post could have many comments and/or many likes
    comment = db.relationship("Comment", back_populates="post_cmnt")
    like_post = db.relationship("PostLike", back_populates="post_liked")

#generate a comments table with id, post_id, user_id, body and time
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    #a comment belongs to only one post
    post_cmnt = db.relationship("Post", back_populates="comment")
    commenter = db.relationship("User", back_populates="user_cmntr")
 
    #a comment has many likes
    like_comment = db.relationship("CommentLike", back_populates="comment_liked")


#generates a postlikes table with id, post_id and user_id
class PostLike(db.Model):
    __tablename__ = "postlikes"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    db.UniqueConstraint(post_id, user_id)
    
    post_liked = db.relationship("Post", back_populates="like_post")
    post_liker = db.relationship("User", back_populates="user_liker")

#generates a commentlikes table with id, comment_id and user_id
class CommentLike(db.Model):
    __tablename__ = "commentlikes"

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    db.UniqueConstraint(comment_id, user_id)

    comment_liked = db.relationship("Comment", back_populates="like_comment")
    comment_liker = db.relationship("User", back_populates="user_liker_c")
