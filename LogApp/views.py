import ldap
from datetime import date

from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from werkzeug.urls import url_parse

from .app import app, session
from .models import User, UserGroup, UserUsergroupMap, Report
from flask_login import current_user, login_user, login_required, logout_user
from flask import redirect, url_for, flash, render_template, request, jsonify, json, g

from .forms import LoginForm

from sqlalchemy import desc

# Главная страница
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.before_request
def get_current_user():
    g.user = current_user

# авторизация для преподов, контроллеров
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            User.try_login(form.username.data, form.password.data)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('login.html', form=form)
        user = session.query(User).filter_by(username=form.username.data).first()
        if user is None:
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
    permission_group_id = User.get_group_parent_id(current_user)
    if  permission_group_id == 18:
        teacher = current_user

        reports = session.query(Report).filter(Report.id_teacher == current_user.id).order_by(desc(Report.id)).all()
        date_list = set([report.date for report in reports])

        try:
            controller = reports[0].controller
        except IndexError:
            controller = "контроллер не назначен"
        if request.args.get('date') is not None:
            reports = [report for report in reports if str(report.date) == request.args.get('date')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', reports=reports, user=current_user, controller=controller,
                                               date_list=date_list, permission_group_id=permission_group_id))
        return render_template('reports.html', reports=reports, user=teacher, controller=controller,
                               date_list=date_list, permission_group_id=permission_group_id)
    if permission_group_id == 31:
        reports = session.query(Report).filter(Report.id_controller == current_user.id).order_by(desc(Report.id)).all()
        date_list = set([report.date for report in reports])
        teachers_list = []
        groups_list = []
        for report in reports:
            teacher = session.query(User).get(report.id_teacher)
            if teachers_list.count(teacher) < 1:
                teachers_list.append(teacher)
        for report in reports:
            if groups_list.count(report.group) < 1:
                groups_list.append(report.group)
        if request.args.get('date') is not None:
            reports = [report for report in reports if str(report.date) == request.args.get('date')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list,
                                               permission_group_id=permission_group_id))
        if request.args.get('group') is not None:
            reports = [report for report in reports if str(report.group) == request.args.get('group')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list,
                                               permission_group_id=permission_group_id))
        if request.args.get('teacher') is not None:
            reports = [report for report in reports if str(report.teacher) == request.args.get('teacher')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list,
                                               permission_group_id=permission_group_id))
        if request.args.get('status') is not None:
            reports = [report for report in reports if str(report.status) == request.args.get('status')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list,
                                               permission_group_id=permission_group_id))
        return render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list,
                               permission_group_id=permission_group_id)
    if permission_group_id == 6 or permission_group_id == 1:
        reports = session.query(Report).order_by(desc(Report.id)).all()
        date_list = set([report.date for report in reports])
        teachers_list = []
        groups_list = []
        controller_list = []
        for report in reports:
            teacher = session.query(User).get(report.id_teacher)
            if teachers_list.count(teacher) < 1:
                teachers_list.append(teacher)
        for report in reports:
            if groups_list.count(report.group) < 1:
                groups_list.append(report.group)
        for report in reports:
            controller = session.query(User).get(report.id_controller)
            if controller_list.count(controller) < 1:
                controller_list.append(controller)
        if request.args.get('date') is not None:
            reports = [report for report in reports if str(report.date) == request.args.get('date')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list, controller_list=controller_list,
                                               permission_group_id=permission_group_id))
        if request.args.get('group') is not None:
            reports = [report for report in reports if str(report.group) == request.args.get('group')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list, controller_list=controller_list,
                                               permission_group_id=permission_group_id))
        if request.args.get('teacher') is not None:
            reports = [report for report in reports if str(report.teacher) == request.args.get('teacher')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list, controller_list=controller_list,
                                               permission_group_id=permission_group_id))
        if request.args.get('controller') is not None:
            reports = [report for report in reports if str(report.controller) == request.args.get('controller')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list, controller_list=controller_list,
                                               permission_group_id=permission_group_id))
        if request.args.get('status') is not None:
            reports = [report for report in reports if str(report.status) == request.args.get('status')]
            if 'CONTENT_TYPE' in request.headers.environ:
                return jsonify(render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list,
                                               permission_group_id=permission_group_id, controller_list=controller_list))
        return render_template('reports.html', user=current_user, reports=reports, date_list=date_list,
                               teachers_list=teachers_list, groups_list=groups_list, controller_list=controller_list,
                               permission_group_id=permission_group_id)
    return BadRequest()

@app.route('/create_report', methods=['GET', 'POST'])
@login_required
def create_report_view():
    permission_group_id = User.get_group_parent_id(current_user)
    if request.method == 'POST':
        report = Report(date=date.today(), group=request.form['group'], id_teacher=int(request.form['teacher']),
                        comment=request.form['comment'], id_controller=int(current_user.id),
                        pages=str('Страницы: с '+ request.form['number-from']+' по '+request.form['number-to']) + '.')
        session.add(report)
        session.commit()
        return redirect(url_for('reports_view'))
    if permission_group_id != 31:
        return Forbidden()
    users = session.query(User).all()
    teachers = [teacher for teacher in users if User.get_group_parent_id(teacher)==18]
    return render_template('create_report.html', date=date.today(), teachers=teachers, permission_group_id=permission_group_id)

@app.route('/change_status_report/<id>', methods=["GET", "POST"])
@login_required
def change_status_report_view(id):
    permission_group_id = User.get_group_parent_id(current_user)
    try:
        report = session.query(Report).get(id)
        if request.headers.get('action') == 'status':
            if permission_group_id == 18:
                report.status = 'Подтверждение'
            if permission_group_id == 31:
                if request.headers.get('change') == 'success':
                    report.status = 'Выполнено'
                if request.headers.get('change') == 'change':
                    report.status = 'Исправить'
        if request.headers.get('action') == 'info':
            report = request.form
            report.status = 'Исправить'
        session.commit()
        import time
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    except:
        return NotFound("Report not found")

@app.route('/change_report/<id>', methods=["GET", "POST"])
@login_required
def change_report_view(id):
    permission_group_id = User.get_group_parent_id(current_user)
    if permission_group_id != 31:
        return Forbidden()
    report = session.query(Report).get(id)
    if request.method == 'POST':
        report.date=date.today()
        report.group=request.form['group']
        report.id_teacher=int(request.form['teacher'])
        report.comment=request.form['comment']
        report.id_controller=int(current_user.id)
        report.pages=str('Страницы: с '+ request.form['number-from']+' по '+request.form['number-to']) + '.'
        session.commit()
        return redirect(url_for('reports_view'))
    import re
    page_start = page_end = None
    try:
        page_start, page_end = re.findall('(\d+)', report.pages)
    except ValueError:
        pass
    users = session.query(User).all()
    teachers = [teacher for teacher in users if User.get_group_parent_id(teacher) == 18]
    return render_template('create_report.html', date=date.today(), teachers=teachers, report=report,
                           page_start=page_start, page_end=page_end, permission_group_id=permission_group_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))