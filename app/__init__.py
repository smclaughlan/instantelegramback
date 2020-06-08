from flask import Flask
from flask_migrate import Migrate
from .config import Configuration
from .routes import follows, session
from .models import db

app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(follows.bp)
app.register_blueprint(session.bp)
db.init_app(app)
Migrate(app, db)
