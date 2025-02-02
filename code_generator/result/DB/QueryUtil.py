# -*- coding:utf-8 -*-
# 拼接 SQL 语句的工具类。

# 引入同一目录下的py文件
from code_generator.result.DB.Page import Page

class QueryUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def queryColumns(columnList):
        i = 1
        s = ""
        for col in columnList:
            if i != 1:
                s += ", `%s`" % (col)
            else:
                s += "`%s`" % (col)
            i += 1
        return s

    @staticmethod
    def selectByPK(primaryKeyDict, value, columnList):
        """
        拼接主键查询
        """
        sql = 'SELECT %s FROM `%s` WHERE `%s`="%s"'%(QueryUtil.queryColumns(columnList), primaryKeyDict["tableName"], primaryKeyDict["primaryKey"], str(value))
        return sql

    @staticmethod
    def selectAll(tableName, columnList):
        """
        拼接查询所有
        """
        return 'SELECT %s FROM %s'%(QueryUtil.queryColumns(columnList), tableName)

    @staticmethod
    def selectCount(tableName):
        """
        拼接查询记录数
        """
        return 'SELECT COUNT(*) FROM %s'%(tableName)

    @staticmethod
    def selectByProperties(tableName, objDict):
        """
        条件查询
        """
        if (not objDict) or (len(objDict) == 0) or (not isinstance(objDict, dict)):
            return 'SELECT * FROM %s' % (tableName)
        else:
            sql = "SELECT * FROM  `%s` where " % (tableName)
            i = 0
            for key, value in objDict.items():
                if (not value) or (value == None) or (value == "None"):
                    continue
                if i == 0:
                    sql += key + "='" + str(value) + "'"
                    i += 1
                else:
                    sql += " and " + key + "='" + str(value) + "'"
            return sql

    @staticmethod
    def selectAllByPage(tableName, columnList, page=None):
        """
        拼接分页查询
        """
        if not page:
            page = Page()
        return 'SELECT %s FROM %s LIMIT %d,%d'%(QueryUtil.queryColumns(columnList), tableName, page.get_begin(), page.get_limit())


    @staticmethod
    def insert(primaryKeyDict, objDict):
        """
        拼接新增
        """
        tableName = primaryKeyDict["tableName"]
        key = primaryKeyDict["primaryKey"]
        columns = list(objDict.keys())
        values = list(objDict.values())

        sql = "INSERT INTO `%s`(" % (tableName)
        for i in range(0, columns.__len__()):
            if i == 0:
                sql += '`%s`'%(columns[i])
            else:
                sql += ',`%s`'%(columns[i])
        sql += ') VALUES('
        for i in range(0, values.__len__()):
            if values[i] == None or values[i] == "None":
                value = "null"
            else:
                value = '"%s"'%(values[i])
            if i == 0:
                sql += value
            else:
                sql += ',%s'%(value);
        sql += ')'
        return sql

    @staticmethod
    def delete(primaryKeyDict, objDict):
        """
        拼接删除
        """
        tableName = primaryKeyDict["tableName"]
        key = primaryKeyDict["primaryKey"]
        columns = list(objDict.keys())
        values = list(objDict.values())

        sql = "DELETE FROM `%s` WHERE 1=1 " % (tableName)
        for i in range(0, values.__len__()):
            if values[i] != None and values[i] != "None":
                sql += 'and `%s`="%s"'%(columns[i], values[i])
        return sql

    @staticmethod
    def deleteByPK(primaryKeyDict, value=None):
        """
        拼接根据主键删除
        """
        sql = 'DELETE FROM `%s` WHERE `%s`="%s"'%(primaryKeyDict["tableName"], primaryKeyDict["primaryKey"], value)
        return sql

    @staticmethod
    def updateByPK(primaryKeyDict, objDict):
        """
        拼接根据主键更新
        UPDATE t_user SET name='test' WHERE id = 1007
        """
        tableName = primaryKeyDict["tableName"]
        key = primaryKeyDict["primaryKey"]
        columns = list(objDict.keys())
        values = list(objDict.values())
        keyValue = None
        sql = "UPDATE `%s` SET" % (tableName)
        for i in range(0, columns.__len__()):
            if (values[i] != None) and (values[i] != "None"):
                if columns[i] != key:
                    sql += ' `%s`="%s", '%(columns[i], values[i])
                else:
                    keyValue = values[i]
        sql = sql[0:len(sql)-2] + ' WHERE `%s`="%s"'%(key, keyValue)
        return sql