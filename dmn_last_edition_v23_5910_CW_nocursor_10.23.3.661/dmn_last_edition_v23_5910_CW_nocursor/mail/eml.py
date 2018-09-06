#-*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import zipfile 
from variable import var
def mailsmtp():
    now_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f = zipfile.ZipFile(var.mail_path, 'w' ,zipfile.ZIP_DEFLATED) 
    #f.write(var.everyday_login_path) 
    #f.write(var.excel_file_name[:-9] + '-bug.xls') 
    f.write(var.excel_file_name) 
    f.close() 
    sender = '1015052260@qq.com'
    if var.model_sign == 2 or var.model_sign == 3:
        mailto = ['xiaoliujun@che08.com','1015052260@qq.com']
    else:
        mailto = ['xiaoliujun@che08.com','1015052260@qq.com']
        #mailto = ['xiaoliujun@che08.com','1015052260@qq.com','wanghailong@che08.com','yanshaowei@che08.com','wangmingxing@che08.com','huochengjun@che08.com']
        #mailto = ['xiaoliujun@che08.com','1015052260@qq.com','huxiaoshuang@che08.com','situjinquan@che08.com','xietianwei@che08.com','wanghailong@che08.com','wangmingxing@che08.com','huochengjun@che08.com','yanshaowei@che08.com']
    mailto1 = ','.join(mailto)
    imgfiles5 = var.mail_path
    msg = MIMEMultipart()
    if var.ctrl_sign == 'JG':
        msg['Subject'] = 'JG__OBD__Data_Analyze_' + now_dt + '_model_' + var.sql_getimei[-4:]
    else:
        msg['Subject'] = 'GR__OBD__Data_Analyze_' + now_dt + '_model_' + var.sql_getimei[-4:]
    msg['To'] = mailto1
    msg['From'] = sender

    # 邮件内容
    if var.ctrl_sign == 'JG':
        Contents = MIMEText('<b>Automatic processing!!!</b>'+ \
        '<b> ; Count_Login: </b>' + str(var.login_imei) +   \
        '<b> ; Count_Nolgn: </b>' + str(var.nologin_imei) + \
        '<b> ; ServerError: </b>' + str(var.server_error) + \
        '<b> ; aotu-reset-num: </b>' + str(var.ct_sms) + \
        '<b> ; auto-reset-imei: </b>' + str(var.imei_list),'html')
    else:
        Contents = MIMEText('<b>Automatic processing!</b>' + \
        '<b> ; Count_Login: </b>' + str(var.login_imei) +   \
        '<b> ; Count_Nolgn: </b>' + str(var.nologin_imei) + \
        '<b> ; ServerError: </b>' + str(var.server_error) + \
        '<b> ; aotu-reset-num: </b>' + str(var.ct_sms) + \
        '<b> ; auto-reset-imei: </b>' + str(var.imei_list),'html')
    
    msg.attach(Contents)

    att5 =  MIMEApplication(file(imgfiles5, 'rb').read())  
    att5["Content-Type"] = 'application/octet-stream'  
    if var.ctrl_sign == 'JG':
        att5.add_header('content-disposition','attachment',filename = 'JG__OBD__' +var.dt + '.zip')
    else:
        att5.add_header('content-disposition','attachment',filename = 'GR__OBD__' +var.dt + '.zip')
    msg.attach(att5)
    

    # 登录邮件发送服务器
    smtp = smtplib.SMTP('smtp.qq.com')
    smtp.login('1015052260','1234qw')

    # 发送邮件
    smtp.sendmail(sender, mailto, msg.as_string())
    smtp.quit()
    print 'success!'
