from flask import Blueprint, request
from sqlalchemy import and_
from app.models import Comment, Post, PostLike, db
from ..util import token_required

bp = Blueprint('posts', __name__, url_prefix='/posts')

#create a new post with image and caption, current user will be owner/poster
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

#updates a post caption, checks if the user matches the owner/poster
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

#deletes a particular post after deleting all likes and comments for the post
#checks if the user matches with the owner/poster
@bp.route('/<id>', methods=['DELETE'])
@token_required
def deletePost(current_user, id):
    #delete all the postlikes for that imageId
    delPostLikes = PostLike.query.filter(PostLike.post_id == id).delete()
    #delete all the comments for that imageId
    delComments = Comment.query.filter(Comment.post_id == id).delete()
   
    db.session.commit()

    post = Post.query.get(id)
    if not post:
        return {'message': 'you can\'t delete a post that doesn\'t exist!'}
    if post.user_id == current_user.id:
        db.session.query(Post).filter(Post.id == id).delete()
        db.session.commit()
        return {'message': 'you just deleted!'}
    return {'message': 'you can\'t delete this!'}

#returns all posts for a user
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

#add a new like to a particular post
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

#deletes a like for a particular post, checks if the current user matches the owner 
@bp.route('/<int:id>/likes', methods=["DELETE"])
@token_required
def deletelike(current_user, id):
    db.session.query(PostLike).filter(and_((PostLike.post_id == id), (PostLike.user_id == current_user.id))).delete()
    db.session.commit()
    likesList = list(PostLike.query.filter(PostLike.post_id == id).all())
    returnList = [like.user_id for like in likesList]
    return {"data": returnList}
