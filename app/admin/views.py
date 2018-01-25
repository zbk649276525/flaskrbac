#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-23,12:43"
from flask import render_template,flash,redirect,url_for,request
from . import admin
from .forms import MenuForm,GroupForm
from ..models import Menu,Group
from app import db



@admin.route("/")
def index():
    return render_template('admin/layout.html')

@admin.route("/menu_add",methods = ["GET","POST"])
def menu_add():
    '''添加菜单'''

    form = MenuForm()
    if request.method == "GET":
        form.menu_id.choices = [(v.id,v.name) for v in Menu.query.all ()]
    if form.validate_on_submit():
        data = form.data
        menu = Menu.query.filter_by(name = data.get("name")).count()
        if menu:
            flash("菜单名称已存在!","err")
            return redirect(url_for("admin.menu_add"))
        menu = Menu(
            name = data.get("name")
        )
        print(data.items())
        db.session.add(menu)
        db.session.commit()
        flash("菜单添加成功!",'ok')
        return redirect(url_for("admin.menu_add"))
    return render_template("admin/menu_add.html",form = form)

@admin.route("/group_add",methods = ["GET","POST"])
def group_add():
    '''添加组'''
    form= GroupForm()
    if request.method == 'POST' and form.validate():
        group = Group(
            name = form.data.get("name"),
            menu_id = form.data.get("menu_id")
        )
        db.session.add(group)
        db.session.commit()
        flash("添加组名称成功!","ok")
        return redirect(url_for("admin.group_add"))
    print(form.data.get("menu_id"))
    return render_template("admin/group_add.html",form = form)