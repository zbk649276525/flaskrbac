#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-25,14:01"
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,SubmitField,SelectField,widgets
from app.models import Menu




class MenuForm(FlaskForm):
    '''菜单表单'''
    name = StringField(label = "菜单名称",validators = [DataRequired("菜单不能为空!")],
                       render_kw = {"class":"form-control","placeholder":"请输入菜单名称!"})
    submit = SubmitField("提交",render_kw = {"class":"btn btn-primary"})

class GroupForm(FlaskForm):
    '''分组表单'''
    name = StringField(label = "组名称",validators = [DataRequired("组名称不能为空!")],
                       render_kw = {"class":"form-control","placeholder":"请输入组名称!"})
    menu_id = SelectField(label = "所属菜单",validators = [DataRequired("请选择菜单!")],coerce = int,
                         choices = [(v.id,v.name) for v in Menu.query.all()],render_kw = {"class":"form-control"})
    submit = SubmitField("提交",render_kw = {"class":"btn btn-primary"})

    # def __init__(self,*args,**kwargs):
    #     self.menu_id.choices = [(v.id,v.name) for v in Menu.query.all()]
    #     super().__init__(*args,**kwargs)