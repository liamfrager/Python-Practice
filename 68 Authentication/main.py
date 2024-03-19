from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
login_manager = LoginManager(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE IN DB
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    user = db.session.execute(
        db.select(User).where(User.id == user_id)).scalar()
    return user


# ROUTES
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        try:
            with app.app_context():
                new_user = User(
                    email=request.form['email'],
                    password=generate_password_hash(
                        password=request.form['password'],
                        method='pbkdf2:sha256',
                        salt_length=8
                    ),
                    name=request.form['name'],
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            return redirect(url_for('secrets'))
        except IntegrityError:
            flash('User already exists with that email.')
            return render_template("register.html", form_data=request.form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('secrets'))
        else:
            return render_template("login.html")
    elif request.method == "POST":
        with app.app_context():
            user = db.session.execute(
                db.select(User).where(User.email == request.form['email'])).scalar()
            if check_password_hash(user.password, request.form['password']):
                login_user(user)
                return redirect(url_for('secrets'))
            else:
                flash('Incorrect login.')
                return render_template("login.html", form_data=request.form)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', 'files/cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True, port=4000)
