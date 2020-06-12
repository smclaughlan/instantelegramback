from flask import Blueprint, request
from sqlalchemy import and_
from ..models import db, Comment
from ..util import token_required

bp = Blueprint("comments", __name__, url_prefix="/comments")


@bp.route('/')
def getComments():
    comments = list(Comment.query.all())
    returnDict = dict()
    for comment in comments:
        if comment.post_id not in returnDict:
            returnDict[comment.post_id] = {
                comment.id: {
                    'commenter': comment.commenter.username,
                    'commenterId': comment.commenter.id,
                    'commenterAvi': comment.commenter.avatarUrl,
                    'body': comment.body,
                    'timestamp': comment.timestamp
                }
            }
        else:
            returnDict[comment.post_id][comment.id] = {
                'commenter': comment.commenter.username,
                'commenterId': comment.commenter.id,
                'commenterAvi': comment.commenter.avatarUrl,
                'body': comment.body,
                'timestamp': comment.timestamp
            }
    return returnDict


@bp.route('/<int:postId>', methods=['POST'])
@token_required
def addComment(current_user, postId):
    data = request.json
    newComment = Comment(
        post_id=postId,
        commenter=current_user,
        body=data['commentBody'],
    )
    db.session.add(newComment)
    db.session.commit()
    comments = Comment.query.filter(Comment.post_id == postId).all()
    returnDict = dict((comment.id, {
            'commenter': comment.commenter.username,
            'commenterId': comment.commenter.id,
            'commenterAvi': comment.commenter.avatarUrl,
            'body': comment.body,
            'timestamp': comment.timestamp,
        }) for comment in comments)
    return returnDict


@bp.route('/<int:commentId>', methods=['DELETE'])
@token_required
def deleteComment(current_user, commentId):
    data = request.json
    postId = data['postId']
    db.session.query(Comment).filter(and_((Comment.id == commentId), (Comment.commenter == current_user))).delete()
    db.session.commit()
    comments = Comment.query.filter(Comment.post_id == postId).all()
    returnDict = dict((comment.id, {
            'commenter': comment.commenter.username,
            'commenterId': comment.commenter.id,
            'commenterAvi': comment.commenter.avatarUrl,
            'body': comment.body,
            'timestamp': comment.timestamp,
        }) for comment in comments)
    return returnDict
