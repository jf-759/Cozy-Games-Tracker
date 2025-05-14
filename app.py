from app import create_app
from flask_login import LoginManager
from app.models import User

app = create_app()
login_manager = app.login_manager


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)
