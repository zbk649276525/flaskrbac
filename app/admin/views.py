#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-23,12:43"
from flask import render_template,flash,redirect,url_for,request,session
from . import admin
from .forms import MenuForm,GroupForm,UserAddForm,RoleAddForm,AuthAddForm,LoginForm
from ..models import Menu,Group,Auth,User,User_Roles,Role,Role_auths
from app import db
from werkzeug.security import generate_password_hash
from ..service.init_permission import init_permission
from . import flask_rbac



@admin.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.data.get("account")).first()
        if not user.check_pwd(form.data.get("pwd")):
            flash("用户名或密码错误!","err")
            return redirect (url_for ("admin.login"))
        init_permission(user,session)
        return redirect(request.args.get("next"),url_for("admin.index"))
    return render_template("admin/login.html",form = form)

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

@admin.route("/user/add",methods = ["GET","POST"])
def user_add():
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
            user_roles = []
            for i in form.data.get ("role_id"):
                user_role = User_Roles (
                    user_id = user.id,
                    role_id = i
                )
                user_roles.append (user_role)
            db.session.add_all (user_roles)
            db.session.commit ()
        flash("添加管理员成功!","ok")
        return redirect(url_for("admin.user_add"))
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
        data = form.data
        try:
            role = Role.query.filter_by (name = data.get ("name")).count ()
            if role:
                flash("角色名称已经存在!","err")
                return redirect(url_for("admin.role_add"))
            role = Role(name = data.get("name"))
            db.session.add(role)
            db.session.commit()
            if form.auth_id.data:
                role_auths = []
                for i in data.get("auth_id"):
                    role_auth = Role_auths(
                        role_id = role.id,
                        auth_id = i
                    )
                    role_auths.append(role_auth)
                db.session.add_all(role_auths)
                db.session.commit()
            flash("角色添加成功!","ok")
        except Exception as e:
            db.session.rollback()
            flash("角色添加失败","err")
    return render_template("admin/role_add.html",form = form)

@admin.route("/auth/add",methods = ["GET","POST"])
def auth_add():
    form = AuthAddForm()
    if form.validate_on_submit():
        menu_gp_id = form.data.get ("auth_id")
        if not menu_gp_id:
            auth = Auth (
                name = form.data.get ("name"),
                url = form.data.get ("url"),
                code = form.data.get ("code"),
                menu_gp_id = None,
                group_id = form.data.get ("group_id")
            )
        else:
            auth = Auth (
                name = form.data.get ("name"),
                url = form.data.get ("url"),
                code = form.data.get ("code"),
                menu_gp_id = menu_gp_id,
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

