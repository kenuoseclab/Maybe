#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 18:21:49
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-26 14:15:24
#

import click

from flask import Flask
from flask import current_app

from app.extensions import db
from app.extensions import loginmanager
from app.models import Role
from app.models import User

from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprint(app)
    register_extensions(app)
    register_command(app)

    return app


def register_extensions(app):
    db.init_app(app)
    loginmanager.init_app(app)


def register_blueprint(app):
    from app.views import main
    app.register_blueprint(main.bp)
    from app.views import auth
    app.register_blueprint(auth.bp, url_prefix='/auth')


def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            if click.confirm('This operation will delete the database, do you want to continue?'):
                db.drop_all()
                click.echo('All tables have been dropped.')
        db.create_all()
        click.echo('Initialized database.')
        Role.initRoles()
        click.echo('Initialized Roles.')

    @app.cli.command()
    @click.argument('username')
    @click.argument('password')
    def initadmin(username, password):
        email = current_app.config['ADMIN_EMAIL']
        if User.query.first():
            click.echo('Administrator already exsits.')
            return None
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        click.echo('Initialized Administrator %s' % username)