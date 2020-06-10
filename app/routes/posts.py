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
