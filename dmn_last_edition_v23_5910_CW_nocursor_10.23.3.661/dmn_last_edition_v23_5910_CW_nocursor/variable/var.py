#-*- coding:utf-8 -*-
import sys
import datetime

# 控制软件运行平台环境
# 车网外网
ctrl_sign = 'GR'
# 车网demo
#ctrl_sign = 'DM'
# 建国集团
#ctrl_sign = 'JG'

# 非自动从数据库获取imei号时，需设置imei的txt路径
# production - 车网
file_imei_txt = '/home/xiaoliujun/dmn_last_edition_v23_5910_CW_nocursor/imei.txt'
# demo - 车网
#file_imei_txt = '/opt/dmn_final_v23_4B11/imei.txt'
# production - 建国
#file_imei_txt = 'D:\\xiao\\dmn\\dmn_last_edition_v21_5416_CW\\imei.txt'


if ctrl_sign == 'GR':
    obd_path = '/home/xiaoliujun/obd/'
    test_path = '/home/xiaoliujun/tst/'
    #1. mysql obd db ip and port
    # production
    sql_ip_obd,sql_name_obd,sql_pw_obd,sql_base_obd,sql_char_obd = "10.26.8.22","xiaoliujun","clt","","utf8"

    #2. mysql tcm db ip and port
    # production
    sql_ip_tcm,sql_name_tcm,sql_pw_tcm,sql_base_tcm,sql_char_tcm = "10.26.4.22","xiaoliujun","clt","tcm","utf8"

    #3. mongo db ip and port
    # production
    mongo_ip,mongo_port = '10.26.8.102',30000

    #4. hadoopSpark db ip and port
    # production
    hadoop_ip,hadoop_port,hadoop_name,hadoop_pw,hadoop_database,hadoop_authMechanism = '10.21.2.21',12229,'hadoop','clt','default','PLAIN'
    
    #5. get group_customer
    sql_ip_csr,sql_name_csr,sql_pw_csr,sql_base_csr,sql_char_csr = "10.21.1.135","huxiaoshuang","huxiaoshuang1234","","utf8"
    
elif ctrl_sign == 'DM':
    obd_path = '/root/xiao/obd/'
    test_path = '/root/xiao/tst/'
    #1. mysql obd db ip and port
    # demo
    sql_ip_obd,sql_name_obd,sql_pw_obd,sql_base_obd,sql_char_obd = "10.23.102.33","root","clt","","utf8"

    #2. mysql tcm db ip and port
    # demo
    sql_ip_tcm,sql_name_tcm,sql_pw_tcm,sql_base_tcm,sql_char_tcm = "10.23.102.33","root","clt","tcm","utf8"

    #3. mongo db ip and port
    # demo
    mongo_ip,mongo_port = '10.23.106.21',30000

    #4. hadoopSpark db ip and port
    # demo
    hadoop_ip,hadoop_port,hadoop_name,hadoop_pw,hadoop_database,hadoop_authMechanism = '10.23.101.230',10000,'hadoop','clt','default','PLAIN'
    
elif ctrl_sign == 'JG':
    
    obd_path = 'D:\\xiao\\obd\\'
    test_path = 'D:\\xiao\\tst\\'
    #1. mysql obd db ip and port
    # production
    sql_ip_obd,sql_name_obd,sql_pw_obd,sql_base_obd,sql_char_obd = "172.16.200.32 ","xiaoliujun","xiaoliujun4321","","utf8"
    '''
    #2. mysql tcm db ip and port
    # production
    sql_ip_tcm,sql_name_tcm,sql_pw_tcm,sql_base_tcm,sql_char_tcm = "10.21.1.33","xiaoliujun","xlj7799","tcm","utf8"
    '''
    #3. mongo db ip and port
    # production
    mongo_ip,mongo_port = '172.16.200.21',30000
    '''
    #4. hadoopSpark db ip and port
    # production
    hadoop_ip,hadoop_port,hadoop_name,hadoop_pw,hadoop_database,hadoop_authMechanism = '10.21.2.21',12229,'hadoop','clt','default','PLAIN'
    '''

else:
    print 'ctrl_sign is error.'

'''
sql语句整理
'''

