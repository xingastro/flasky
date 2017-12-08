# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    @staticmethod
    def init_config(app):
        app.config.update(dict(
            DATABASE='ForFun.db',
            SECRET_KEY='development_key',
            DEBUG=True
        ))
