from flask import Flask
from config import config
from api.controller import register_blueprints
from flask_smorest import Api


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    api = Api(app)
    register_blueprints(api)

    return app
