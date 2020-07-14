from flask import Blueprint, request
from sqlalchemy import update, and_, desc
from app.models import User, Follow, Post, db


from ..config import Configuration
from ..util import token_required

bp = Blueprint('users', __name__, url_prefix='/users')

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

@bp.route("/<int:userId>", methods=["PUT"])
def putUser(userId):

    user = User.query.filter(User.id == userId).first()
    reqData = request.json

    if 'avatar' in reqData:
        user.avatarUrl = reqData['avatar']
    if 'bio' in reqData:
        user.bio = reqData['bio']
    db.session.commit()
    return "Updated"

@bp.route("/<int:followedId>/follow", methods=["POST"])
def followeReq(followedId):
    reqData = request.json
    newFollow = Follow()
    newFollow.followed_id = followedId
    newFollow.follower_id = reqData['userId']
    db.session.add(newFollow)
    db.session.commit()
    return "New followe added"


@bp.route("/<int:followedId>/follow", methods=["DELETE"])
def unfolloweReq(followedId):
    reqData = request.json

    delFollow = Follow.query.filter(and_(Follow.follower_id == int(reqData['userId']), Follow.followed_id == followedId)).first()

    db.session.delete(delFollow)
    db.session.commit()
    return "Follow removed"


@bp.route("/<int:followedId>/followings")
def followings(followedId):
    followings = Follow.query.filter(Follow.follower_id == followedId).all()
    returnFollowings =  dict((following.id, {'followingId': following.followed_id}) for following in followings)
    return returnFollowings


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
    'user_id': post.user_id,
    'timestamp': post.timestamp,
    }) for post in posts)

  return returnPosts
