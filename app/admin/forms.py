#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-25,14:01"
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,EqualTo,Email
from wtforms import StringField,SubmitField,SelectField,PasswordField,SelectMultipleField
from app.models import Menu,Auth,Group,Role


class MenuForm (FlaskForm):
    '''菜单表单'''
    name = StringField (label = "菜单名称",validators = [DataRequired ("菜单不能为空!")],
                        render_kw = {"class":"form-control","placeholder":"请输入菜单名称!"})
    submit = SubmitField ("提交",render_kw = {"class":"btn btn-primary"})


class GroupForm (FlaskForm):
    '''分组表单'''
    name = StringField (label = "组名称",validators = [DataRequired ("组名称不能为空!")],
                        render_kw = {"class":"form-control","placeholder":"请输入组名称!"})
    menu_id = SelectField (label = "所属菜单",validators = [DataRequired ("请选择菜单!")],coerce = int,
                           choices = [(v.id,v.name) for v in Menu.query.all ()],render_kw = {"class":"form-control"})
    submit = SubmitField ("提交",render_kw = {"class":"btn btn-primary"})

    # def __init__(self,*args,**kwargs):
    #     self.menu_id.choices = [(v.id,v.name) for v in Menu.query.all()]
    #     super().__init__(*args,**kwargs)


class UserAddForm (FlaskForm):
    '''管理员添加表单'''
    username = StringField (
        label = "管理员名称",
        validators = [DataRequired ("请输入管理员名称!")],description = "管理员名称",
        render_kw = {"class":"form-control","placeholder":"请输入管理员名称!"}
    )
    password = PasswordField (
        label = "管理员密码",
        validators = [DataRequired ("请输入管理员密码!")],description = "管理员密码!",
        render_kw = {"class":"form-control","placeholder":"请输入管理员密码!"}
    )
    repwd = PasswordField(
        label="管理员重复密码",
        validators=[DataRequired("请输入管理员重复密码！"),EqualTo('password', message="两次密码不一致！")],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员重复密码！",
        }
    )
    email = StringField (
        label = "邮箱",
        validators = [DataRequired ("邮箱不能为空!"),Email ("邮箱格式不正确!")],
        render_kw = {"class":"form-control","placeholder":"请输入邮箱!"}
    )
    role_id = SelectMultipleField (
        label = "所属角色",
        coerce = int,
        choices = [(v.id,v.name) for v in Role.query.all ()],render_kw = {"class":"form-control"}
    )
    submit = SubmitField (
        "提交",
        render_kw = {"class":"btn btn-primary"}
    )


class RoleAddForm (FlaskForm):
    '''角色添加表单'''
    name = StringField (label = "角色名称",validators = [DataRequired ("角色不能为空!")],
                        render_kw = {"class":"form-control","placeholder":"请输入角色名称!"})

    auth_id = SelectMultipleField (
        label = "角色权限",
        coerce = int,
        choices = [(v.id,v.name) for v in Auth.query.all ()],render_kw = {"class":"form-control"}
    )
    submit = SubmitField ("提交",render_kw = {"class":"btn btn-primary"})

class xxx(SelectField):

    def pre_validate (self,form):
        pass


class AuthAddForm (FlaskForm):
    '''权限添加表单'''
    name = StringField (
        label = "权限名称",validators = [DataRequired ("请输入权限名称!")],
        render_kw = {"class":"form-control","placeholder":"请输入权限名称!"}
    )
    url = StringField (
        label = "权限地址",validators = [DataRequired ("请输入权限地址!")],
        render_kw = {"class":"form-control","placeholder":"请输入权限地址!"}
    )
    code = StringField (
        label = "权限代码",validators = [DataRequired ("请输入权限代码名称!")],
        render_kw = {"class":"form-control","placeholder":"请输入权限代码!"}
    )

    auth_id = xxx(
        label = "所属权限",coerce = int,
        description = "所属权限id,自关联",
        choices = [(v.id,v.name) for v in Auth.query.all ()],
              render_kw = {"class":"form-control"})
    group_id = SelectField (
        label = "所属组",validators = [DataRequired ("请选择所属组!")],coerce = int,
        choices = [(v.id,v.name) for v in Group.query.all ()],render_kw = {"class":"form-control"}
    )
    submit = SubmitField ("提交",render_kw = {"class":"btn btn-primary"})


