#-*- coding:utf-8 -*-
from dtbs.hadoop import pySpark
sql_hd1,sql_hd2,sql_hd3 = "select category,content,process_time from obd_raw_data where stat_date= '","' and imei = '" ,"'  order by process_time"
def main():
    try:
        
        conn = pySpark.impylaConnect("10.26.8.132",21051)
        sql_hd = sql_hd1 + '20161122' + sql_hd2 + '869267011388449' + sql_hd3
        rows_hd = pySpark.impylaGetMessage(conn,sql_hd)
        if rows_hd != -1 or rows_hd != []:
            f = open(r'/home/xiaoliujun/dmn_script/txt/869267011388449.txt','w')
            for rows in rows_hd:
                f.write(str(rows)+'\r\n')
            f.close()

    finally:
        print 'pyspark close.'
        pySpark.impylaClose(conn)
        

if __name__ == '__main__':
    main()
