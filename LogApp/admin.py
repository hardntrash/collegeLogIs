from flask_admin.contrib import sqla
import flask_admin as admin
from werkzeug.exceptions import Forbidden

from LogApp.forms import AdminLoginForm
from flask_admin import expose, helpers
from .app import app, session
from flask_login import logout_user, current_user, AnonymousUserMixin, login_required


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        try:
            return current_user.id_permission_gorup == 4
        except AttributeError:
            return redirect(url_for('admin.login_view'))

class MyAdminIndexView(admin.AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = AdminLoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = session.query(User).filter_by(login=form.username.data).first()
            if user is None or user.password != form.password.data:
                flash('Invalid username or password')
                return redirect(url_for('.login_view'))
            login_user(user)
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))




# регаем админку
admin = admin.Admin(app, 'CollegeLogIS', index_view=MyAdminIndexView(), base_template='my_master.html')

# создаем вьюхи под модели в админке
from .models import *

admin.add_view(MyModelView(Report, session))
admin.add_view(MyModelView(User, session))
admin.add_view(MyModelView(Group, session))
admin.add_view(MyModelView(PermissionGroup, session))

from .views import *