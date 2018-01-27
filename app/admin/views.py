#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-23,12:43"
from flask import render_template,flash,redirect,url_for,request
from . import admin
from .forms import MenuForm,GroupForm,UserAddForm,RoleAddForm,AuthAddForm
from ..models import Menu,Group,Auth,User,User_Roles,Role,Role_auths
from app import db
from werkzeug.security import generate_password_hash



@admin.route("/")
def index():
    return render_template('admin/layout.html')

@admin.route("/menu/add",methods = ["GET","POST"])
def menu_add():
    '''添加菜单'''

    form = MenuForm()
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


@admin.route("/menu/list/<int:page>/",methods = ["GET"])
@admin.route("/menu/list/",methods = ["GET"])
def menu_list(page = None):
    '''菜单列表'''
    if not page:
        page = 1
    page_data = Menu.query.paginate(page = page,per_page = 10)
    return render_template("admin/menu_list.html",page_data = page_data)


@admin.route("/group/add",methods = ["GET","POST"])
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
    return render_template("admin/group_add.html",form = form)

@admin.route("/admin/add",methods = ["GET","POST"])
def admin_add():
    form = UserAddForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            password = generate_password_hash(form.password.data),
            email = form.email.data,
        )
        db.session.add(user)
        db.session.commit()

        if form.role_id.data:
            user_role = User_Roles(
                user_id = user.id,
                role_id = form.role_id.data
            )
            db.session.add(user_role)
            db.session.commit()
        flash("添加管理员成功!","ok")
        return redirect(url_for("admin.admin_add"))
    return render_template("admin/user_add.html",form = form)

@admin.route("/user/list/<int:page>/",methods = ["GET"])
@admin.route("/user/list/",methods = ["GET"])
def user_list(page = None):
    '''权限列表'''
    if not page:
        page = 1
    page_data = User.query.paginate(page = page,per_page = 10)
    return render_template("admin/user_list.html",page_data = page_data)



@admin.route("/role/add",methods = ["GET","POST"])
def role_add():
    form = RoleAddForm()
    if form.validate_on_submit():
        role = Role(name = form.name.data)
        db.session.add(role)
        db.session.commit()
        if form.auth_id.data:
            role_auth = Role_auths(
                role_id = role.id,
                auth_id = form.auth_id.data
            )
            db.session.add(role_auth)
            db.session.commit()
        flash("角色添加成功!","ok")
    return render_template("admin/role_add.html",form = form)

@admin.route("/auth/add",methods = ["GET","POST"])
def auth_add():
    form = AuthAddForm()
    if form.validate_on_submit():
        auth = Auth (
            name = form.data.get ("name"),
            url = form.data.get ("url"),
            code = form.data.get ("code"),
            menu_gp_id = form.data.get ("auth_id",None),
            group_id = form.data.get ("group_id")
        )
        db.session.add (auth)
        db.session.commit ()
        flash ("添加权限成功!","ok")
        return redirect (url_for ("admin.auth_add"))
    return render_template("admin/auth_add.html",form = form)


@admin.route("/auth/list/<int:page>/",methods = ["GET"])
@admin.route("/auth/list/",methods = ["GET"])
def auth_list(page = None):
    '''权限列表'''
    if not page:
        page = 1
    page_data = Auth.query.paginate(page = page,per_page = 10)
    return render_template("admin/auth_list.html",page_data = page_data)

