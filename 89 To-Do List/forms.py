from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, EmailField, PasswordField
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


class ThemeColorForm(FlaskForm):
    theme = SelectField('Theme Color', choices=[(None, 'Default'), ('flatly', 'Flatly'), (
        'minty', 'Minty'), ('sandstone', 'Sandstone'), ('litera', 'Litera')])
    submit = SubmitField('Change Theme')
