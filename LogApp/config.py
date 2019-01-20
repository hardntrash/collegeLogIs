import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'jioqwjuieqw987eh879327y918h2'
    SECRET_KEY = 'sdufiunwodiun8273y9821hn37nd8u2n38u'
    SQLALCHEMY_DATABASE_URI = 'mysql://king:123res@localhost:3306/testlogtdb?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'

class ProductionConfig(Config):
    DEBUG = False

class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True