#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-30,15:51"


import re
from flask import session,current_app,request

def menu_html():
    '''
    去session中获取菜单相关信息，匹配当前url,生成菜单
    :param request:
    :return:
    '''
    menu_list = session[current_app.config["PERMISSION_MENU_KEY"]]
    current_url = request.path

    menu_dict = {}

    for item in menu_list:
        if not item["menu_gp_id"]:  #说明是菜单
            menu_dict[item["id"]] = item # 以id 为健，item本身为value构建字典




    for item in menu_list:
        regex = "^{0}$".format(item["url"])
        if re.match(regex,current_url):
            menu_gp_id = item["menu_gp_id"]
            if menu_gp_id:
                menu_dict[menu_gp_id]["active"] = True #如果有id 表名不是菜单，找到这个menu_gp_id 对应的value给它加上active = True
            else:
                #如果没有id,表名本身就是菜单(注意，这里是通过item["id"]来找到这个健的），直接加active = True
                menu_dict[item["id"]]["active"] = True

    result = {}
    for item in menu_dict.values():
        active = item.get("active")
        menu_id = item["menu_id"]
        if menu_id in result:
            result[menu_id]["children"].append( {"title":item["title"],"url":item["url"],"active":active})
        else:
            result[menu_id] = {
                "menu_id":item["menu_id"],
                "menu_title":item["menu_title"],
                "active":active,
                "children":[
                    {"title":item["title"],"url":item["url"],"active":active}
                ]

            }
    return result