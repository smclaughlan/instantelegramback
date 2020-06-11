from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Configuration
<<<<<<< HEAD
from .routes import comments, follows, session, likes, posts, users
=======
from .routes import session, likes, posts, users
>>>>>>> master
from .models import db

app = Flask(__name__)
CORS(app)
app.config.from_object(Configuration)
app.register_blueprint(session.bp)
app.register_blueprint(posts.bp)
app.register_blueprint(likes.bp)
app.register_blueprint(users.bp)
app.register_blueprint(comments.bp)
db.init_app(app)
Migrate(app, db)
