from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models import User, db
from sqlalchemy.exc import SQLAlchemyError
import jwt
from ..config import Configuration
from ..util import token_required

bp = Blueprint('session', __name__, url_prefix='/session')

#create a new user and sends back a token and currentUserId
@bp.route('/register', methods=['POST'])
def register_user():
    data = request.json

    hashed_password = generate_password_hash(data['hashed_password'])
    new_user = User(username=data['username'],
                    email=data['email'],
                    hashed_password=hashed_password,
                    bio=data['bio']
                    )
    try:
        db.session.add(new_user)
        db.session.commit()
        token = jwt.encode({'user_id': new_user.id}, Configuration.SECRET_KEY).decode('utf-8')
        return {
            'token': token,
            'currentUserId': new_user.id,
        }
    except SQLAlchemyError as e:
        db.session.rollback()
        error = str(e.__dict__['orig'])
        return { 'error': error }, 401


# Given a particular user's username and password, checks to see if the credentials
# match what is stored in the database
#if not sends back a 401 status
@bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = jwt.encode({'user_id': user.id}, Configuration.SECRET_KEY).decode('utf-8')
        return {
            'token': token,
            'currentUserId': user.id,
        }
    else:
        return {'message': 'Invalid credentials'}, 401


@bp.route('/auth')
@token_required
def check_auth(current_user):
    return {'message': 'User is authorized!', 'user_id': current_user.id}
