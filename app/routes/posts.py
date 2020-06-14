from flask import Blueprint, request
from sqlalchemy import and_
from app.models import Comment, Post, PostLike, db
from ..util import token_required

bp = Blueprint('posts', __name__, url_prefix='/posts')


@bp.route('/', methods=['POST'])
@token_required
def post(current_user):
    data = request.json
    post = Post(
        image=data['imgUrl'],
        caption=data['caption'],
        poster=current_user,
    )
    db.session.add(post)
    db.session.commit()
    return {'message': 'you just posted!'}


@bp.route('/<id>', methods=['PUT'])
@token_required
def updateCaption(current_user, id):
    data = request.json
    db.session.query(Post).\
        filter(Post.id == id).\
        update({Post.caption: data['caption']})
    db.session.commit()
    post = Post.query.get(id)
    post = {
        'id': post.id,
        'image': post.image,
        'caption': post.caption,
        'user_id': post.user_id,
        'timestamp': post.timestamp
    }
    return post


@bp.route('/<id>', methods=['DELETE'])
@token_required
def deletePost(current_user, id):
    #delete all the postlikes for that imageId
    delPostLikes = PostLike.query.filter(PostLike.post_id == id).delete()
    #delete all the comments for that imageId
    delComments = Comment.query.filter(Comment.post_id == id).delete()
    # for like in delPostLikes:
    #     like.delete()
    # for comment in delComments:
    #     comment.delete()
    db.session.commit()

    post = Post.query.get(id)
    if not post:
        return {'message': 'you can\'t delete a post that doesn\'t exist!'}
    if post.user_id == current_user.id:
        db.session.query(Post).filter(Post.id == id).delete()
        db.session.commit()
        return {'message': 'you just deleted!'}
    return {'message': 'you can\'t delete this!'}


@bp.route('/<int:userId>')
def getPost(userId):
    posts = list(Post.query.filter(Post.user_id == userId).all())
    returnPosts = dict((post.id, {
        'imageUrl': post.image,
        'caption': post.caption,
        'user_id': post.user_id,
        'timestamp': post.timestamp,
        }) for post in posts)
    return returnPosts


@bp.route('/<int:id>/likes', methods=["POST"])
@token_required
def createlike(current_user, id):
    like = PostLike(
        post_liker=current_user,
        post_id=id,
    )
    db.session.add(like)
    db.session.commit()
    likesList = list(PostLike.query.filter(PostLike.post_id == id).all())
    returnList = [like.user_id for like in likesList]
    return {"data": returnList}


@bp.route('/<int:id>/likes', methods=["DELETE"])
@token_required
def deletelike(current_user, id):
    db.session.query(PostLike).filter(and_((PostLike.post_id == id), (PostLike.user_id == current_user.id))).delete()
    db.session.commit()
    likesList = list(PostLike.query.filter(PostLike.post_id == id).all())
    returnList = [like.user_id for like in likesList]
    return {"data": returnList}
