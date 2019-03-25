import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'jioqwjuieqw987eh879327y918h2'
    SECRET_KEY = 'sdufiunwodiun8273y9821hn37nd8u2n38u'
    # TODO: НА ПРОДЕ ПОМЕНЯТЬ
    SQLALCHEMY_DATABASE_URI = 'mysql://king:123res@localhost:3306/collegetestdb?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    # TODO: НА ПРОДЕ ПОМЕНЯТЬ
    LDAP_PROVIDER_URL = 'ldap://ldap.testathon.net:389/'
    LDAP_PROTOCOL_VERSION = 3

class ProductionConfig(Config):
    DEBUG = False

class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True