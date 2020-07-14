from flask import Blueprint, request
from werkzeug.security import generate_password_hash
from app.models import User, db
import jwt
from ..config import Configuration
from ..util import token_required

bp = Blueprint('session', __name__, url_prefix='/session')


@bp.route('/register', methods=['POST'])
def register_user():
    data = request.json

    hashed_password = generate_password_hash(data['hashed_password'])
    new_user = User(username=data['username'],
                    email=data['email'],
                    hashed_password=hashed_password,
                    bio=data['bio']
                    )
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({'user_id': new_user.id}, Configuration.SECRET_KEY)
    return {
        'token': token.decode('UTF-8'),
        'currentUserId': new_user.id,
        }


@bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user.check_password(data['password']):
        token = jwt.encode({'user_id': user.id}, Configuration.SECRET_KEY)
        return {
            'token': token.decode('UTF-8'),
            'currentUserId': user.id,
        }
    else:
        return {'message': 'Invalid credentials'}, 401


@bp.route('/auth')
@token_required
def check_auth(current_user):
    return {'message': 'User is authorized!', 'user_id': current_user.id}
