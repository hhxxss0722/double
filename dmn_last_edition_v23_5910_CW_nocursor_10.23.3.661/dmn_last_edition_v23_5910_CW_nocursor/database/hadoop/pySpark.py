#-*- coding:utf-8 -*-
#import pyhs2

# hadoopSpark 连接

def hadoopConnect(hadoop_ip,hadoop_port,hadoop_name,hadoop_pw,hadoop_database,hadoop_authMechanism):
    try:
        conn = pyhs2.connect(host=hadoop_ip,
                            port=hadoop_port,
                            authMechanism=hadoop_authMechanism,
                            user=hadoop_name,
                            password=hadoop_pw,
                            database=hadoop_database,
                            )
        
        print 'hadoopSpark connect success.'
        return conn
    except Exception,ex:
        print Exception,":",ex
        print 'hadoopSpark connect fail, Game Over.'
        return -1

# hadoopSpark 关闭

def hadoopClose(conn,cursor):
    try:
        cursor.close()
        conn.close()
        print 'hadoopSpark is closed.'
    except Exception,ex:
        print Exception,":",ex
        print 'hadoopSpark close fail.'

# hadoopSpark 获取设备数据

def hadoopGetMessage(conn,sql):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            message = cursor.fetchall() 
            cursor.close()
            return message
    except Exception,ex:
        print Exception,":",ex
        print 'hadoopSpark get message fail:',sql
        return -1

from impala.dbapi import connect
# impyla连接
def impylaConnect(host,port):
    try:
        conn = connect(host,port)
        #cursor = conn.cursor()
        print 'impyla connect success.'
        #return conn,cursor
        return conn
    except Exception,ex:
        print Exception,":",ex
        print 'hadoopSpark connect fail, Game Over.'
        return -1
    
def impylaClose(conn):
    try:
        conn.close()
        print 'impylaSpark is closed.'
    except Exception,ex:
        print Exception,":",ex
        print 'hadoopSpark close fail.'

def impylaGetMessage(conn,sql):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            message = cursor.fetchall() 
            #cursor.close()
            return message
    except Exception,ex:
        print Exception,":",ex
        print 'hadoopSpark get message fail:',sql
        return -1
