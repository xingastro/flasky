# -*- coding: utf-8 -*-
import sqlite3


class Model(object):
    @staticmethod
    def connect_db(database='ForFun.db'):
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        return conn
