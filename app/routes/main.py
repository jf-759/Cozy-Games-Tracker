from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import GameLog, Game
from app import db
from app.forms import NewGameForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required 
def dashboard():
    gamelogs = GameLog.query.filter_by(user_id=current_user.id).all()
    print(f"Found {len(gamelogs)} gamelogs for user {current_user.username}")
    for g in gamelogs:
        print(g.game.title, g.status)
    return render_template('dashboard.html', gamelogs=gamelogs)

@main_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_game():
    form = NewGameForm()
    if form.validate_on_submit():
        game = Game(
            title=form.title.data,
            genre=form.genre.data,
            platform=form.platform.data,
            description=form.description.data,
            cozy_elements=form.cozy_elements.data,
            image_url=form.image_url.data
        )
        db.session.add(game)
        db.session.commit()

        # 🔥 Add this GameLog entry
        log = GameLog(user_id=current_user.id, game_id=game.id, status=form.status.data)
        db.session.add(log)
        db.session.commit()

        flash('Game added successfully!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('new_game.html', form=form)
