from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class GameForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = StringField('Genre')
    platform = StringField('Platform')
    status = SelectField('Status', choices=[('Backlog', 'Backlog'), ('Playing', 'Playing'), ('Completed', 'Completed')])
    submit = SubmitField('Add Game')

class ReviewForm(FlaskForm):
    content = TextAreaField('Review', validators=[DataRequired()])
    rating = IntegerField('Rating (1–10)', validators=[DataRequired()])
    submit = SubmitField('Submit Review')
