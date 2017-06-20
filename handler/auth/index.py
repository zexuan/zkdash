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
from model.db.zd_grant import ZdGrant
from handler.bases import ArgsMap
from service import zookeeper as ZookeeperService
from kazoo.exceptions import NoNodeError
from datetime import datetime
from conf.settings import SUPERUSERS


@route(r'/')
class IndexHandler(CommonBaseHandler):

    '''配置管理系统页面入口
    '''

    @authenticated
    def get(self):
        isSuperUser = self.current_user in SUPERUSERS 
        return self.render('index.html', isSuperUser=isSuperUser)



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
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect("/")
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/auth/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", str(user))
        else:
            self.clear_cookie("user")


@route(r'/auth/grant')
class GrantHandler(CommonBaseHandler):
    '''index, 查看
    '''
    args_list = [
            ArgsMap('pageSize', 'page_size', default=30),
            ArgsMap('pageCurrent', 'current_page', default=1),
            ArgsMap('orderDirection', 'order_direction', default="asc"),
            ArgsMap('orderField', 'order_field', default="id"),
            ]

    @authenticated
    def response(self):
        username = self.current_user
        sql_tpl = ("SELECT username  from zd_user where username<>'{0}' order by username")

        sql = sql_tpl.format(username)
        records = ZdUser.raw(sql)

        self.render('grant.html',
                action='/auth/grant/save',
                records=records,
                )


    def post(self):
            self.redirect("/")

@route(r'/auth/grant/resource')
class GrantResouceHandler(CommonBaseHandler):
    '''index, 查看
    '''
    args_list = [
            ArgsMap('pageSize', 'page_size', default=30),
            ArgsMap('pageCurrent', 'current_page', default=1),
            ArgsMap('orderDirection', 'order_direction', default="asc"),
            ArgsMap('orderField', 'order_field', default="id"),
            ]

    @authenticated
    def response(self):
        username = self.current_user
        sql_tpl = ("SELECT distinct cluster_name, path from zd_grant where tousername='{0}' and deleted=0 order by cluster_name, path")
        sql = sql_tpl.format(username)
        grants = ZdGrant.raw(sql)


        self.render('grant_resource.html',
                action='/auth/grant',
                grants=grants
                )


@route(r'/auth/grant/save')
class ZdGrantSaveHandler(CommonBaseHandler):

    args_list = [
        ArgsMap('tousername', required=True),
        ArgsMap('cluster_name', required=True),
        ArgsMap('path', required=True),
        ArgsMap('child_path', default=""),
    ]

    @authenticated
    def response(self):
        self.child_path = self.child_path.rstrip("/")
        path = self.path + self.child_path
        if path == "/":
            return self.ajax_popup(close_current=False, code=300, msg="不能授权根目录")

        try:
            data = ZookeeperService.get(self.cluster_name, path)
        except NoNodeError as exc:
            return self.ajax_popup(close_current=False, code=300, msg="保存失败！")

        self_username = self.current_user
        sql_tpl = ("SELECT cluster_name, path, tousername from zd_grant where tousername='{0}' and cluster_name='{1}' and path='{2}' and deleted=0 order by cluster_name, path")
        sql = sql_tpl.format(self.tousername, self.cluster_name, path)
        grants = ZdGrant.raw(sql)

        i = 0
        for g in grants:
            i=1;
            break;
        if i==1:
            return self.ajax_ok(close_current=False)



        grant = ZdGrant(fromusername=self_username,
                tousername=self.tousername,
                cluster_name=self.cluster_name,
                path=path,
                ctime=datetime.now(),
                deleted=0)
        grant.save()
        return self.ajax_ok(close_current=False)
