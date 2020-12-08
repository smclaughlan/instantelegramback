from flask import Blueprint, request
from sqlalchemy import update, and_, desc
from app.models import User, Follow, Post, db

from ..config import Configuration
from ..util import token_required

bp = Blueprint('users', __name__, url_prefix='/users')

#returns info for a particular user
@bp.route("/<int:userId>")
def getUser(userId):
  user = User.query.filter(User.id == userId).first()
  returnData = {
    "id": user.id,
    "username": user.username,
    "bio": user.bio,
    "avatarUrl": user.avatarUrl,
  }
  if user:
    return returnData
  else:
    return "Error"

#updates a user's avatar or/and bio
@bp.route("/<int:userId>", methods=["PUT"])
def putUser(userId):

    user = User.query.filter(User.id == userId).first()
    reqData = request.json
    if 'avatar' in reqData:
        user.avatarUrl = reqData['avatar']
    if 'bio' in reqData:
        user.bio = reqData['bio']
    db.session.commit()

    returnData = {
      "id": user.id,
      "username": user.username,
      "bio": user.bio,
      "avatarUrl": user.avatarUrl,
    }
    if user:
      return returnData
    else:
      return "Error"

#creates a new follow
@bp.route("/<int:followedId>/follow", methods=["POST"])
def followeReq(followedId):
    data = request.json
    followerId = int(data['userId'])
    newFollow = Follow(
      followed_id=followedId,
      follower_id=followerId,
    )
    db.session.add(newFollow)
    db.session.commit()

    followers = Follow.query.filter(Follow.followed_id == followedId).all()
    returnFollowers =  dict({'ids': [f.follower.id for f in followers]})
    return returnFollowers

#deletes a particular follow
@bp.route("/<int:followedId>/follow", methods=["DELETE"])
def unfolloweReq(followedId):
    reqData = request.json

    delFollow = Follow.query.filter(and_(Follow.follower_id == int(reqData['userId']), Follow.followed_id == followedId)).first()

    db.session.delete(delFollow)
    db.session.commit()

    followers = Follow.query.filter(Follow.followed_id == followedId).all()
    returnFollowers =  dict({'ids': [f.follower.id for f in followers]})
    return returnFollowers

#returns all the followers for a particular user
@bp.route("/<int:followedId>/followings")
def followings(followedId):
    followers = Follow.query.filter(Follow.followed_id == followedId).all()
    returnFollowers =  dict({'ids': [f.follower.id for f in followers]})
    return returnFollowers

#returns all posts for a feed page for a particular user
#start by getting all followings for the current user
#then gets all post for all followings including the current user
@bp.route("/<int:userId>/posts")
def feed_posts(userId):
  queryIds = [userId]
  followingIds = Follow.query.filter(Follow.follower_id==userId).all()
  for followingId in followingIds:
    queryIds.append(followingId.followed_id)
  posts = Post.query.filter(Post.user_id.in_(queryIds))

  returnPosts = dict((post.id, {
    'imageUrl': post.image,
    'caption': post.caption,
    'userId': post.user_id,
    'username': post.poster.username,
    'avatarUrl': post.poster.avatarUrl,
    'timestamp': post.timestamp,
    }) for post in posts)

  return returnPosts