#1. 获取所有激活的imei
#C2 V1.2 8692670126
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE  a.imei LIKE '8692670126%' AND supplier_name IN('iOBD-C1','iOBD-C2') AND (software_version LIKE 'C1%' OR software_version LIKE 'C2%')"
#C2 V1.5
sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE a.imei LIKE '866717021%' AND a.software_version LIKE 'C20224%'"
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE a.hardware_version = '0002030038' AND a.software_version LIKE 'C20224%'"
#C2 V1.5 AND C2 V1.2 86926701262
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE (a.imei LIKE '86926701262%' OR a.imei LIKE '8667%') AND supplier_name IN('iOBD-C1','iOBD-C2') AND (software_version LIKE 'C1%' OR software_version LIKE 'C2%')"
#C2 V1.5 8667170220 AND C2 V1.2 86926701262
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE (a.imei LIKE '86926701262%' OR a.imei LIKE '8667170222%') AND supplier_name IN('iOBD-C1','iOBD-C2') AND (software_version LIKE 'C1%' OR software_version LIKE 'C2%')"

#根据车型来找对应的imei号，扫描数据
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE a.imei LIKE '86%' AND a.software_version LIKE 'C20224%' AND e.model_name LIKE '奥迪%'"
#根据CM3版本来找对应的imei号，扫描数据
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE a.imei LIKE '86%' AND a.software_version LIKE 'C20224%' AND a.hardware_version = '0020019994'"
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE a.imei LIKE '86%' AND a.software_version LIKE 'C20%' AND e.brand_id = 159"







#域名解析
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE  (a.imsi LIKE '134179%' OR a.imsi LIKE '138256%') AND a.software_version LIKE 'C%' AND a.imei LIKE '8692%'"
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE a.software_version LIKE 'C%' AND c.license_plate LIKE '京%' AND a.imei LIKE '8692%'"

#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE  a.imei LIKE '86926%' AND supplier_name IN('iOBD-C1','iOBD-C2') AND (software_version LIKE 'C1%' OR software_version LIKE 'C2%')"
#sql_getimei = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id WHERE  a.imei LIKE '86926901%' AND supplier_name IN('iOBD-C1','iOBD-C2') AND (software_version LIKE 'C1%' OR software_version LIKE 'C2%')"
#C1
#sql_getimei = "SELECT terminal_id,imei,imsi,hardware_version,software_version,group_name,supplier_name,network_name,bind_time,security_domain FROM obd.terminal WHERE imei LIKE '86926%' AND supplier_name IN('iOBD-C1','iOBD-C2') AND (software_version LIKE 'C1%')"
#C2
#sql_getimei = "SELECT terminal_id,imei,imsi,hardware_version,software_version,group_name,supplier_name,network_name,bind_time,security_domain FROM obd.terminal WHERE imei LIKE '86926%' AND supplier_name IN('iOBD-C1','iOBD-C2') AND (software_version LIKE 'C2%')"
#TEST
#sql_getimei = "SELECT terminal_id,imei,imsi,hardware_version,software_version,group_name,supplier_name,network_name,bind_time,security_domain FROM obd.terminal WHERE imei LIKE '86926701223%' AND supplier_name IN('iOBD-C1','iOBD-C2') AND (software_version LIKE 'C2%')"

#2. 从hadoop中获取原始报文
# production
sql_hd1,sql_hd2,sql_hd3 = "select category,content,process_time from obd_raw_data where stat_date= '","' and imei = '" ,"'  order by process_time"

#3. 获取单个imei的信息
#sql_obdversion = "SELECT terminal_id,imei,imsi,hardware_version,software_version,group_name,supplier_name,network_name,bind_time,security_domain FROM obd.terminal WHERE imei = "
sql_obdversion = "SELECT a.terminal_id,a.imei,a.imsi,a.hardware_version,a.software_version,a.group_name,a.supplier_name,a.network_name,a.bind_time,a.security_domain,c.license_plate,c.vin,d.style_name,e.model_name,f.latest_interact_time,h.mobile,j.latest_login,j.first_login FROM obd.terminal a LEFT JOIN obd.terminal_vehicles b ON a.terminal_id = b.terminal_id LEFT JOIN auto.vehicle c ON b.vehicle_id = c.vehicle_id LEFT JOIN auto.style d ON c.style_id = d.style_id LEFT JOIN auto.model e ON d.model_id = e.model_id LEFT JOIN troubleshooting.client_profile f ON a.imei = f.imei LEFT JOIN obd.customer_terminals g ON a.terminal_id = g.terminal_id LEFT JOIN obd.uc_customer h ON g.customer_id = h.customer_id LEFT JOIN obd.terminal_statuz j ON a.terminal_id = j.terminal_id WHERE a.imei = "

