from flask import Blueprint
from ..models import db, Comment

bp = Blueprint("comments", __name__, url_prefix="/comments")


@bp.route('/')
def getComments():
    comments = list(Comment.query.all())
    # dict
    # if the likes.post_id not there, add
    # otherwise loop through like and set values
    # returnDict = {
    #   post_id: {
    #     commment_id: {}
    #     comment
    # }
    # }
    returnDict = dict()
    for comment in comments:
        if comment.post_id not in returnDict:
            returnDict[comment.post_id] = {
                comment.id: {
                    'commenter': comment.user_id,
                    'body': comment.body,
                    'timestamp': comment.timestamp
                }
            }
        else:
            returnDict[comment.post_id][comment.id] = {
                'commenter': comment.user_id,
                'body': comment.body,
                'timestamp': comment.timestamp
            }
    print(returnDict)
    return {'message': 'you tried to get all the comments'}
