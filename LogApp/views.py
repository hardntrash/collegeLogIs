from datetime import date
from werkzeug.urls import url_parse

from .app import app, session
from .models import User, Report
from flask_login import current_user, login_user, login_required
from flask import redirect, url_for, flash, render_template, request, jsonify
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




@app.route('/reports')
@login_required
def reports_view():
    if current_user.id_permission_gorup == 2:
        teacher = current_user
        reports = session.query(Report).filter(Report.id_teacher == current_user.id).all()
        date_list = set([report.date for report in reports])
        controller = reports[0].controller
        if request.args.get('date') is not None:
            reports = [report for report in reports if str(report.date) == request.args.get('date')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', reports=reports, teacher=teacher, controller=controller, date_list=date_list))
        return render_template('reports.html', reports=reports, teacher=teacher, controller=controller, date_list=date_list)