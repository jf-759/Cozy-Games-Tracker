from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.models import Game
from app import db

game_bp = Blueprint('game', __name__, url_prefix='/games')

@game_bp.route('/')
def list_games():
    games = Game.query.all()
    return render_template('games/list.html', games=games)

@game_bp.route('/add', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        platform = request.form['platform']
        description = request.form['description']
        cozy_elements = request.form['cozy_elements']
        image_url = request.form['image_url']

        new_game = Game(
            title=title,
            genre=genre,
            platform=platform,
            description=description,
            cozy_elements=cozy_elements,
            image_url=image_url
        )

        db.session.add(new_game)
        db.session.commit()
        flash('Game added successfully!')
        return redirect(url_for('game.list_games'))

    return render_template('games/add.html')
