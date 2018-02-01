#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2018-01-31,14:04"

class Base_permission_list(object):
    def __init__(self,code_list):
        self.code_list = code_list

    def has_add(self):
        if "add" in self.code_list:
            return True

    def has_edit(self):
        if "edit" in self.code_list:
            return True

    def has_delete(self):
        if "delete" in self.code_list:
            return True