#4. 获取用户车辆信息
sql_carinfo1 = "select a.license_plate,a.vin,a.style_id from auto.vehicle a,obd.terminal_vehicles b where b.terminal_id ="
sql_carinfo2 = " and b.vehicle_id = a.vehicle_id"
sql_carinfo3 = "select model_id,style_name from auto.style where style_id="
sql_carinfo4 = "select model_name from auto.model where model_id="

#5. 获取升级记录信息
sql_upgrade1 = "SELECT created FROM upgrade_history WHERE imei= "
sql_upgrade2 = " ORDER BY CREATEd DESC"

#6. 获取设备所属客户信息
sql_customer1 = "SELECT terminal_id FROM serviceopen.terminal WHERE imei = "
sql_customer2 = "SELECT group_customer_id FROM serviceopen.terminal_group WHERE terminal_id = "

#7. 用户最近登录app的时间
sql_applogin = "SELECT latest_interact_time FROM troubleshooting.client_profile WHERE imei = "

#8. 用户手机号码
sql_phone1 = "SELECT customer_id FROM obd.customer_terminals WHERE terminal_id = "
sql_phone2 = "SELECT mobile FROM obd.uc_customer WHERE customer_id = "

#9. 设备生产批次
sql_batch1 = "SELECT product_batch FROM detect_record WHERE imei = "
sql_batch2 = " ORDER BY CREATEd DESC"




import os
import xlwt

xls_order,xls_supplier,xls_network,xls_imei = 0,1,2,3

xls_dict = {
xls_order:'№',xls_supplier:u'设备类型',xls_network:u'客户',xls_imei:'imei'
}
#obd_path = '/home/xiaoliujun/obd/'
#test_path = '/home/xiaoliujun/tst/'

for cpath in [obd_path,test_path]:
    if os.path.exists(cpath):
        #print 'exist'
        pass
    else:
        os.makedirs(cpath)
        #print 'filemake success'

    if os.path.exists(cpath + cpath[-4:-1] + '_login_table.xls'):
        #print 'exist'
        pass
    else:
        wbk = xlwt.Workbook(encoding = 'utf-8')
        sheet1 = wbk.add_sheet('login',cell_overwrite_ok=True)
        for key in xls_dict.keys():
            sheet1.write(0,key,xls_dict[key])

        wbk.save(cpath + cpath[-4:-1] + '_login_table.xls')
        print 'xlsmake success'

# argv 判断
lens = len(sys.argv)
if lens == 1:
    ismail = 'ym'
    if ctrl_sign == 'JG':
        model_sign = 1
    else:
        model_sign = 0
    dt = ''.join(str(datetime.date.today()- datetime.timedelta(1)).split('-'))
    save_excel_path_1,save_excel_path_2 = obd_path,'-obd-data.xls'
    everyday_login_path = obd_path + 'obd_login_table.xls'
    mail_path = obd_path + 'obd.zip'
elif lens == 4:
    ismail = sys.argv[2]
    dt = ''.join(str(datetime.date.today()- datetime.timedelta(int(sys.argv[3]))).split('-'))
    if sys.argv[1] == '0':
        model_sign = 0
        save_excel_path_1,save_excel_path_2 = obd_path,'-obd-data.xls'
        everyday_login_path = obd_path + 'obd_login_table.xls'
        mail_path = obd_path + 'obd.zip'
    elif sys.argv[1] == '1':
        model_sign = 1
        save_excel_path_1,save_excel_path_2 = obd_path,'-obd-data.xls'
        everyday_login_path = obd_path + 'obd_login_table.xls'
        mail_path = obd_path + 'obd.zip'
        
    elif sys.argv[1] == '2':
        model_sign = 2
        save_excel_path_1,save_excel_path_2 = test_path,'-test-data.xls'
        everyday_login_path = test_path + 'tst_login_table.xls'
        mail_path = test_path + 'test.zip'
    elif sys.argv[1] == '3':
        model_sign = 3
        save_excel_path_1,save_excel_path_2 = test_path,'-test-data.xls'
        everyday_login_path = test_path + 'tst_login_table_3.xls'
        mail_path = test_path + 'test.zip'
    
    else:
        model_sign = 4
        save_excel_path_1,save_excel_path_2 = test_path,'-test-data.xls'
        everyday_login_path = test_path + 'tst_login_table.xls'
        mail_path = test_path + 'test.zip'
        
