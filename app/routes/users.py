from flask import Blueprint, request
from sqlalchemy import update, and_
from app.models import User, Follow, db

from ..config import Configuration
from ..util import token_required

bp = Blueprint('users', __name__, url_prefix='/api/users')

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
  # print(request.json)
  user = User.query.filter(User.id == userId).first()
  reqData = request.json
  # print(dir(reqData))
  # print(dir(user))
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
    print(reqData)
    print(followedId)
    delFollow = Follow.query.filter(and_(Follow.follower_id==int(reqData['userId']), Follow.followed_id==followedId)).first()
    print(delFollow)
    db.session.delete(delFollow)
    db.session.commit()
    return "Follow removed"
