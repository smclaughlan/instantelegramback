from flask import Blueprint
from ..models import db, PostLike, Post

bp = Blueprint("likes", __name__, url_prefix="/likes")

#returns all likes
@bp.route('/')
def getLikes():
    likes = list(PostLike.query.all())
    returnDict = dict()
    for like in likes:
        if like.post_id not in returnDict:
            returnDict[like.post_id] = [like.user_id]
        else:
            returnDict[like.post_id].append(like.user_id)
    return returnDict
