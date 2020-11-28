import click
import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from appcore.appconfig import get_config
from appcore.models import *
from appcore.models.user import User

migrate = Migrate(compare_type=True)

def create_app(config_name=None):
    app = Flask("appcore")
    app.config.from_object(get_config())

    register_commands(app)

    jwt = JWT(app, authenticate, identity)

    db.init_app(app)
    migrate.init_app(app, db)

    from appcore.blueprints.auth import auth_bp
    from appcore.blueprints.seller import seller_bp
    from appcore.blueprints.common_resource import common_resource_bp
    blue_prints = [auth_bp,seller_bp ,common_resource_bp]
    for bp in blue_prints:
        register_routes(app, bp)

    return app


def register_commands(app):

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        click.echo('start drop database.')
        """Initialize the appcore."""
        if drop:
            click.confirm(
                'This operation will delete the appcore, do you want to continue?',
                abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def hello():
        click.echo('Hello World.')


def register_routes(app, blueprint):
    app.register_blueprint(blueprint)


def authenticate(username, password):
    user = User.query.filter_by(email=username).first()
    if not user:
        return {"msg": "user not found"}
    if not user.check_password(password):
        return {"msg": "password error"}
    return user


def identity(payload):
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    return user


def configure_jwt(app):
    jwt = JWT(app, authenticate, identity)
    return jwt
