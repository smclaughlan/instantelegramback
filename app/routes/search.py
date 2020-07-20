from flask import Blueprint
from ..models import db, User

bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route('/')
def getUserIds():
    users = list(User.query.all())
    returnDict = dict((user.id, user.username) for user in users)
    return returnDict
