from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cozygames.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.game import game_bp
    from app.routes.log import log_bp
    from app.routes.main import main_bp  # <-- Make sure this one exists!

    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(main_bp)  # <-- This handles the homepage

    return app
