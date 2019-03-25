import ldap
from flask import Flask
from sqlalchemy.orm import sessionmaker
from flask_admin import Admin, expose, helpers
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_admin.contrib import sqla
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user, current_user
import flask_admin as admin
from LogApp.forms import AdminLoginForm

app = Flask(__name__)
# регаем Фласк-Логин
login = LoginManager(app)
login.login_view = 'login'

# грузим конфиг для приложения
app.config.from_object('LogApp.config.DevelopConfig')

# декларируем базу
Base = declarative_base()
# регаем движок из конфига приложения
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# надстройка над базой
# Base.metadata.create_all(engine)
Base.metadata.reflect(engine)
# создаем сессию
Session = sessionmaker(bind=engine)
session = Session()
# переманная бд для админки
db = SQLAlchemy(app)
# регаем скрипт для миграций
migrate = Migrate(app, Base)

def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    return conn

from .admin import *

