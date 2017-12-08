# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap

from .config import Config
from .views import Views

bootstrap = Bootstrap()



def create_app():
    app = Flask(__name__)
    bootstrap.init_app(app)

    Config.init_config(app)
    Views.init_views(app)
    return app
