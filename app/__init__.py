from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
login = LoginManager()
moment = Moment()

if os.environ.get('FlASK_DEBUG'):
    cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    login.login_view = 'pokemon.login'
    login.login_message = 'You need to login.'
    login.login_message_category = 'danger'

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.pokemon import bp as pokemon_bp
    app.register_blueprint(pokemon_bp)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html.j2')


    return app

from app import models