else:
    print 'input error, form: python d:\\xiao\\dmn\main.py 0(1) ym(nm) 1'

excel_file_name = save_excel_path_1 + dt + '-' + datetime.datetime.now().strftime('%H%M%S') + save_excel_path_2

'''
参数设置，imei变化时不需要重置
len_imei  : imei号的数量
num_imei  ：当前查询到多少个
server_error ： 获取原始报文异常的数量
login_imei   ： 发送了上行数据包的数量
nologin_imei ： 未发送上行数据包的数量
'''
# imei相关的数据统计
len_imei,num_imei,server_error,login_imei,nologin_imei,ct_sms = 0,0,0,0,0,0

# 低电压的值
value_volt_low = 11.3

# 数据包格式错误写入最大的列数量
value_sht2_err = 50

# 低压报警的阈值,里程异常的最大值，油量异常的最小值、最大值，转速异常的最小值、最大值，车速异常的最小值、最大值
value_volt_low,value_mileage_max,value_oil_min,value_oil_max,value_enginespeed_min,value_enginespeed_max,value_speed_min,value_speed_max = 11.3,500000,0,123,0,4000,0,160

# 线程控制
if ctrl_sign == 'JG':
    if model_sign == 2:
        count_threading = 1
    else:
        count_threading = 1
else:
    if model_sign == 2 or model_sign == 3:
        count_threading = 1
    else:
        count_threading = 5

# 4001、4002 电压应用的值，dt_volt
value_volt_4001,value_volt_4002 = 4001,4002

# 判断数据是否延迟的参数,cell_id的lacc初始值
value_delay_min,value_delay_max,speed_gps_4002 = 1,90,10.0

# 记录自动下发短信的imei号
imei_list = []


'''
xls表格的列控制和列头数据
'''
# xls列头参数1
col_imei,col_type,col_batch,col_applogin,col_date,col_runtime,col_action,col_discon,col_login,\
col_mileage,col_oil,col_enginespeed,col_speed,col_carvin,col_tid,\
col_imsi,col_hardware,col_software,col_group,col_network,col_domain,\
col_model,col_style,col_vin_value,col_vin,col_licence_plate,\
col_phone = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26

dict1 = {
col_imei:'imei',col_type:'设备类型',col_batch:'生产批次',col_applogin:'APP登录-用户最近',col_date:'最近登录时间',col_runtime:'首次登录时间',\
col_action:'行为分析',col_discon:'掉电时间',col_login:'登录情况',\
col_mileage:'里程',col_oil:'油量',col_enginespeed:'转速',col_speed:'车速',col_carvin:'vin',col_tid:'tid',col_imsi:'imsi',col_hardware:'CM3版本',\
col_software:'主控版本',col_group:'集团',col_network:'网点',col_domain:'安全域',col_model:'车型',col_style:'型号',\
col_vin_value:'vin_车辆',col_vin:'vin_平台',col_licence_plate:'车牌号',col_phone:'用户手机号'
}

# xls列头参数1.1，平台配置解析
col_fbox,col_alarmvolt,col_shakevalue,col_accgps,col_collision = 27,28,29,30,31


dict1_1 = {
col_fbox:'下发油箱',col_alarmvolt:'低电阈值',col_shakevalue:'震动阈值',col_accgps:'加速阈值',col_collision:'碰撞阈值'
}


# xls列头参数2
col_count_1004,col_count_2001,col_count_2011,col_count_2021,col_count_2031,col_count_3021,col_count_3031,col_count_3032,\
col_count_4001,\
col_count_4002,col_count_4011,col_count_5001,col_count_5005,col_count_5006,col_count_6001,col_count_9000,col_count_9100,\
col_count_9990,col_count_9999 = 32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50

dict2 = {
col_count_1004:'1004数量',col_count_2001:'2001数量',col_count_2011:'2011数量',col_count_2021:'2021数量',col_count_2031:'2031数量',\
col_count_3021:'3021数量',col_count_3031:'3031数量',col_count_3032:'3032数量',\
col_count_4001:'4001数量',col_count_4002:'4002数量',col_count_4011:'4011数量',\
col_count_5001:'5001数量',col_count_5005:'5005数量',col_count_5006:'5006数量',col_count_6001:'6001数量',col_count_9000:'9000数量',\
col_count_9100:'9100数量',col_count_9990:'9990数量',col_count_9999:'9999数量'
}

