from datetime import date, timedelta
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from database import database, db, ListItem
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
        print('login', form.data)
        return redirect(url_for('lists'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('register', form.data)
        try:
            with app.app_context():
                new_user = database.add_user(form.data)
                login_user(new_user)
            return redirect(url_for('lists'))
        except IntegrityError:
            flash('User already exists with that email.')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/lists', methods=['GET', 'POST'])
def lists():
    if request.method == 'POST':
        list_item = request.form.to_dict()
        list_name = list(list_item.keys())[0]
        match list_name:
            case 'Today':
                due_date = date.today()
            case 'This Week':
                due_date = date.today() + timedelta(days=7)
            case 'This Month':
                due_date = date.today() + timedelta(weeks=4)
            case 'Future':
                due_date = date.today() + timedelta(weeks=13)
        with app.app_context():
            new_list_item = ListItem(
                text=list_item[list_name],
                due_date=due_date,
                user_id=current_user.id
            )
            db.session.add(new_list_item)
            db.session.commit()
    with app.app_context():
        today_q = db.select(ListItem).where(
            ListItem.due_date <= date.today(), ListItem.user_id == current_user.id).order_by(ListItem.due_date)
        this_week_q = db.select(ListItem).where(
            ListItem.due_date > date.today(), ListItem.due_date <= date.today() + timedelta(days=7), ListItem.user_id == current_user.id).order_by(ListItem.due_date)
        this_month_q = db.select(ListItem).where(
            ListItem.due_date > date.today() + timedelta(days=7), ListItem.due_date <= date.today() + timedelta(weeks=4), ListItem.user_id == current_user.id).order_by(ListItem.due_date)
        future_q = db.select(ListItem).where(
            ListItem.due_date > date.today() + timedelta(weeks=4), ListItem.user_id == current_user.id).order_by(ListItem.due_date)
        today = {'title': 'Today',
                 'items': db.session.execute(today_q).scalars()}
        this_week = {'title': 'This Week',
                     'items': db.session.execute(this_week_q).scalars()}
        this_month = {'title': 'This Month',
                      'items': db.session.execute(this_month_q).scalars()}
        future = {'title': 'Future',
                  'items': db.session.execute(future_q).scalars()}
        return render_template('lists.html', today=date.today(), lists=[today, this_week, this_month, future], editing=request.args.get('edit') if request.args.get('edit') else False)


@app.route('/edit/<list_name>', methods=['GET', 'POST'])
def edit(list_name):
    if request.method == 'POST':
        data = request.form.to_dict()
        ids = [id.split('_')[1] for id in list(data.keys())[::2]]
        texts = [text for text in list(data.values())[::2]]
        due_dates = [date(*(int(n) for n in due_date.split('-')))
                     for due_date in list(data.values())[1::2]]
        data = [{'id': ids[i], 'text': texts[i], 'due_date': due_dates[i]}
                for i in range(len(ids))]
        with app.app_context():
            for entry in data:
                db.session.query(ListItem).\
                    filter(ListItem.id == entry['id']). \
                    update(entry)
            db.session.commit()
        return redirect(url_for('lists'))
    return redirect(url_for('lists', edit=list_name))


@app.route('/delete/<list_item_id>')
def delete(list_item_id):
    with app.app_context():
        list_item = db.session.execute(
            db.select(ListItem).where(ListItem.id == list_item_id)).scalar()
        db.session.delete(list_item)
        db.session.commit()
    return redirect(url_for('lists'))


@ app.route('/calendar/<view>')
def calendar(view):
    match view:
        case 'week':
            pass
        case 'month':
            pass
        case 'year':
            pass
    return render_template('calendar.html', view=view)


@ app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# RUN SERVER
if __name__ == '__main__':
    app.run(port=4000, debug=True)


# TODO: check box that makes it go away.
# TODO: time for todo item
# TODO: sidebar list of lists
# TODO: save edits
