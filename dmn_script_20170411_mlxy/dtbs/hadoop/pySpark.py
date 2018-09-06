#-*- coding:utf-8 -*-
from impala.dbapi import connect
# impyla连接
def impylaConnect(host,port):
    try:
        conn = connect(host,port)
        #transport.append(pySpark.impylaConnect("10.26.8.132", 21051))
        #cursor = conn.cursor()
        print "impyla connect success."
        #return conn,cursor
        return conn
    except Exception,ex:
        print Exception,":",ex
        print "hadoopSpark connect fail, Game Over."
        return -1
    
def impylaClose(conn):
    try:
        conn.close()
        print "impylaSpark is closed."
    except Exception,ex:
        print Exception,":",ex
        print "hadoopSpark close fail."

def impylaGetMessage(conn,sql):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            message = cursor.fetchall() 
            #cursor.close()
            return message
    except Exception,ex:
        print Exception,":",ex
        print "hadoopSpark get message fail:",sql
        return -1
