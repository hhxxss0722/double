#-*- coding:utf-8 -*-
import MySQLdb
import sys

# mysql 连接
def mysqlConnect(sql_ip,sql_name,sql_pw,sql_base,sql_char):
    try:
        conn = MySQLdb.connect(sql_ip,sql_name,sql_pw,sql_base,charset = sql_char)
        cursor = conn.cursor()
        print "mysql connect success."
        return conn,cursor
    except Exception,ex:
        print Exception,":",ex
        print "mysql connect fail, Game Over."
        return -1,-1

# mysql 关闭

def mysqlClose(conn,cursor):
    try:
        cursor.close()
        conn.close()
        print "mysql is closed."
    except Exception,ex:
        print Exception,":",ex
        print "mysql close fail."


# mysql 获取设备数据

def mysqlGetMessage(cursor,sql):
    try:
        cursor.execute(sql)
        message = cursor.fetchall() 
        return message
    except Exception,ex:
        print Exception,":",ex
        print "mysql get message fail:",sql
        return -1
