#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-29,20:12"
from flask import current_app


def init_permission(user,session):
    '''
    获取权限信息列表，放入session中
    :param user: 当前登录用户
    :param request: 请求
    :param session: 会话
    :return:
    '''
    permission_list = []
    for role in user.roles:
        for auth in role.auths:
            tmp = {}
            tmp["auth_id"] = auth.id#权限
            tmp["auth_name"] = auth.name#权限名称
            tmp["auth_url"] = auth.url#权限url
            tmp["auth_code"] = auth.code#权限代码
            tmp["auth_group_id"] = auth.group_id#权限所属组id
            tmp["auth_menu_gp_id"] = auth.menu_gp_id#自关联id
            tmp["auth_menu_id"] = auth.group.menu.id#菜单id
            tmp["auth_menu_name"] = auth.group.menu.name#菜单名称
            permission_list.append(tmp)



    sub_permission = []
    for item in permission_list:
        tpl = {
            "id":item ["auth_id"],
            "title":item ["auth_name"],
            "url":item ["auth_url"],
            "menu_gp_id":item ["auth_menu_gp_id"],
            "menu_id":item ["auth_menu_id"],
            "menu_title":item ["auth_menu_name"]
        }
        sub_permission.append (tpl)

    sub_permissions = []
    for item in sub_permission:
        if item not in sub_permissions:
            sub_permissions.append(item)
    session[current_app.config["PERMISSION_MENU_KEY"]] = sub_permissions


    result = {}
    for item in permission_list:
        group_id = item["auth_group_id"]
        code = item["auth_code"]
        url = item["auth_url"]

        if group_id in result:
            result[group_id]["codes"].append(code)
            result[group_id]["urls"].append(url)
        else:
            result[group_id] = {
                "codes":[code,],
                "urls":[url,]
            }
    session[current_app.config["PERMISSION_URL_DICT_KEY"]] = result