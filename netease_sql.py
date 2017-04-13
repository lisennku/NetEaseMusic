#encoding:utf-8
'''
Created on 2017年4月12日

@author: Lisen
'''
import MySQLdb
import getconfig
from __builtin__ import str

host = getconfig.host
user = getconfig.user
pwd  = getconfig.pwd
schema = getconfig.schema

db = MySQLdb.connect(host, user, pwd, schema, charset = 'utf8')
db_cursor = db.cursor()

# execute sql
def execute_sql(sql_string):
    global db
    global db_cursor
    '''
     执行SQL语句
    @param db: object for database connection 
    @param db_cursor: database cursor for specified schema.table
    @param sql_string: sql dml string
    '''    
    try:
        db_cursor.execute(sql_string)
        db.commit()
    except Exception,e:
        print "Error in %s" % e
        db.rollback()

# check exist
def check_exist(sql_string):
    global db
    global db_cursor
    ''' 
   查看是否已经在数据库中
    @param db: object for database connection 
    @param db_cursor: database cursor for specified schema.table
    @param sql_string: sql dml string
    @return: flag to indicate if the record exists in the table
    '''
    res_len = len(query_sql(sql_string))
    if res_len > 0:
        return True    # 在数据库中
    else:
        return False   # 不在数据库中
    return

# query data
def query_sql(sql_string):
    global db
    global db_cursor
    '''
    查询SQL
    @param db: object for database connection 
    @param db_cursor: database cursor for specified schema.table
    @param sql_string: sql dml string
    @return: sql queries result
    '''
    try:
        db_cursor.execute(sql_string)
        result = db_cursor.fetchall()
        return result
    except Exception, e:
        print "Error in %s" % e

def close():
    db.close()


def esccape_str(str):
    return MySQLdb.escape_string(str)












