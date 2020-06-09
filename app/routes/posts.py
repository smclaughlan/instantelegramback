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
    return {'you just posted!'}
