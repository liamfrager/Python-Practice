from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, URLField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(8)])
    submit = SubmitField('Register')
