#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-22,20:21"

import os
import pymysql

basedir = os.path.abspath (os.path.dirname (__file__))


class Config:
    # SECRET_KEY = os.urandom (24)#上线用
    SECRET_KEY = 'funk'#调试用
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/flaskrbac?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    PERMISSION_URL_DICT_KEY = "permission_url_dict_key"
    PERMISSION_MENU_KEY = "permission_menu_key"
    VALID_URL = ["/admin/login/","/static.*"]

    @staticmethod
    def init_app (app):
        pass
