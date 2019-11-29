# -*- coding:utf-8 -*-
# 涉及的三方库：pymysql
# pip3 install pymysql
import os
import pymysql


# 把顶级app.logger放到代理中，方便其他组件调用，如蓝图
from flask import current_app
from werkzeug.local import LocalProxy

logger = LocalProxy(lambda: current_app.logger)

import importlib

# 找出环境变量，动态导入模块
profile = os.environ.get("profile")
if not profile:
    profile = "test"
module_name = 'config.' + profile + '_config'
config = importlib.import_module(module_name)


class ConfigurationParser(object):
    def __init__(self, ):
        pass

    def parseConfiguration(self):
        jdbcConnectionDict= {}
        jdbcConnectionDict['host']= config.DB_HOST
        jdbcConnectionDict['port'] = config.DB_PORT
        jdbcConnectionDict['database'] =config.DB_DATABASE
        jdbcConnectionDict['user'] =config.DB_USER
        jdbcConnectionDict['password'] =config.DB_PASSWORD
        jdbcConnectionDict['charset'] =config.DB_CHARSET
        jdbcConnectionDict['creator'] = pymysql
        jdbcConnectionDict['mincached'] =0
        jdbcConnectionDict['maxcached'] =10
        jdbcConnectionDict['maxshared'] =0
        jdbcConnectionDict['maxconnections'] =20
        return jdbcConnectionDict

if __name__ == "__main__":
    print(ConfigurationParser().parseConfiguration())