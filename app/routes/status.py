from flask import Blueprint


bp = Blueprint("status", __name__, url_prefix="/")

@bp.route('/')
def displayRunning():
    return 'Server is running!'