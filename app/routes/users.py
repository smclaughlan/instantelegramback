from flask import Blueprint, request
from app.models import User, db

from ..config import Configuration
from ..util import token_required

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route("/<int:userId>")
def getUser(userId):
  user = User.query.filter(User.id == userId).first()
  # user = user[0]
  print(user)
  print(type(user))
  print(user.__dict__)
  returnData = {
  "id": user.id,
  "username": user.username,
  "bio": user.bio}
  if user:
    return returnData
  else:
    return "Error"
