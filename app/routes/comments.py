from flask import Blueprint, request
from ..models import db, Comment
from ..util import token_required

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
                    'commenter': comment.commenter.username,
                    'commenterAvi': comment.commenter.avatarUrl,
                    'body': comment.body,
                    'timestamp': comment.timestamp
                }
            }
        else:
            returnDict[comment.post_id][comment.id] = {
                'commenter': comment.commenter.username,
                'commenterAvi': comment.commenter.avatarUrl,
                'body': comment.body,
                'timestamp': comment.timestamp
            }
    # print(returnDict)
    return returnDict


@bp.route('/<int:postId>', methods=['POST'])
@token_required
def addComment(current_user, postId):
    data = request.json
    # print(data)
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
            'commenterAvi': comment.commenter.avatarUrl,
            'body': comment.body,
            'timestamp': comment.timestamp,
        }) for comment in comments)
    # print(returnDict)
    return returnDict


@bp.route('/<int:postId>', methods=['DELETE'])
@token_required
def addComment(current_user, postId):
    data = request.json
    Comment.query.filter(Comment.id).first()
    # print(data)
    # newComment = Comment(
    #     post_id=postId,
    #     commenter=current_user,
    #     body=data['commentBody'],
    # )
    # db.session.add(newComment)
    # db.session.commit()
    # comments = Comment.query.filter(Comment.post_id == postId).all()
    # returnDict = dict((comment.id, {
    #     'commenter': comment.commenter.username,
    #     'commenterAvi': comment.commenter.avatarUrl,
    #     'body': comment.body,
    #     'timestamp': comment.timestamp,
    # }) for comment in comments)
    # # print(returnDict)
    # return returnDict
