#-*- coding:utf-8 -*-
import pymongo
import sys

# mongo 连接

def mongoConnect(mongo_ip,mongo_port):
    try:
        conn = pymongo.Connection(mongo_ip,mongo_port,slave_okay=True) #SLAVE db use
        #conn = pymongo.Connection(mongo_ip,mongo_port)
        mg = conn.obd
        print "mongo connect success."
        return conn,mg
    except Exception,ex:
        print Exception,":",ex
        print "mongo connect fail, Game Over."
        return -1,-1

# mongo 关闭

def mongoClose(conn):
    try:
        conn.disconnect()
        print "mongo is closed."
    except Exception,ex:
        print Exception,":",ex
        print "mongo close fail."


# mongo 获取 message

def mongoGetMessage(mg,sql):
    try:
        message = mg.obd_raw_data.find(sql)
        return message
    except Exception,ex:
        print Exception,":",ex
        print "mongo get message fail:",sql
        return -1
    
    
"""
# mongo 获取登录登出记录

def mongoGetLogInOut(mg,tid):
    try:
        message = mg.obd_raw_data.find({"imei":imei,"process_time":{"$regex":dt}})
        loginout = mg.login_record.find({"tid":int(tid)}).sort([("Time", pymongo.DESCENDING)])
        return loginout
    except Exception,ex:
        print Exception,"::",ex
        print "mongo get loginout fail : ",imei
        return -1
"""
