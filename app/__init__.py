import cloudinary
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Configuration
from .routes import comments, session, likes, posts, users, search, status
from .models import db

app = Flask(__name__)
CORS(app)
cloudinary.config(
            cloud_name = os.environ.get('CLOUD_NAME'),
            api_key = os.environ.get('API_KEY'),
            api_secret = os.environ.get('API_SECRET')
        )
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

@app.errorhandler(400)
def error_handler(e):
        return jsonify(message=str(e)), 400