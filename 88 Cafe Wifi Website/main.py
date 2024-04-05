
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, RegisterForm, CafeForm
from db import db, db_func


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'flatly'
bootstrap = Bootstrap5(app)

# LOGIN MANAGEMENT
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return db_func.get_user(id=user_id)


@login_manager.unauthorized_handler
def error_401():
    return render_template(
        'pages/error.html',
        error={
            'code': 401,
            'message': 'You must be logged in.'
        }
    )


# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe-wifi.db'
db.init_app(app)
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
            user = db_func.get_user(email=form.data['email'])
            if user and check_password_hash(user.password, form.data['password']):
                login_user(user)
                return redirect(url_for('all_cafes'))
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
                new_user = db_func.add_user(form.data)
                login_user(new_user)
            return redirect(url_for('home'))
        except IntegrityError:
            flash('User already exists with that email.')
            return render_template('pages/register.html', form=form)
    else:
        return render_template('pages/register.html', form=form)


@app.route('/cafes')
def all_cafes():
    with app.app_context():
        cafes = db_func.get_all_cafes()
        return render_template('pages/cafes.html', cafes=cafes)


@app.route('/cafe/<cafe_id>')
def cafe(cafe_id):
    with app.app_context():
        cafe = db_func.get_cafe(cafe_id)
        if cafe:
            return render_template('pages/cafe.html', cafe=cafe)
        else:
            return render_template(
                'pages/error.html',
                error={
                    'code': 404,
                    'message': 'That cafe does not exist.'
                }
            )


@app.route('/my-list')
@login_required
def my_list():
    with app.app_context():
        my_cafes = db_func.get_user_cafes(current_user.id)
        return render_template('pages/cafes.html', cafes=my_cafes)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        try:
            with app.app_context():
                db_func.add_cafe(form.data, current_user.id)
            return redirect(url_for('all_cafes'))
        except IntegrityError:
            flash('Cafe already exists.')
            return render_template('pages/add.html', form=form)
    else:
        return render_template('pages/add.html', form=form)


@app.route('/delete/<cafe_id>')
@login_required
def delete(cafe_id):
    with app.app_context():
        cafe = db_func.get_cafe(cafe_id)
        if cafe:
            if cafe.added_by_id == current_user.id or current_user.is_admin:
                db_func.delete_cafe(cafe)
                return redirect(url_for('all_cafes'))
            else:
                return render_template(
                    'pages/error.html',
                    error={
                        'code': 401,
                        'message': 'You are not authorized to delete that cafe.'
                    }
                )
        else:
            return render_template(
                'pages/error.html',
                error={
                    'code': 404,
                    'message': 'That cafe does not exist'
                }
            )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# RUN SERVER
if __name__ == '__main__':
    app.run(port=4000, debug=True)
