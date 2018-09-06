#-*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import zipfile 
from var import var
def mailsmtp():
    now_dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f = zipfile.ZipFile(var.path_mail, "w" ,zipfile.ZIP_DEFLATED) 
    f.write(var.path_rslt)
    f.write(var.path_lrcd)
    f.close() 
    sender = "1015052260@qq.com"
    if var.type_imei == 'imei' or var.type_imei == 'test':
        mailto = ['1152291236@qq.com','xiaoliujun@che08.com','1015052260@qq.com',]
    elif var.type_imei == 'baoxian':
        mailto = ['xiaoliujun@che08.com','1015052260@qq.com']
        #mailto = ['sunyalei@che08.com','xiaoliujun@che08.com','1015052260@qq.com','wangyanbing@che08.com','xietianwei@che08.com']
    elif var.type_imei == 'mlxy':
        mailto = ['xiaoliujun@che08.com','1015052260@qq.com']
        #mailto = ['xiaoliujun@che08.com','wuge@che08.com','liyijun@che08.com','ouguoshi@che08.com','situjinquan@che08.com','lijiaming@che08.com','xietianwei@che08.com','wangchenglong@che08.com','huxiaoshuang@che08.com','sunyalei@che08.com','xiangsen@che08.com','wanghailong@che08.com']
    elif var.type_imei == 'lecheng':
        mailto = ['xiaoliujun@che08.com','1015052260@qq.com']
    elif var.type_imei == 'abnormal':
        mailto = ['xiaoliujun@che08.com','1015052260@qq.com']
    elif var.type_imei == 'other':
        mailto = ['xiaoliujun@che08.com','1015052260@qq.com']
    else:
        mailto = ['xiaoliujun@che08.com','1015052260@qq.com']
    mailto1 = ','.join(mailto)
    #print mailto
    imgfiles5 = var.path_mail
    msg = MIMEMultipart()
    if var.type_imei == "baoxian":
        msg["Subject"] = "OBD_YDCX_Data_Analyze_" + now_dt
    else:
        msg["Subject"] = "OBD_" + var.type_imei + "_Data_Analyze_" + now_dt
    msg["To"] = mailto1
    msg["From"] = sender

    #邮件内容
    if var.type_imei == 'baoxian':
        Contents = MIMEText(
        "<b>Auto-Completion!</b>" + "<br />" + \
        "<b>Login_Count: </b>" + str(var.ct_lgin) + "<br />" + \
        "<b>Nologin_Count: </b>" + str(var.ct_nlgin) + "<br />" + \
        "<b>Get_Data_Error: </b>" + str(var.ct_svrr) + "<br />" + \
        "<b>Devices Lost: </b>" + str(var.ct_lost) + "<br />" + str(var.dc_lost) + "<br />" + \
        "<b>Devices Resume: </b>" + str(var.ct_resm) + "<br />" + str(var.dc_resm) + "<br />" ,\
        "html")
    else:
        Contents = MIMEText(
        "<b>Auto-Completion!</b>" + "<br />" + \
        "<b>Login_Count: </b>" + str(var.ct_lgin) + "<br />" + \
        "<b>Nologin_Count: </b>" + str(var.ct_nlgin) + "<br />" + \
        "<b>Get_Data_Error: </b>" + str(var.ct_svrr) + "<br />" + \
        "<b>Devices Lost: </b>" + str(var.ct_lost) + "<br />" + str(var.dc_lost) + "<br />" + \
        "<b>Devices Resume: </b>" + str(var.ct_resm) + "<br />" + str(var.dc_resm) + "<br />" + \
        "<b>Devices Debug: </b>" + "<br />" + str(var.dc_debg) + "<br />",\
        "html")
        
    msg.attach(Contents)

    att5 =  MIMEApplication(file(imgfiles5, "rb").read())  
    att5["Content-Type"] = "application/octet-stream"  
    att5.add_header("content-disposition","attachment",filename = var.type_imei + "_obd_" +var.dt + ".zip")
    msg.attach(att5)
    

    # 登录邮件发送服务器
    smtp = smtplib.SMTP("smtp.qq.com")
    smtp.login("1015052260","zemixoduxirobdeb")

    # 发送邮件
    for recv in mailto:
        smtp.sendmail(sender, recv, msg.as_string())
    smtp.quit()
    print "success!"
