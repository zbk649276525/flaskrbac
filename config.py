#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-22,20:21"

import os
import pymysql

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom (24)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost:3306/flaskrbac?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True



    @staticmethod
    def init_app(app):
        pass