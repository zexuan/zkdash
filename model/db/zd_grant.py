from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import SQL

from model.db.base import ZKDASH_DB, EnumField


class ZdGrant(ZKDASH_DB.Model):

    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    fromusername = CharField(max_length=128)
    tousername = CharField(max_length=128)
    cluster_name = CharField(max_length=128)
    path = CharField(max_length=255)
    ctime = DateTimeField(null=True)
    deleted = EnumField(enum_value="'0', '1'", constraints=[SQL("DEFAULT '0'")])

    class Meta(object):
        db_table = "zd_grant"
