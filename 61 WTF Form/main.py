from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
boostrap = Bootstrap5(app)
app.secret_key = "shhhSECRETS"


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=8)])
    submit = SubmitField("Login")


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        pw = form.password.data
        if email == "admin@email.com" and pw == "12345678":
            return render_template('success.html')
        else:
            return render_template('denied.html')
    else:
        return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
