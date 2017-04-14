#encoding:utf-8
'''
@author: Lisen
Created on 2017年4月12日
--------Changed on 2017年4月14日----------
Using OOP method to replace the functions
------------------------------------------
@author: Lisen
'''
import MySQLdb

class Conn(object):
    """
   Class for database connection
    ATTR:  db:      database connection
           cursor:  cursor for current connection db
    FUNC:  query_sql
           exce_sql
           exist_check
           db_close
    INIT:  db_open_connect
    """
    def __init__(self, host, user, pwd, schema):
        """
        Initialize the database connection when create an object
        @param host:   database ip 
        @param user:   database user
        @param pwd:    database user password
        @param schema: database specific schema
        """
        self.db = MySQLdb.connect(host, user, pwd, schema, charset='utf8')
        self.cursor = self.db.cursor()
    
    # query sql 
    def query_sql(self, sql):
        """
        Using sql string to query specific database table
        @param self: instance
        @param sql:  sql string to be executed for querying data  
        """
        try:
            self.cursor.execute(sql)
        except Exception, e:
            print "Woops, error %s" % str(e) + "when querying database using " \
                                                                        + sql
        else:
            return self.cursor.fetchall()
            
            
    def exec_sql(self, sql):
        """
        Executing insert/update/alter actions using sql string
        @param self: instance
        @param sql:  sql string to be executed 
        """
        try:
            self.cursor.execute(sql)
        except Exception, e:
            print "Woops, error %s" % str(e) + "when querying database using " \
                                                                        + sql
            self.db.rollback()
        else:
            self.db.commit()
    
    
    def check_exist(self, sql):
        """
        Checking duplication before changing database table's records
        @param self: instance
        @param sql:  sql string to be checked 
        """ 
        try:
            check_result = self.query_sql(sql)
        except Exception, e:
            print "Woops, error %s" % str(e) + "when querying database using " \
                                                                        + sql
        else:
            if len(check_result):
                return True
            else:
                return False


    def close(self):
        """
        Close database connection
        @param self: instance 
        """
        self.db.close()
