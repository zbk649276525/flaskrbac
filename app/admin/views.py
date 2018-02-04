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
from app.middlewares import flask_rbac
from app.tempaltetags.page_auth_list import Base_permission_list



@admin.route("/login/",methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.data.get("account")).first()
        if not user.check_pwd(form.data.get("pwd")):
            flash("用户名或密码错误!","err")
            return redirect (url_for ("admin.login"))
        session["admin"] = user.username
        init_permission(user,session)
        return redirect(request.args.get("next")or url_for("admin.index"))
    return render_template("admin/login.html",form = form)

@admin.route("/index/")
def index():

    return render_template('admin/layout.html')

@admin.route("/menu/add/",methods = ["GET","POST"])
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
        print(menu)
        db.session.add(menu)
        db.session.commit()
        flash("菜单添加成功!",'ok')
        return redirect(url_for("admin.menu_add"))
    return render_template("admin/menu_add.html",form = form)


@admin.route("/menu/list/<int:page>/",methods = ["GET"])
@admin.route("/menu/list/",methods = ["GET"])
def menu_list(page = None):
    '''菜单列表'''
    auth_list = Base_permission_list (request.permission_code_list)
    if not page:
        page = 1
    page_data = Menu.query.paginate(page = page,per_page = 10)
    return render_template("admin/menu_list.html",page_data = page_data,auth_list = auth_list)


@admin.route("/group/add/",methods = ["GET","POST"])
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

@admin.route("/user/add/",methods = ["GET","POST"])
def user_add():
    '''添加管理员'''
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
    auth_list = Base_permission_list (request.permission_code_list)
    if not page:
        page = 1
    page_data = User.query.paginate(page = page,per_page = 10)
    return render_template("admin/user_list.html",page_data = page_data,auth_list = auth_list)

@admin.route("/user/delete/<int:id>/")
def user_delete(id = None):
    auth = User.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash("删除标签成功！", "ok")
    return redirect(url_for('admin.user_list', page=1))


@admin.route("/role/add/",methods = ["GET","POST"])
def role_add():
    '''角色添加'''
    form = RoleAddForm()
    if form.validate_on_submit():
        data = form.data
        role_name = Role.query.filter_by(name=data.get("name")).count()
        if role_name:
            flash("角色已存在!","err")
            return redirect(url_for("admin.role_add"))
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

@admin.route("/role/list/<int:page>/",methods = ["GET"])
@admin.route("/role/list/",methods = ["GET"])
def role_list(page = None):
    '''权限列表'''
    auth_list = Base_permission_list (request.permission_code_list)
    if not page:
        page = 1
    page_data = Role.query.paginate(page = page,per_page = 10)
    return render_template("admin/role_list.html",page_data = page_data,auth_list = auth_list)


@admin.route("/auth/add/",methods = ["GET","POST"])
def auth_add():
    '''权限添加'''
    form = AuthAddForm()
    if form.validate_on_submit():
        auth_name = Auth.query.filter_by(name = form.data.get("name")).count()
        auth_url = Auth.query.filter_by(url = form.data.get ("url")).count()
        if auth_name or auth_url:
            flash("权限已存在,请勿重复添加!","err")
            return redirect(url_for("admin.auth_add"))
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
        db.session.add(auth)
        db.session.commit ()
        #超级管理员拥有所所有的权限
        role = Role.query.filter_by(name="超级管理员").first()
        role_auth = Role_auths(
            role_id= role.id,
            auth_id = auth.id
        )
        db.session.add(role_auth)
        db.session.commit()
        flash ("添加权限成功!","ok")
        return redirect (url_for ("admin.auth_add"))
    return render_template("admin/auth_add.html",form = form)


@admin.route("/auth/list/<int:page>/",methods = ["GET"])
@admin.route("/auth/list/",methods = ["GET"])
def auth_list(page = None):
    '''权限列表'''
    auth_list = Base_permission_list (request.permission_code_list)
    if not page:
        page = 1
    page = int(request.args.get("page", 1))
    page_data = Auth.query.paginate(page = page,per_page = 10)
    return render_template("admin/auth_list.html",page_data = page_data,auth_list = auth_list)

