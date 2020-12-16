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

    # validations
    # TODO: move these to a decorator function in util.py
    if len(data['username']) > 20:
        return {'error': 'please choose a username with under 20 characters'}, 400

    username_check = User.query.filter(User.username == data['username']).first()
    email_check = User.query.filter(User.email == data['email']).first()
    if username_check:
        return {'error': f'username {username_check.username} is already taken'}, 400
    if email_check:
        return {'error': f'email {email_check.email} is already taken'}, 400

    # creation of a new user
    new_user = User(username=data['username'],
                    email=data['email'],
                    hashed_password=hashed_password,
                    bio=data['bio']
                    )
    try:
        db.session.add(new_user)
        db.session.commit()
        token = jwt.encode({'user_id': new_user.id}, Configuration.SECRET_KEY)
        return {
            'token': token.decode('UTF-8'),
            'currentUserId': new_user.id,
        }
    except SQLAlchemyError as e:
        db.session.rollback()
        error = str(e.__dict__['orig'])
        return { 'error': error }, 400


# Given a particular user's username and password, checks to see if the credentials
# match what is stored in the database
#if not sends back a 401 status
@bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = jwt.encode({'user_id': user.id}, Configuration.SECRET_KEY)
        return {
            'token': token.decode('UTF-8'),
            'currentUserId': user.id,
        }
    else:
        if user:
            return {'message': 'Invalid password'}, 401
        else:
            return {'message': 'Invalid username'}, 401


@bp.route('/auth')
@token_required
def check_auth(current_user):
    return {'message': 'User is authorized!', 'user_id': current_user.id}
