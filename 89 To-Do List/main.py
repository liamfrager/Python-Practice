from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from database import database, db
from forms import LoginForm, RegisterForm

# APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySeCrEtDaTaBaSeKeY'
bootstrap = Bootstrap5(app)

# LOGIN MANAGER
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return database.get_user(id=user_id)


# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do-list.db'
db.init_app(app)
with app.app_context():
    db.create_all()


# ROUTES
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('login.html', form=form)
        return redirect(url_for('list'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/list')
def list():
    today = {}
    this_week = {}
    this_month = {}
    return render_template('list.html', today=today, this_week=this_week, this_month=this_month)


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/logout')
def logout():
    return redirect(url_for('home'))


# RUN SERVER
if __name__ == '__main__':
    app.run(port=4000, debug=True)


# TODO: check box that makes it go away.
# TODO: time for todo item
# TODO: sidebar list of lists
