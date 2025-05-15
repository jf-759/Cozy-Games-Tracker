from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# User model
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    games = db.relationship('Game', back_populates='user', cascade="all, delete-orphan")
    gamelogs = db.relationship('GameLog', back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Load user for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Game model
class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    platform = db.Column(db.String(50))
    description = db.Column(db.Text)
    cozy_elements = db.Column(db.String(200))
    image_url = db.Column(db.String(255))

    gamelogs = db.relationship('GameLog', back_populates='game', cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='games')

# GameLog model 
class GameLog(db.Model):
    __tablename__ = "gamelogs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    status = db.Column(db.String(20))  
    notes = db.Column(db.Text)
    rating = db.Column(db.Integer) 

    user = db.relationship('User', back_populates='gamelogs')
    game = db.relationship('Game', back_populates='gamelogs')