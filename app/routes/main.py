from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import GameLog, Game
from app import db
from app.forms import NewGameForm
from app.forms import GameForm


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required 
def dashboard():
    gamelogs = GameLog.query.filter_by(user_id=current_user.id).all()
    print(f"Found {len(gamelogs)} gamelogs for user {current_user.username}")
    for g in gamelogs:
        print(g.game.title, g.status)

    all_logs = GameLog.query.all()
    print(f"Total gamelogs: {len(all_logs)}")

    user_logs = GameLog.query.filter_by(user_id=current_user.id).all()
    print(f"Gamelogs for user {current_user.username} ({current_user.id}): {len(user_logs)}")

    return render_template('dashboard.html', gamelogs=gamelogs)

@main_bp.route('/games/new', methods=['GET', 'POST'])
@login_required
def new_game():
    form = GameForm()
    if form.validate_on_submit():
        game = Game(
            title=form.title.data,
            genre=form.genre.data,
            platform=form.platform.data,
            description=form.description.data,
            cozy_elements=form.cozy_elements.data,
            image_url=form.image_url.data,
            user_id=current_user.id
        )
        db.session.add(game)
        db.session.commit()  

        gamelog = GameLog(
            user_id=current_user.id,
            game_id=game.id,
            status='Playing'  # or default status you want
        )
        db.session.add(gamelog)
        db.session.commit()

        flash('Game added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('games/new_game.html', form=form)
