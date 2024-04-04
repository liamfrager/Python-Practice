from sqlite3 import IntegrityError
from typing import List
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from forms import LoginForm, RegisterForm, CafeForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

# LOGIN MANAGEMENT
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    user = db.session.execute(
        db.select(User).where(User.id == user_id)).scalar()
    return user


@login_manager.unauthorized_handler
def error_401():
    return render_template('/pages/errors/401.html')

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe-wifi.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    cafes_added: Mapped[List["Cafe"]] = relationship(back_populates="added_by")


class Cafe(db.Model):
    __tablename__ = 'cafes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cafe: Mapped[str] = mapped_column(String(100), unique=True)
    url: Mapped[str] = mapped_column(String(100))
    open_time: Mapped[str] = mapped_column(String(1000))
    close_time: Mapped[str] = mapped_column(String(1000))
    coffee_rating: Mapped[int] = mapped_column(Integer)
    wifi_rating: Mapped[int] = mapped_column(Integer)
    outlet_rating: Mapped[int] = mapped_column(Integer)
    added_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    added_by: Mapped["User"] = relationship(back_populates="cafes_added")


with app.app_context():
    db.create_all()


# ROUTES
@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            user = db.session.execute(
                db.select(User).where(User.email == form.data['email'])).scalar()
            if check_password_hash(user.password, form.data['password']):
                login_user(user)
                return redirect(url_for('cafes'))
            else:
                flash('Incorrect login.')
                return render_template('pages/login.html', form=form)
    else:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return render_template('pages/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            with app.app_context():
                new_user = User(
                    email=form.data['email'],
                    password=generate_password_hash(
                        password=form.data['password'],
                        method='pbkdf2:sha256',
                        salt_length=8
                    ),
                    name=form.data['name'],
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
            return redirect(url_for('home'))
        except IntegrityError:
            flash('User already exists with that email.')
            return render_template('pages/register.html', form=form)
    else:
        return render_template('pages/register.html', form=form)


@app.route('/cafes')
def cafes():
    return render_template('pages/cafes.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    else:
        return render_template('pages/add.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=4000, debug=True)
