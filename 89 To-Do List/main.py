from datetime import date, timedelta
from calendar import monthrange, leapdays, weekday
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from database import database, db, ListItem, UserSettings, User
from forms import LoginForm, RegisterForm
from turbo_flask import Turbo

# APP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySeCrEtDaTaBaSeKeY'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = None
bootstrap = Bootstrap5(app)
turbo = Turbo(app)

# LOGIN MANAGER
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return database.get_user(id=user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do-list.db'
db.init_app(app)
with app.app_context():
    db.create_all()


# VARIABLES & CLASSES
@app.context_processor
def add_variables():
    return {'today_date': date.today()}


class ToDoList():
    '''
    Parameters:
    title: The name of the list.
    range_start: The number of days from today where your range of data should start.
    range_end: The number of days from today where your range of data should end.
    new_item_due_date: The number of days from today that a newly added item should be due.
    '''

    def __init__(self, title, range_start, range_end):
        self.title = title
        self.query = db.select(ListItem).where(ListItem.due_date >= date.today() + timedelta(days=range_start), ListItem.due_date <
                                               date.today() + timedelta(days=range_end), ListItem.user_id == current_user.id).order_by(ListItem.due_date)
        self.items = db.session.execute(self.query).scalars()
        self.new_item_due_date = date.today() + timedelta(days=range_end - 1)
        self.route = '/'
        self.is_today = 0 in range(range_start, range_end)


# ROUTES
@app.route('/')
def home():
    return redirect(url_for('lists'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            user = database.get_user(email=form.data['email'])
            if user and check_password_hash(user.password, form.data['password']):
                login_user(user)
                app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = current_user.settings.theme_color
                return redirect(url_for('lists'))
            flash('Incorrect login.', 'warning')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            with app.app_context():
                new_user = database.add_user(form.data)
                login_user(new_user)
                app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = current_user.settings.theme_color
            return redirect(url_for('lists'))
        except IntegrityError:
            flash('User already exists with that email.')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/lists')
@login_required
def lists():
    list_name = None
    with app.app_context():
        today = ToDoList('Today', 0, 1)
        this_week = ToDoList('This Week', 1, 7)
        this_month = ToDoList('This Month', 7, 7*4)
        lists = [today, this_week, this_month]
        if current_user.settings.show_future_list:
            future = ToDoList('Future', 28, 7*13)
            lists.append(future)
        if current_user.settings.show_overdue_list:
            overdue = ToDoList('Overdue', -365, 0)
            overdue.items = [
                item for item in overdue.items if not item.is_completed]
            lists.append(overdue)
        for l in lists:
            l.route = 'lists'
        lists = {l.title: l for l in lists}
        if turbo.can_stream() and request.method == 'POST':
            return turbo.stream(
                turbo.update(render_template('components/list_display.html', lists=lists, editing=request.args.get('editing') if request.args.get('editing') else list_name), target='turboLists'))
        return render_template('lists.html', lists=lists, editing=request.args.get('editing') if request.args.get('editing') else list_name)


@app.route('/calendar/<view>')
@login_required
def calendar(view):
    return redirect(url_for(f'calendar_{view}'))


@app.route('/calendar/week')
@login_required
def calendar_week():
    view = 'week'
    list_name = None
    date_offset = int(request.args.get('offset')
                      ) if request.args.get('offset') else 0
    week_start = date.today() + timedelta(days=-weekday(date.today().year, date.today().month, date.today().day) -
                                          current_user.settings.week_start + date_offset * 7)
    week_end = week_start + timedelta(days=6)
    title = week_start.strftime('%b %-d') + ' – ' + week_end.strftime(
        '%-d' if week_start.strftime('%b') == week_end.strftime('%b') else week_end.strftime('%b %-d')) if request.args.get('offset') else 'This Week'
    lists = {}
    for i in range(7):
        j = i - weekday(date.today().year, date.today().month,
                        date.today().day) - current_user.settings.week_start + date_offset * 7
        todo_list = ToDoList('Today' if j == 0 else (
            date.today() + timedelta(days=j)).strftime('%A – %-d' if request.args.get('offset') else '%A'), j, j + 1)
        todo_list.route = 'calendar'
        lists[todo_list.title] = todo_list

    if turbo.can_stream():
        return turbo.stream(
            turbo.update(render_template('components/list_display.html', view=view, lists=lists, editing=request.args.get('editing') if request.args.get('editing') else list_name, title=title), target='turboCalendar'))
    return render_template(f'calendar.html', view=view, lists=lists, editing=request.args.get('editing') if request.args.get('editing') else list_name, title=title)


@app.route('/calendar/month')
@login_required
def calendar_month():
    view = 'month'
    list_name = None
    title = date(1, 12 if ((date.today().month + int(request.args.get('offset'))) % 12) == 0 else (date.today().month + int(request.args.get('offset'))) %
                 12, 1).strftime('%B') + ' ' + str(date.today().year + (date.today().month + int(request.args.get('offset'))) // 12) if request.args.get('offset') else 'This Month'
    lists = {}
    date_offset = int(request.args.get('offset')
                      ) if request.args.get('offset') else 0
    offset_year = date.today().year + (date_offset // 12)
    offset_month = 12 if ((
        date.today().month + date_offset) % 12) == 0 else (date.today().month + date_offset) % 12
    offset_days = 0
    for i in range(date_offset) if date_offset >= 0 else range(-1, date_offset - 1, -1):
        offset_days += monthrange(date.today().year + ((date.today().month + i) // 12), 12 if (
            date.today().month + i) % 12 == 0 else (date.today().month + i) % 12)[
            1] * (-1 if date_offset < 0 else 1)
    for i in range(offset_days, offset_days + monthrange(offset_year, offset_month)[1]):
        todo_list = ToDoList('Today' if i == date.today().day - 1 else (date.today() - timedelta(
            days=date.today().day) + timedelta(days=i + 1)).strftime('%-d'), i - date.today().day + 1, i - date.today().day + 2)
        todo_list.route = 'calendar'
        lists[todo_list.title] = todo_list
    if turbo.can_stream():
        return turbo.stream(
            turbo.update(render_template('components/list_display.html', view=view, lists=lists, editing=request.args.get('editing') if request.args.get('editing') else list_name, title=title), target='turboCalendar'))
    return render_template(f'calendar.html', view=view, lists=lists, editing=request.args.get('editing') if request.args.get('editing') else list_name, title=title)


@app.route('/calendar/year')
@login_required
def calendar_year():
    view = 'year'
    list_name = None
    title = str(date.today().year + int(request.args.get('offset'))
                ) if request.args.get('offset') else 'This Year'
    lists = {}
    date_offset = int(request.args.get('offset')
                      ) if request.args.get('offset') else 0
    offset_days = 365 * date_offset + \
        (leapdays(date.today().year, date.today().year + date_offset) if date_offset >=
            0 else -leapdays(date.today().year + date_offset, date.today().year))
    for i in range(12):
        this_month_start = date.today() - timedelta(days=date.today().day - 1)
        month_start = this_month_start - \
            timedelta(days=sum([monthrange(date.today().year, x)[1] for x in range(1, date.today().month)])) + \
            timedelta(days=sum([monthrange(date.today().year, x)[1]
                                for x in range(1, i + 1)]))
        todo_list = ToDoList(month_start.strftime(
            '%B'), -(date.today() - month_start).days + offset_days, -(date.today() - month_start).days + monthrange(date.today().year, month_start.month)[1] + offset_days)
        todo_list.route = 'calendar'
        lists[todo_list.title] = todo_list
    if turbo.can_stream():
        return turbo.stream(
            turbo.update(render_template('components/list_display.html', view=view, lists=lists, editing=request.args.get(
                'editing') if request.args.get('editing') else list_name, title=title), target='turboCalendar'))
    return render_template(f'calendar.html', view=view, lists=lists, editing=request.args.get('editing') if request.args.get('editing') else list_name, title=title)


@app.route('/edit/<route>', methods=['GET', 'POST'])
@login_required
def edit(route):
    if request.method == 'POST':
        data = request.form.to_dict()
        # If there is text in the new item form field
        if len(data['new_item'].strip()) > 0:
            with app.app_context():
                new_list_item = ListItem(
                    text=data['new_item'].strip(),
                    due_date=date(
                        *(int(n) for n in data['new_item_due_date'].split('-'))),
                    user_id=current_user.id
                )
                db.session.add(new_list_item)
                db.session.commit()
        # If check box is hit.
        if request.args.get('checked'):
            ids = [id.split('_')[1] for id in list(data.keys())[:-3:2]]
            texts = [text for text in list(data.values())[:-3:2]]
            due_dates = [date(*(int(n) for n in due_date.split('-')))
                         for due_date in list(data.values())[1:-3:2]]
            data = [{'id': ids[i], 'text': texts[i], 'due_date': due_dates[i]}
                    for i in range(len(ids))]
            with app.app_context():
                for entry in data:
                    db.session.query(ListItem).\
                        filter(ListItem.id == entry['id']). \
                        update(entry)
                db.session.commit()
        return redirect(url_for(route, view=request.args.get('view'), offset=request.args.get('offset'), editing=request.args.get('editing')))


@app.route('/delete/<list_item_id>')
@login_required
def delete(list_item_id):
    with app.app_context():
        list_item = db.session.execute(
            db.select(ListItem).where(ListItem.id == list_item_id)).scalar()
        db.session.delete(list_item)
        db.session.commit()
    return redirect(url_for(request.args.get('route'), view=request.args.get('view'), editing=request.args.get('editing'), offset=request.args.get('offset')))


@app.route('/toggle/<list_item_id>')
@login_required
def toggle(list_item_id):
    with app.app_context():
        list_item = db.session.execute(
            db.select(ListItem).where(ListItem.id == list_item_id)).scalar()
        list_item.is_completed = not list_item.is_completed
        db.session.commit()
    return redirect(url_for(request.args.get('route'), view=request.args.get('view'), editing=request.args.get('editing'), offset=request.args.get('offset')))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        with app.app_context():
            settings = request.form.to_dict()
            current_user.settings.theme_color = None if settings[
                'theme_color'] == 'default' else settings['theme_color']
            current_user.settings.show_future_list = 'show_future_list' in settings
            current_user.settings.show_overdue_list = 'show_overdue_list' in settings
            current_user.settings.default_calendar_view = settings['default_calendar_view']
            current_user.settings.week_start = int(
                settings['calendarViewWeekStart'])
            db.session.commit()
        app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = current_user.settings.theme_color
    return render_template('settings.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = None
    return redirect(url_for('login'))


@app.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    entered_pw = request.form.to_dict()['password']
    with app.app_context():
        user = database.get_user(email=current_user.email)
        if user and check_password_hash(user.password, entered_pw):
            delete_q = ListItem.__table__.delete().where(
                ListItem.user_id == current_user.id)
            db.session.execute(delete_q)
            delete_q = UserSettings.__table__.delete().where(
                UserSettings.user_id == current_user.id)
            db.session.execute(delete_q)
            delete_q = User.__table__.delete().where(
                User.id == current_user.id)
            db.session.execute(delete_q)
            db.session.commit()
            logout_user()
            app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = None
            flash('Your account has been deleted.')
            return redirect(url_for('register'))
        flash('Incorrect password. Could not delete account.')
        return render_template('settings.html')


# RUN SERVER
if __name__ == '__main__':
    app.run(port=4000)
