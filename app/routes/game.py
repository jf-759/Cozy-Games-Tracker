from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required  
from app.models import Game, GameLog
from app.forms import GameForm
from app import db

game_bp = Blueprint('game', __name__, url_prefix='/games')

@game_bp.route('/')
@login_required
def list_games():
    games = Game.query.filter_by(user_id=current_user.id).all()  
    return render_template('games/list.html', games=games)

@game_bp.route('/add', methods=['GET', 'POST'])
@login_required  
def add_game():
    form = GameForm()
    if form.validate_on_submit():
        new_game = Game(
            title=form.title.data,
            genre=form.genre.data,
            platform=form.platform.data,
            user_id=current_user.id
        )
        db.session.add(new_game)
        db.session.commit()

        new_log = GameLog(
            user_id=current_user.id,
            game_id=new_game.id,
            status=form.status.data,
            notes='',
            rating=0
        )
        db.session.add(new_log)
        db.session.commit()

        flash('Game added successfully!')
        return redirect(url_for('game.list_games'))

    return render_template('games/new_game.html', form=form)