from flask import Blueprint
from ..models import db, User, Follow

bp = Blueprint("follow", __name__, url_prefix="/follow")


@bp.route("/test")
def testfollow():

    return 'test'
