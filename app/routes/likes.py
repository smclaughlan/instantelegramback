from flask import Blueprint
from ..models import db, PostLike, Post

bp = Blueprint("likes", __name__, url_prefix="/likes")


@bp.route('/')
def getLikes():
    likes = list(PostLike.query.all())
    # dict
    # if the likes.post_id not there, add
    # otherwise loop through like and set values
    returnDict = dict()
    for like in likes:
        if like.post_id not in returnDict:
            returnDict[like.post_id] = [like.user_id]
        else:
            returnDict[like.post_id].append(like.user_id)
    return returnDict
