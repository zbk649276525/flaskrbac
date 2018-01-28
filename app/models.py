#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-22,20:19"
from datetime import datetime
from . import db
from werkzeug.security import check_password_hash

#用户表
class User(db.Model):

    __tablename__ = 'users'
    id = db.Column (db.Integer,primary_key = True)
    username = db.Column (db.String (64),unique = True)
    password = db.Column (db.String (100))
    email = db.Column(db.String(32))

    roles= db.relationship('Role',secondary = 'user_roles',backref = 'user_role')


    def __repr__ (self):
        return "<User %r>" % self.username

    def check_pwd(self,pwd):
        return check_password_hash(self.password,pwd)


# 角色表
class Role(db.Model):

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    #与表结构无关，用于查询
    auths = db.relationship ('Auth',secondary = 'role_auths',backref = 'role_auth') # 与权限表建立多对多关系
    users = db.relationship ('User',secondary = 'user_roles',backref = 'role_user') # 与角色表建立多对多关系

    def __repr__(self):
        return "<Role %r>" % self.name

# 权限表
class Auth(db.Model):

    __tablename__ = "auths"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    code = db.Column(db.String(32))

    menu_gp_id = db.Column (db.Integer,db.ForeignKey ('auths.id'),nullable = True) #与自身建立多对一关系
    group_id = db.Column(db.Integer,db.ForeignKey('groups.id'))# 与分组表建立的多对一关系

    menu_gp = db.relationship ("Auth",remote_side = [id])#自关联
    roles = db.relationship("Role",secondary = "role_auths",backref = "auth_role")
    group = db.relationship("Group",backref = "group")


    def __repr__(self):
        return "<Auth %r>" % self.name

# 菜单表
class Menu(db.Model):

    __tablename__ = 'menus'
    id = db.Column (db.Integer,primary_key = True)
    name = db.Column (db.String (32))




    def __repr__ (self):
        return "<Menu %r>" % self.name

#分组表
class Group(db.Model):

    __tablename__ = 'groups'
    id = db.Column (db.Integer,primary_key = True)
    name = db.Column (db.String (32))

    menu_id = db.Column(db.Integer,db.ForeignKey('menus.id'))#与菜单表建立外健关系

    menu = db.relationship ("Menu",backref = 'menu')

    def __repr__ (self):
        return "<Group %r>" % self.name

#用户角色表
class User_Roles(db.Model):

    __tablename__ = "user_roles"
    id = db.Column (db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))


    def __repr__ (self):
        return "<User_Roles %r>" % self.id


#角色权限表

class Role_auths(db.Model):

    __tablename__ = 'role_auths'
    id = db.Column (db.Integer,primary_key = True)
    role_id = db.Column (db.Integer,db.ForeignKey('roles.id'))
    auth_id = db.Column (db.Integer,db.ForeignKey('auths.id'))

    def __repr__ (self):
        return "<Role_auths %r>" % self.id