# xls列头参数3
col_count_vlow,col_count_lgin,col_count_in,col_count_out,col_duplicate,\
col_count_updelay,col_count_miss4001,col_count_error4002,col_bnds,\
col_count_reset,col_rate2001,col_distance = 51,52,53,54,55,56,57,58,59,60,61,62
'''
col_count_vlow : ct_vlow
col_count_lgin : count_fbox
col_duplicate  : count_duplicate
col_bnds       : ct_bnds
col_count_miss4001  : sign_2011 + sign_2021，miss_4001
col_count_error4002 : sign_4002
col_count_updelay   : sign_delay
col_count_reset     : sign_rst
'''

dict3 = {
col_count_vlow:'低电数量',col_count_lgin:'配置数量',col_count_in:'登录数量',col_count_out:'登出数量',\
col_duplicate:'重复数量',col_bnds:'号码绑定数量',\
col_count_miss4001:'漏报点火数量',col_count_error4002:'误报熄火数量',col_count_updelay:'延迟上报数量',\
col_count_reset:'重启数量',col_rate2001:'2001上报间隔',col_distance:'两点距离大于3km的数量'
}

# xls列头参数4
col_er_rate2001,\
col_form1004,col_form2001,col_form2011,col_form2021,col_form2031,col_form3021,col_form3031,col_form3032,\
col_form4001,col_form4002,\
col_form4011,col_form5001,col_form5005,col_form5006,col_form6001,col_form9000,col_form9100,col_form9990,col_form9999,\
col_formtime,col_timeerror = 63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84

dict4 = {
col_er_rate2001:'2001间隔错误数量',\
col_form1004:'1004错误',col_form2001:'2001错误',col_form2011:'2011错误',col_form2021:'2021错误',col_form2031:'2031错误',\
col_form3021:'3021错误',col_form3031:'3031错误',col_form3032:'3032错误',\
col_form4001:'4001错误',col_form4002:'4002错误',col_form4011:'4011错误',\
col_form5001:'5001错误',col_form5005:'5005错误',col_form5006:'5006错误',col_form6001:'6001错误',col_form9000:'9000错误',\
col_form9100:'9100错误',col_form9990:'9990错误',col_form9999:'9999错误',col_formtime:'时间格式错误',col_timeerror:'写包时间错误'
}

# xls列头参数5
col_debug_0,col_debug_1,col_debug_2,col_debug_3,col_debug_4,col_debug_5,col_debug_6,col_debug_7,col_debug_9011,col_debug_9021,\
col_debug_9031,col_debug_9041,col_debug_9051,col_debug_9052,col_debug_9053,col_debug_9054,col_debug_9061,col_debug_9062,\
col_debug_9063,col_debug_9064,col_debug_9065,col_debug_9066,col_debug_9067,col_debug_9068,col_debug_9069,col_debug_9071,\
col_debug_9072,col_debug_9073,col_debug_9074,col_debug_9075,col_debug_9076,col_debug_9081,col_debug_9082,col_debug_9100,\
col_debug_9101,col_debug_9102,col_debug_9103,col_debug_9109,col_debug_9301,col_debug_9302,col_debug_9303,col_debug_9304,\
col_debug_9305,col_debug_9306,col_debug_9307,col_debug_9308,col_debug_9309,col_debug_9310,col_debug_9331,col_debug_9332,\
col_debug_9401,col_debug_9991,col_debug_9992,col_debug_9993,col_debug_9994,col_debug_9995,col_volt_time = 85,86,87,88,89,90,91,92,\
93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,\
124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141

