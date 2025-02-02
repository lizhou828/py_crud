# -*- coding:utf-8 -*-
# 涉及的三方库：DBUtils
# pip3 install DBUtils
import math

import pymysql
import time
import json

from DBUtils.PooledDB import PooledDB

# 引入同一目录下的py文件（来自指定py文件下，导入该文件下的某个类）
from code_generator.result.DB.ConfigurationParser import ConfigurationParser
from code_generator.result.DB.QueryUtil import QueryUtil
from code_generator.result.DB.Logger import Logger
from code_generator.result.DB.Page import Page




global PRIMARY_KEY_DICT_LIST
PRIMARY_KEY_DICT_LIST = []

class BaseDao(object):
    """
    Python 操作数据库基类方法
    - @Author RuanCheng
    - @UpdateDate 2017/5/17
    """
    __logger = None
    __parser = None                 # 获取 xml 文件信息对象
    __poolConfigDict = None         # 从 xml 中获取的数据库连接信息的字典对象
    __pool = None                   # 数据库连接池
    __obj = None                    # 实体类
    __className = None              # 实体类类名
    __tableName = None              # 实体类对应的数据库名
    __primaryKeyDict = {}           # 数据库表的主键字典对象
    __columnList = []

    def __init__(self, obj=None):
        """
        初始化方法：
        - 1.初始化配置信息
        - 2.初始化 className
        - 3.初始化数据库表的主键
        """
        if not obj:
            raise Exception("BaseDao is missing a required parameter --> obj(class object).\nFor example [super().__init__(User)].")
        else:
            self.__logger = Logger(self.__class__)                                      # 初始化日志对象
            self.__logger.start()                                                       # 开启日志

            if not self.__parser:                                                       # 解析 xml
                self.__parser = ConfigurationParser()
                self.__poolConfigDict = self.__parser.parseConfiguration()
                print(self.__poolConfigDict)

                # 用于传递到数据库的准备会话，如 [”set name UTF-8″] 。
                self.__pool = PooledDB(**self.__poolConfigDict)
                # setsession = "set name UTF-8"


            # 初始化参数
            if (self.__obj == None) or ( self.__obj != obj):
                global PRIMARY_KEY_DICT_LIST
                if (not PRIMARY_KEY_DICT_LIST) or (PRIMARY_KEY_DICT_LIST.count == 0):
                    self.__init_primary_key_dict_list()                                 # 初始化主键字典列表
                self.__init_params(obj)                                                 # 初始化参数
                self.__init_columns()                                                   # 初始化字段列表
                self.__logger.end()                                                     # 结束日志
        pass





    ################################################# 外部调用方法 #################################################


    def selectAll(self):
        """
        查询所有
        """
        sql = QueryUtil.selectAll(self.__tableName, self.__columnList)
        return self.executeQuery(sql)

    def selectByPK(self, value):
        """
        按主键查询
        - @Param: value 主键
        """
        if (not value) or (value == ""):
            raise Exception("selectByPrimaryKey() is missing a required paramter 'value'.")
        sql = QueryUtil.selectByPK(self.__primaryKeyDict, value, self.__columnList)
        result_list = self.executeQuery(sql)
        if result_list and len(result_list) == 1:
            return result_list[0]
        else:
            return None

    def selectCount(self):
        """
        查询总记录数
        """
        sql = QueryUtil.selectCount(self.__tableName)
        return self.execute(sql)[0][0]

    def selectByProperties(self, obj):
        """
        条件查询
        """
        sql = QueryUtil.selectByProperties(self.__tableName, json.loads(str(obj)))
        if (not sql) or sql == "" or len(sql) == 0 or (not isinstance(sql, str)):
            self.__logger.outMsg("Generate sql failed!!!!")
            return 0
        return self.executeQuery(sql, logEnable=True)

    def selectAllByPage(self, pageNum=1, limit=10):
        """
        分页查询
        """
        page = Page()
        page.set_page(pageNum)
        page.set_limit(limit)
        total_count = self.selectCount()
        page.set_total_count(total_count)
        if total_count % limit == 0:
            total_page = total_count / limit
        else:
            total_page = math.ceil(total_count / limit)
        page.set_total_page(total_page)
        page.set_begin((pageNum - 1) * limit)

        if (not page) or (not isinstance(page,Page)):
            raise Exception("Paramter [page] is not correct. Parameter [page] must a Page object instance. ")
        sql = QueryUtil.selectAllByPage(self.__tableName, self.__columnList, page)
        return self.executeQuery(sql, logEnable=True)

    def insert(self, obj):
        """
        新增
        - @Param: obj 实体对象
        """
        if (not obj) or (obj == ""):
            raise Exception("insert() is missing a required paramter 'obj'.")
        sql = QueryUtil.insert(self.__primaryKeyDict, json.loads(str(obj)))
        return self.__executeUpdate(sql)

    def delete(self, obj=None):
        """
        根据实体删除
        - @Param: obj 实体对象
        """
        if (not obj) or (obj == ""):
            raise Exception("delete() is missing a required paramter 'obj'.")
        sql = QueryUtil.delete(self.__primaryKeyDict, json.loads(str(obj)))
        return self.__executeUpdate(sql)

    def deleteByPK(self, value=None):
        """
        根据主键删除
        - @Param: value 主键
        """
        if (not value) or (value == ""):
            raise Exception("deleteByPrimaryKey() is missing a required paramter 'value'.")
        sql = QueryUtil.deleteByPK(self.__primaryKeyDict, value)
        return self.__executeUpdate(sql)

    def updateByPK(self, obj=None):
        """
        根据主键更新
        - @Param: obj 实体对象
        """
        if (not obj) or (obj == ""):
            raise Exception("updateByPrimaryKey() is missing a required paramter 'obj'.")
        sql = QueryUtil.updateByPK(self.__primaryKeyDict, json.loads(str(obj)))
        return self.__executeUpdate(sql)









    ################################################# 内部调用方法 #################################################
    def execute_with_dict(self, sql="", logEnable=True):
        """
        执行 SQL 语句，返回dict数据
        - @Param: sql 执行sql
        - @Param: logEnable 是否开启输出日志
        - @return 查询结果
        """
        if not sql:
            raise Exception("Execute method is missing a required parameter --> sql.")
        try:
            self.__logger.outSQL(sql, enable=logEnable)
            conn = self.__pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            columns = cur.description # 获取列名信息
            resultList = []
            for row in result:
                obj = {}
                for index in range(len(row)):
                    obj[columns[index][0]] = row[index]
                resultList.append(obj)
            return resultList
        except Exception as e:
            # 判断变量是否定义
            if 'conn' in dir():
                conn.rollback()
            raise Exception(e)
        finally:
            # 判断变量是否定义
            if 'cur' in dir():
                cur.close()

            if 'conn' in dir():
                conn.close()
            pass

    def execute(self, sql="", logEnable=True):
        """
        执行 SQL 语句，返回结果集数据
        - @Param: sql 执行sql
        - @Param: logEnable 是否开启输出日志
        - @return 查询结果
        """
        if not sql:
            raise Exception("Execute method is missing a required parameter --> sql.")
        try:
            self.__logger.outSQL(sql, enable=logEnable)
            conn = self.__pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            resultList = []
            for r in result:
                resultList.append(r)
            return resultList
        except Exception as e:
            # 判断变量是否定义
            if 'conn' in dir():
                conn.rollback()
            raise Exception(e)
        finally:
            # 判断变量是否定义
            if 'cur' in dir():
                cur.close()

            if 'conn' in dir():
                conn.close()
            pass

    def executeQuery(self, sql="", logEnable=True):
        """
        执行查询 SQL 语句,返回对象数据
        - @Param: sql 执行sql
        - @Param: logEnable 是否开启输出日志
        - @return 查询结果
        """
        if not sql:
            raise Exception("Execute method is missing a required parameter --> sql.")
        try:
            self.__logger.outSQL(sql, enable=logEnable)
            conn = self.__pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            resultTuple = cur.fetchall()
            resultList = list(resultTuple)
            objList = []

            for result in resultList:
                i = 0
                obj = self.__obj()
                for col in self.__columnList:
                    # 如果是实例下的私有属性的话，则必须通过 "_类名__私有属性" 的方式给私有属性赋值
                    # prop = '_%s__%s'%(self.__className, col)
                    # setattr(obj, prop, result[i])

                    # 如果是实例属性，则用下面的方式处理：
                    setattr(obj, col, result[i])
                    i += 1
                objList.append(obj)
            if not objList:
                return None
            else:
                return objList
        except Exception as e:
            conn.rollback()
            raise Exception(e)
        finally:
            cur.close()
            conn.close()
            pass

    def __executeUpdate(self, sql=None, logEnable=True):
        """
        执行修改 SQL 语句：
        - @Param: sql 执行sql
        - @Param: logEnable 是否开启输出日志
        - @return 影响行数
        """
        try:
            self.__logger.outSQL(sql, enable=logEnable)
            conn = self.__pool.connection()
            cur = conn.cursor()
            result = cur.execute(sql)
            conn.commit()
            if "INSERT INTO" in sql:
                return cur.lastrowid
            else:
                return result
        except Exception as e:
            conn.rollback()
            raise Exception(e)
            pass
        finally:
            cur.close()
            conn.close()
            pass

    def __init_params(self, obj):
        """
        初始化参数
        - @Param：obj class 对象
        """
        self.__obj = obj
        self.__className = obj.__name__
        for i in PRIMARY_KEY_DICT_LIST:
            if i.get("className") == self.__className:
                self.__primaryKeyDict = i
                self.__className = i["className"]
                self.__tableName = i["tableName"]
                break

    def __init_primary_key_dict_list(self):
        """
        初始化数据库主键集合：
        - pk_dict = {"className": {"tableName":tableName,"primaryKey":primaryKey,"auto_increment":auto_increment}}
        """
        global PRIMARY_KEY_DICT_LIST
        sql = """
            SELECT
                t.TABLE_NAME,
                c.COLUMN_NAME,
                c.ORDINAL_POSITION
            FROM
                INFORMATION_SCHEMA.TABLE_CONSTRAINTS as t,
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS c
            WHERE t.TABLE_NAME = c.TABLE_NAME
                AND t.TABLE_SCHEMA = "%s"
                AND c.CONSTRAINT_SCHEMA = "%s"
        """ % (self.__poolConfigDict.get("database"),self.__poolConfigDict.get("database"))
        resultList = self.execute(sql, logEnable=False)
        for result in resultList:
            pk_dict = dict()
            pk_dict["tableName"] = result[0]
            pk_dict["primaryKey"] = result[1]
            pk_dict["ordinalPosition"] = result[2]
            pk_dict["className"] = self.__convertToClassName(result[0])
            PRIMARY_KEY_DICT_LIST.append(pk_dict)
        self.__logger.outMsg("initPrimaryKey is done.")

    def __init_columns(self):
        """
        初始化表字段
        """
        self.__columnList = []
        sql = "SELECT column_name FROM  Information_schema.columns WHERE table_Name = '%s' AND TABLE_SCHEMA='%s'" % (self.__tableName, self.__poolConfigDict["database"])
        resultList = self.execute(sql, logEnable=False)
        for result in resultList:
            self.__columnList.append(result[0])
        self.__logger.outMsg("init_columns is done.")
        # print(self.__columnList)
        pass

    def __convertToClassName(self, tableName):
        """
        表名转换方法：
        - @Param: tableName 表名
        - @return 转换后的类名
        """
        result = None
        if tableName.startswith("t_"):
            result = tableName.replace("t_","").lower()
        else:
            result = tableName
        return result.capitalize()