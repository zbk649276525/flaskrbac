#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-22,20:14"

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    db.init_app (app)
    from .models import Auth,Role,User,Group,Menu
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint,url_prefix = '/admin')
    return app

