from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError
from model.db.zd_grant import ZdGrant
from conf.settings import SUPERUSERS
from conf import log
import sys




class ZookeeperConfError(Exception):
    pass



def has_permission(username, cluster_name, path):
        isSuperUser = username in SUPERUSERS 
        if isSuperUser:
            return True
        sql_tpl = ("SELECT cluster_name, path, tousername from zd_grant where tousername='{0}' and cluster_name='{1}' and deleted=0 order by cluster_name, path")
        sql = sql_tpl.format(username, cluster_name, path)
        grants = ZdGrant.raw(sql)
        for g in grants:
            if path.find(g.path) == 0:
                return True

        return False




if __name__ == '__main__':
    pass
