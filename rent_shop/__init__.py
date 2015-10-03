__author__ = 'hzhigeng'

from flask import Flask
from rent_shop.views import rent, wanted, pictures
from mongoengine import connect

__all__ = ['create_app']

DEFAULT_BLUEPRINTS = [rent, wanted, pictures]
DEFAULT_APP_NAME = 'rent_shop'


def create_app(config='config', blueprints=None):
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(DEFAULT_APP_NAME, instance_relative_config=True)

    app.config.from_object(config)
    app.config.from_pyfile('config.py')

    configure_db(app.config)
    configure_blueprint(app, blueprints)
    return app


def configure_db(config):
    connect(config['DB_NAME'], host=config['DB_HOST'], username=config['DB_USER'], password=config['DB_PWD'])


def configure_blueprint(app, blueprints):
    for bp in blueprints:
        app.register_blueprint(bp)