dict5 = {
col_debug_0:'0_数量',col_debug_1:'1_数量',col_debug_2:'2_数量',col_debug_3:'3_数量',col_debug_4:'4_数量',col_debug_5:'5_数量',\
col_debug_6:'6_数量',col_debug_7:'7_数量',col_debug_9011:'9011_数量',col_debug_9021:'9021_数量',col_debug_9031:'9031_数量',\
col_debug_9041:'9041_数量',col_debug_9051:'9051_数量',col_debug_9052:'9052_数量',col_debug_9053:'9053_数量',\
col_debug_9054:'9054_数量',col_debug_9061:'9061_数量',col_debug_9062:'9062_数量',col_debug_9063:'9063_数量',\
col_debug_9064:'9064_数量',col_debug_9065:'9065_数量',col_debug_9066:'9066_数量',col_debug_9067:'9067_数量',\
col_debug_9068:'9068_数量',col_debug_9069:'9069_数量',col_debug_9071:'9071_数量',col_debug_9072:'9072_数量',\
col_debug_9073:'9073_数量',col_debug_9074:'9074_数量',col_debug_9075:'9075_数量',col_debug_9076:'9076_数量',\
col_debug_9081:'9081_数量',col_debug_9082:'9082_数量',\
col_debug_9100:'9100_数量',col_debug_9101:'9101_数量',col_debug_9102:'9102_数量',col_debug_9103:'9103_数量',\
col_debug_9109:'9109_数量',\
col_debug_9301:'9301_数量',col_debug_9302:'9302_数量',col_debug_9303:'9303_数量',col_debug_9304:'9304_数量',\
col_debug_9305:'9305_数量',col_debug_9306:'9306_数量',col_debug_9307:'9307_数量',col_debug_9308:'9308_数量',\
col_debug_9309:'9309_数量',col_debug_9310:'9310_数量',col_debug_9331:'9331_数量',col_debug_9332:'9332_数量',\
col_debug_9401:'9401_数量',col_debug_9991:'9991_数量',\
col_debug_9992:'9992_数量',col_debug_9993:'9993_数量',\
col_debug_9994:'9994_数量',col_debug_9995:'9995_数量',col_volt_time:'电压数据'
}


# 6001,9100 xls列头
col_dgtg,col_tacc = 142,143
dict6 = {
col_dgtg:'诊断数据',col_tacc:'百公里加速'
}



'''
参数设置，imei变化时需要重置
'''
'''
对应dict2的参数
'''
#上行数据包的统计
ct_1004,ct_2001,ct_2011,ct_2021,ct_2031,ct_3021,ct_3031,ct_3032,\
ct_4001,ct_4002,ct_4011,ct_5001,ct_5005,ct_5006,\
ct_6001,ct_9000,ct_9100,ct_9990,ct_9999 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

'''
对应dict3的参数
'''
ct_vlow,count_fbox,count_in,count_out,count_duplicate,ct_bnds,sign_2011,sign_2021,\
miss_4001,sign_4002,sign_delay,sign_rst = 0,0,0,0,0,0,0,0,0,0,0,0

'''
对应dict4的参数
'''
# 数据包格式错误的统计
er_rate2001,er_1004,er_2001,er_2011,er_2021,er_2031,er_3021,er_3031,er_3032,\
er_4001,er_4002,er_4011,er_5001,er_5005,er_5006,\
er_6001,er_9000,er_9100,er_9990,er_9999,formtime,timeerror = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

'''
对应dict5的参数
'''
#debug包的统计
ct_0,ct_1,ct_2,ct_3,ct_4,ct_5,ct_6,ct_7,ct_9011,ct_9021,ct_9031,ct_9041,ct_9051,\
ct_9052,ct_9053,ct_9054,ct_9061,ct_9062,ct_9063,ct_9064,ct_9065,ct_9066,ct_9067,\
ct_9067,ct_9068,ct_9069,ct_9071,ct_9072,ct_9073,ct_9074,ct_9075,ct_9076,ct_9081,ct_9082,ctg_9100,\
ct_9101,ct_9102,ct_9103,ct_9109,ct_9301,ct_9302,ct_9303,ct_9304,ct_9305,ct_9306,ct_9307,ct_9308,\
ct_9309,ct_9310,ct_9331,ct_9332,ct_9401,\
ct_9991,ct_9992,ct_9993,ct_9994,ct_9995 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

'''
2001包解析的参数
'''
#用于里程分析的参数
mileage_no,mileage_yes,mileage_ab,mileage_init = 0,0,0,0
#用于油量分析的参数
oil_no,oil_yes,oil_ab = 0,0,0
#用于转速分析的参数
enginespeed_yes,enginespeed_ab,enginespeed_no = 0,0,0
#用于车速分析的参数
speed_no,speed_yes,speed_ab = 0,0,0

'''
temp_time,temp_type : 是否相同的临时参数
temp_4001,temp_4002 ：4001，4002是否重复的临时参数
lac_value ：2021包中lac是否变化的临时参数
'''
temp_time,temp_type,temp_4001,temp_4002,lac_value= '','','','',0

#数据包格式错误的列控制参数
sht2_colx = 1

#所有数据包内电压的统计,掉电时间集合.
dt_volt,dt_discon = {},[]

