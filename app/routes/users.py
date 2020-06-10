from flask import Blueprint, request
from sqlalchemy import update
from app.models import User, db

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
  print(request.json)
  user = User.query.filter(User.id == userId).first()
  reqData = request.json
  print(dir(reqData))
  print(dir(user))
  # if 'avatar' in reqData:
    # user.avatarUrl = reqData.avatar
  # elif 'bio' in reqData:
#   updatedData = {
#   "id": user.id,
#   "username": user.username,
#   "email": user.email,
#   "bio": reqData["bio"],
#   "avatarUrl": user.avatarUrl,
#   }
  user.bio = reqData.data

#   user.update(**updatedData)

  # newUser = update(user).values(bio= reqData["bio"])

  db.session.commit()
  return "Test"
