from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField, URLField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Email


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    url = URLField(validators=[URL()])
    open_time = TimeField()
    close_time = TimeField()
    coffee_rating = SelectField(
        choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'])
    wifi_rating = SelectField(
        choices=['❌', '🛜', '🛜🛜', '🛜🛜🛜', '🛜🛜🛜🛜', '🛜🛜🛜🛜🛜'])
    outlet_rating = SelectField(
        choices=['❌', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Register')
