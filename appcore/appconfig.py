import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
prjbasedir = os.path.join(basedir, "appcore")
dbbasedir = os.path.join(prjbasedir, "data")


class GeneralConfig:
    # Flask Builtin
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'x12345y'
    USE_X_SENDFILE = True
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # max body size: 200M
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = True  # good for response cache

    # Flask-JWT
    JWT_VERIFY_EXPIRATION = True
    JWT_EXPIRATION_DELTA = timedelta(days=30)
    JWT_AUTH_URL_RULE = '/auth/'
    JWT_AUTH_URL_OPTIONS = {'methods': ['POST']}

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbbasedir, 'base.db')

    SQLALCHEMY_BINDS = {
        'biologic': 'sqlite:///' + os.path.join(dbbasedir, 'bio.db'),
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Limiter
    RATELIMIT_DEFAULT = '1000000/minute'


class TestingConfig(GeneralConfig):
    TESTING = True
    MAIL_SUPPRESS_SEND = True


class DevelopConfig(GeneralConfig):
    DEBUG = True


class StageConfig(GeneralConfig):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(GeneralConfig):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True


def get_config(env='develop'):
    configs = {
        'develop': DevelopConfig,
        'stage': StageConfig,
        'production': ProductionConfig,
        'test': TestingConfig
    }
    return configs[env]
