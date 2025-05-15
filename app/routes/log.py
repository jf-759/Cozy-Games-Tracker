from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import GameLog, Game
from app import db

log_bp = Blueprint('log', __name__, url_prefix='/log')

@log_bp.route('/')
@login_required
def view_logs():
    logs = GameLog.query.filter_by(user_id=current_user.id).all()
    return render_template('logs/list.html', logs=logs)


@log_bp.route('/add/<int:game_id>', methods=['GET', 'POST'])
@login_required
def add_log(game_id):
    game = Game.query.get_or_404(game_id)

    if request.method == 'POST':
        status = request.form['status']
        notes = request.form['notes']
        rating = int(request.form['rating'])

        new_log = GameLog(
            user_id=current_user.id,
            game_id=game.id,
            status=status,
            notes=notes,
            rating=rating
        )

        db.session.add(new_log)
        db.session.commit()
        flash('Game log added successfully!')
        return redirect(url_for('log.view_logs'))

    return render_template('logs/add.html', game=game)