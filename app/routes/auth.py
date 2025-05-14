from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, login_manager
from ..models import User
from ..forms import SignupForm, LoginForm
from flask import Blueprint
from app.forms import SignupForm  

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(
            username=form.username.data, 
            email=form.email.data,
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    # Check if the form is being submitted
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        print(f"Form submitted with username: {username}, password: {password}")  # Debugging print
        
        # Query the user by username
        user = User.query.filter_by(username=username).first()

        # If no user is found or password is incorrect
        if not user or not user.check_password(password):
            flash('Invalid credentials', 'danger')
            print(f"Invalid credentials for {username}")  # Debugging print
            return redirect(url_for('auth.login'))

        # If user found and password matches, log them in
        print(f"User found: {user.username}, logging in!")  # Debugging print
        login_user(user)
        flash('Login successful!', 'success')
        
        # Redirect to dashboard after successful login
        return redirect(url_for('main.dashboard'))
    
    # Debugging: If form is not submitted or fails validation
    print(f"Form errors: {form.errors}")  # Debugging print

    return render_template('login.html', form=form)





@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
