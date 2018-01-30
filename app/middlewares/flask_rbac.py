#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-29,22:40"
import re
from app.admin import admin
from flask import request,current_app,session,redirect,url_for


@admin.before_app_request
def process_request():
    current_url = request.path
    VALID_URL = current_app.config["VALID_URL"]

    print(current_url)
    #当前请求的url不需要执行验证的（白名单），在config中设置
    for url in  VALID_URL:
        print(session)
        regex = "^{0}$".format (url) #加上正则
        if re.match (regex,current_url): # 将白名单的url和当前用户请求的url匹配
            return None#return None 表示继续往内层中间件走

    permission_dict = session.get(current_app.config["PERMISSION_URL_DICT_KEY"])#获取放置在session中的当前用户的权限
    print(permission_dict)
    if not permission_dict:#如果session中没有值，说明用户还未登陆，跳转到登录页面
        return redirect (url_for("admin.login"))
    flag = False#设置 标志位
    for group_id,code_url in permission_dict.items ():
        for db_url in code_url ["urls"]:
            regex = "^{0}$".format (db_url)  # 加上正则
            if re.match (regex,current_url):
                request.permission_code_list = code_url ["codes"] # 主动给request中添加一个permission_code_list
                flag = True

                break
        if flag:
            break
    if not flag:
        return "无权访问"