#vin的参数
ct_vin,vin_value = 0,''

#2001包时间间隔
temp_2001,rate1_2001,rate2_2001,rate3_2001,rate4_2001,rate_sign = '',0,0,0,0,0

# gps.py 计算GPS距离的参数
f1,f2,ct_distance = 0,0,0

# 6001包的解析参数
data_6001,dgak_list,dgtg_list,dgtg_ys,dgtg_no,dgtg_ab,dgtg_ac,dgtg_ae,dgtg_af,dgtg_ag = '',[],[],0,0,0,0,0,0,0

# 9100包的解析参数
data_9100,tacc_ys,tacc_no,tacc_ab,tacc_ac,tacc_ad,tacc_ae = '',0,0,0,0,0,0

# 记录自动下发短信的imei号
imei_list = []


'''
正则表达式
'''
re_type = '<type>(\d{4})</type><time>'
re_time = '</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time>'
# 配置信息的正则
re_conf = '^<iobd><conf><fbox>(\d{1,3})</fbox><acq><p>\d{1,3}</p><c>\d{1,3}</c><d>\d{1,3}</d></acq><alarm><b>(\d{1,3}.\d{1,2})</b><s>(\d{1,5})</s><acc-gps>(.{19,21})</acc-gps><acc-gsensor>(.{19,21})</acc-gsensor><collision>(\d{1,2}.\d{1,2})</collision></alarm><engine><emission>(-1|\d{3,5})</emission><form>(-1|(\d))</form></engine><smc><cm>\d{3,23}</cm><cu>\d{3,23}</cu><ct>\d{3,23}</ct></smc></conf></iobd>$'
'''
re_fbox = '<conf><fbox>(\d{1,3})</fbox>'
re_col_alarmvolt = '<alarm><b>(\d{1,3}.\d{1,2})</b><s>'
re_col_shakevalue = '<s>(\d{2,5})</s><acc-gps>'
re_col_accgps = '<acc-gps>(.{12,18})</acc-gps><acc-gsensor>'
re_col_collision = '<collision>(\d{1,2}.\d{1,2})</collision></alarm>'
'''
# 数据包的正则
re_1004 = '^<iobd><type>(1002|1004)</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><voltage>(\d{1,2}.\d{6})</voltage><connect>1</connect></iobd>$'
re_2001 = '^<iobd><type>2001</type><time>(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)</time><condition><m>(-1|\d{1,10})</m>(|<am>\d{1,5}.\d{1,6}</am>)(|<af>(-1.0|\d{1,5}.\d{1,6})</af>)<f>(-1|.\d{0,2}(,.\d{0,2})*)</f><v>(\d{1,2}.\d{1,6})</v><r>(-1|\d{1,8})</r><i1>(\d{1,3}|-1.0)</i1><i2>-1.0</i2><s>(-1|.\d{0,2}(,.\d{0,2})*)</s>(|<l>(-1|\d{1,2})</l>)</condition></iobd>$'
re_2011 = '<gps><p><a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o>(|<l>.\d{0,3}.\d{6}</l>)<s>(\d{1,3}.\d{6})</s>'
#re_2011 = '^<iobd><type>2011</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<p><a>(-1.0|\d{2}.\d{6})</a><o>(-1.0|\d{2,3}.\d{6})</o><s>(-1.0|\d{1,3}.\d{6})</s>(<t>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</t>){0,1}</p>){1,3}</gps></iobd>$'
re_2021 = '^<iobd><type>2021</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><cellid><mcc>\d{1,5}</mcc><mnc>\d{1,5}</mnc><lac>(\d{1,7})</lac><count>\d{1,2}</count><cells>(\d{1,6},\d{1,3})+(;(\d{1,6},\d{1,3})+)*</cells></cellid></iobd>$'
re_2031 = '^<iobd><type>2031</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><acceleration>(<acc><c>\d</c><v>G,.\d{0,2}.\d{1,6}</v><t>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</t><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps></acc>){1,5}</acceleration></iobd>'
re_3021 = '^<iobd><type>3021</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><sms><from>(10010|10086)</from><msg>\w{1,300}</msg></sms></iobd>$'
re_3031 = '^<iobd><type>3031</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><vin>(null|\w{17})</vin></iobd>$'
#re_3032 = '^<iobd><type>3032</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><pull_out_time>(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)</pull_out_time><gps><a>(-1.0|\d{2}.\d{6})</a><o>(-1.0|\d{2,3}.\d{6})</o><s>(-1.0|\d{1,3}.\d{6})</s></gps></iobd>$'
re_3032 = '^<iobd><type>3032</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><pull_out_time>(.{19,24})</pull_out_time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps></iobd>$'
re_4001 = '^<iobd><type>4001</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><vin>(null|\w{17})</vin></iobd>$'
re_4002 = '^<iobd><type>4002</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps>(|<warmup>\d{1,4}</warmup><idle>\d{1,4}</idle>)</iobd>$'
re_4011 = '^<iobd><type>4011</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><voltage>(\d{1,2}.\d{6})</voltage></iobd>$'
re_5001 = '^<iobd><type>5001</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><grade>\d{1,5}</grade></iobd>$'
re_5005 = '^<iobd><type>5005</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><grade>\d{1,5}</grade></iobd>$'
re_5006 = '^<iobd><type>5006</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><grade>\d{1,5}</grade></iobd>$'
re_6001 = '^<iobd><type>6001</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><diag><status>(\d{3})</status>(|<remain>\d{1,3}</remain>)<d><a>(-1|\d{1,3})</a><c>(.{1,300})</c></d></diag></iobd>$'
re_9000 = '^<iobd><type>9000</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><vin>(null|\w{17})</vin><dtu><signal_intensity>-\d{1,3}</signal_intensity><attach_time>\d{1,3}</attach_time></dtu><gps><fix>\d</fix><dop>(\d{1,2}.\d)(,\d{1,2}.\d)*</dop><satellite>\d{1,2},\d{1,2}</satellite></gps><gsensor><status>0</status><g_h_a>\d{1,3}</g_h_a></gsensor></iobd>$'
re_9100 = '^<iobd><type>9100</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><tacc><status>(\d{3})</status>(|<gps><a>\d{2}.\d{6}</a><o>\d{2,3}.\d{6}</o><s>\d{1,3}.\d{6}</s></gps>\<gps><a>\d{2}.\d{6}</a><o>\d{2,3}.\d{6}</o><s>\d{1,3}.\d{6}</s></gps><speed_list>(\d{1,3}.\d{1,2})(,\d{1,3}.\d{1,2})*</speed_list><speed_interval>\d{3,4}</speed_interval><time_consuming>\d{4,5}</time_consuming>)</tacc></iobd>$'
#re_9101 = '^<iobd><type>9100</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><tacc><status>\d{3}</status><gps><a>\d{2}.\d{6}</a><o>\d{2,3}.\d{6}</o><s>\d{1,3}.\d{6}</s></gps>\<gps><a>\d{2}.\d{6}</a><o>\d{2,3}.\d{6}</o><s>\d{1,3}.\d{6}</s></gps><speed_list>(\d{1,3}.\d{1,2})(,\d{1,3}.\d{1,2})*</speed_list><speed_interval>\d{3,4}</speed_interval><time_consuming>\d{4,5}</time_consuming></tacc></iobd>$'
re_9990 = '^<iobd><type>9990</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><exception>1000</exception></iobd>$'
re_9999 = '^<iobd><type>9999</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><debug><debug_infor>(\d{1,4})</debug_infor>(<debug_string>(|NULL|221.122.126.9|csq:\d{1,2}|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</debug_string>){0,1}</debug><voltage>(\d{1,2}.\d{6})</voltage></iobd>$'
re_9310 = '^<iobd><type>9999</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><debug><debug_infor>(\d{1,4})</debug_infor><debug_string>221.122.126.9</debug_string></debug><voltage>(\d{1,2}.\d{6})</voltage></iobd>$'




# bug.xls的列头
# 行控制
row_bg = 0

# bug.xls的列
bg_0,bg_1,bg_2,bg_3,bg_4,bg_5,bg_6,bg_7,bg_8,bg_9,bg_10,bg_11,bg_12 = 0,1,2,3,4,5,6,7,8,9,10,11,12

# 列头
dict_bg = {bg_0:'№',bg_1:u'设备类型',bg_2:'imei',bg_3:u'列号',bg_4:u'异常描述',bg_5:u'主控版本',\
bg_6:u'CM3版本',bg_7:u'集团',bg_8:u'网点',bg_9:'车型',bg_10:'型号',bg_11:u'日期',bg_12:u'备注'}

# xlshd的控制参数
#production
sign_test = 0
#demo
#sign_test = 1




# tcm xls
num_dx = 0
len_dx = 0
