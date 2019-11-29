# -*- coding:utf-8 -*-
# 涉及的三方库：pymysql
# pip3 install pymysql
import os
import pymysql
import code_generator.generator_config as config

class ConfigurationParser(object):
    def __init__(self, ):
        pass

    def parseConfiguration(self):
        jdbcConnectionDict= {}
        jdbcConnectionDict['host']= config.HOST
        jdbcConnectionDict['port'] = config.PORT
        jdbcConnectionDict['database'] =config.DATABASE
        jdbcConnectionDict['user'] =config.USER
        jdbcConnectionDict['password'] =config.PASSWORD
        jdbcConnectionDict['charset'] =config.CHARSET
        jdbcConnectionDict['creator'] = pymysql
        jdbcConnectionDict['mincached'] =0
        jdbcConnectionDict['maxcached'] =10
        jdbcConnectionDict['maxshared'] =0
        jdbcConnectionDict['maxconnections'] =20
        return jdbcConnectionDict

if __name__ == "__main__":
    print(ConfigurationParser().parseConfiguration())