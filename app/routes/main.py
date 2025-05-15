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
            status='Playing'
        )
        db.session.add(gamelog)
        db.session.commit()

        flash('Game added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('games/new_game.html', form=form)

@main_bp.route('/games/<int:id>')
@login_required
def game_detail(id):
    gamelog = GameLog.query.filter_by(game_id=id, user_id=current_user.id).first()
    if not gamelog:
        flash('Game not found or not authorized to view.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    game = gamelog.game
    status = gamelog.status
    return render_template('games/game_detail.html', game=game, gamelog=gamelog, status=status)

@main_bp.route('/games/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_game(id):
    game = Game.query.get_or_404(id)
    gamelog = GameLog.query.filter_by(game_id=id, user_id=current_user.id).first()

    if game.user_id != current_user.id:
        flash("You are not authorized to edit this game.", "danger")
        return redirect(url_for('main.dashboard'))

    form = GameForm(obj=game)
    
    if gamelog and hasattr(form, 'status') and request.method == 'GET':
        form.status.data = gamelog.status
    
    if form.validate_on_submit():
        game.title = form.title.data
        game.genre = form.genre.data
        game.platform = form.platform.data
        game.description = form.description.data
        game.cozy_elements = form.cozy_elements.data
        game.image_url = form.image_url.data

        if gamelog and hasattr(form, 'status'):
            gamelog.status = form.status.data

        db.session.commit()
        flash("Game updated successfully!", "success")
        return redirect(url_for('main.game_detail', id=game.id))
    else:
        if form.is_submitted():
            flash(f"Form validation errors: {form.errors}", "danger")

    return render_template('games/edit_game.html', form=form, game=game, gamelog=gamelog)

@main_bp.route('/games/<int:id>/delete', methods=['POST'])
@login_required
def delete_game(id):
    game = Game.query.get_or_404(id)

    if game.user_id != current_user.id:
        flash("You do not have permission to delete this game.", "danger")
        return redirect(url_for('main.dashboard'))

    db.session.delete(game)
    db.session.commit()
    flash("Game deleted successfully!", "success")
    return redirect(url_for('main.dashboard'))
