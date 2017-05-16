#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
Copyright (c) 2014,掌阅科技
All rights reserved.

摘    要: zd_znode.py
创 建 者: zhuangshixiong
创建日期: 2015-06-16
"""
from peewee import CharField
from peewee import IntegerField
from peewee import SQL

from model.db.base import ZKDASH_DB, EnumField


class ZdUser(ZKDASH_DB.Model):

    """ZdZnode Model
    """

    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    username = CharField(max_length=64, null=True)
    password = CharField(max_length=512, null=True)

    class Meta(object):

        """表配置信息
        """
        db_table = "zd_user"
