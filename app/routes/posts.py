from flask import Blueprint, request
from app.models import Post, db
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
    db.session.query(Post).filter(Post.id == id).update({Post.caption: data['caption']})
    db.session.commit()
    post = Post.query.get(id)
    post = {'id': post.id, 'image': post.image, 'caption': post.caption, 'user_id': post.user_id}
    return {'data': post}


@bp.route('/<id>', methods=['DELETE'])
@token_required
def deletePost(current_user, id):
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
    posts = Post.query.filter(Post.user_id == userId).all()
    returnList = []
    for post in posts:
        returnList.append({
            'id': post.id,
            'image': post.image,
            'caption': post.caption,
            'user_id': post.user_id
        })
    return {"posts": returnList}
