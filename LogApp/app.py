from flask import Flask
from sqlalchemy.orm import sessionmaker
from flask_admin import Admin
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# грузим конфиг для приложения
app.config.from_object('LogApp.config.DevelopConfig')

# декларируем базу
Base = declarative_base()
# регаем движок из конфига приложения
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# надстройка над базой
# Base.metadata.create_all(engine)
Base.metadata.reflect(engine)
# регаем бд для фласк-алхимии
Session = sessionmaker(bind=engine)
db = SQLAlchemy(app)
migrate = Migrate(app, Base)

# регаем админку
admin = Admin(app, name='LogIS', template_mode='bootstrap3')

# создаем вьюхи под модели в админке
from .models import *

admin.add_view(ModelView(Report, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Group, db.session))
admin.add_view(ModelView(PermissionGroup, db.session))

