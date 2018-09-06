#-*- coding:utf-8 -*-
import zipfile 

def main(imei):
    #now_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f = zipfile.ZipFile('/home/xiaoliujun/obd/1.zip', 'w' ,zipfile.ZIP_DEFLATED) 
    f.write('/home/xiaoliujun/obd/20150517-100953-obd-data.xls') 
    #f.write(var.excel_file_name[:-9] + '-bug.xls') 
    #f.write(var.excel_file_name) 
    f.close()
    
    

if __name__ == '__main__':
    imei = "869269016686512"
    main(imei)
