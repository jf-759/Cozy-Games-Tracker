from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class GameForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre')
    platform = StringField('Platform')
    description = TextAreaField('Description')
    cozy_elements = TextAreaField('Cozy Elements')
    image_url = StringField('Image URL')
    status = SelectField('Status', choices=[('Backlog', 'Backlog'), ('Playing', 'Playing'), ('Completed', 'Completed')])
    submit = SubmitField('Add Game')

class ReviewForm(FlaskForm):
    content = TextAreaField('Review', validators=[DataRequired()])
    rating = IntegerField('Rating (1–10)', validators=[DataRequired()])
    submit = SubmitField('Submit Review')

class NewGameForm(FlaskForm):
    title = StringField(' Game Title', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Wishlist', 'Wishlist'), ('Playing', 'Playing'), ('Completed', 'Completed')], validators=[DataRequired()])
    genre = StringField('Genre')
    platform = StringField('Platform')
    description = TextAreaField('Description')
    cozy_elements = StringField('Cozy Elements')
    image_url = StringField('Image URL')
    submit = SubmitField('Add Game')