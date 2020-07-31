from flask import Blueprint
from ..models import db, User

bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route('/')
def getUserIds():
    users = list(User.query.all())
    returnDict = dict((user.id, { 'username': user.username, 'avi': user.avatarUrl}) for user in users)
    return returnDict
