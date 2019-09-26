from flask import Flask, render_template
from flask_uploads import configure_uploads, patch_request_class

from blog.extensions import bootstrap, db, loginmanager, markdowns
# from blog.generate import Generate
from config import config


# gen = Generate()
# gen()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprint(app)
    register_extensions(app)
    # register_errors(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    # loginmanager.init_app(app)
    configure_uploads(app, markdowns)
    patch_request_class(app)


def register_blueprint(app):
    from .views import blog
    app.register_blueprint(blog.bp)
    from .views import admin
    app.register_blueprint(admin.bp, url_prefix='/admin')
    # from .views import api
    # app.register_blueprint(api.bp, url_prefix='/api')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html')
