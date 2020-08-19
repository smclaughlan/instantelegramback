from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Configuration
from .routes import comments, session, likes, posts, users, search, status
from .models import db

app = Flask(__name__)
CORS(app)
app.config.from_object(Configuration)
app.register_blueprint(status.bp)
app.register_blueprint(session.bp)
app.register_blueprint(posts.bp)
app.register_blueprint(likes.bp)
app.register_blueprint(users.bp)
app.register_blueprint(comments.bp)
app.register_blueprint(search.bp)
db.init_app(app)
Migrate(app, db)