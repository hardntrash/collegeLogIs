from werkzeug.urls import url_parse

from .app import app, session
from .models import User
from flask_login import current_user, login_user, login_required
from flask import redirect, url_for, flash, render_template, request
from .forms import LoginForm

# Главная страница
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# авторизация для преподов, контроллеров
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(login=form.username.data).first()
        if user is None or user.password != form.password.data:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)