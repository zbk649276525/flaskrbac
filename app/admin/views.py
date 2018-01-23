#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-23,12:43"
from flask import render_template
from . import admin
@admin.route("/")
def index():
    return render_template('admin/layout.html')