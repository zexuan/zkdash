#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014,掌阅科技
All rights reserved.

摘    要: index.py
创 建 者: zhuangshixiong
创建日期: 2015-10-09
"""
from handler.bases import CommonBaseHandler
from lib import route
import tornado
from tornado.web import authenticated
from model.db.zd_user import ZdUser


@route(r'/')
class IndexHandler(CommonBaseHandler):

    '''配置管理系统页面入口
    '''

    @authenticated
    def get(self):
        return self.render('index.html')



@route(r'/auth/index/main', '首页')
class IndexMainHandler(CommonBaseHandler):

    '''首页
    '''

    @authenticated
    def response(self):
        return self.finish()


@route(r'/auth/login/', '首页')
@route(r'/auth/login', '首页')
class AuthLoginHandler(CommonBaseHandler):

    '''首页
    '''

    def get(self):
        try:
            self.write(self.current_user)
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", errormessage = errormessage)


    def check_permission(self, password, username):
        records = ZdUser.select().where(ZdUser.username == username and ZdUser.password == password)
        count = records.count()
        if count > 0:
            return True
        return False

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        self.write("username: " + username)
        self.write("password: " + password)
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect("/")
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/auth/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

