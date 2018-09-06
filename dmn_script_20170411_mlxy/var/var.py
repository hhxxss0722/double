#-*- coding:utf-8 -*-
import sys
import datetime
import os
import xlwt
import platform

#全局变量
len_imei,num_imei,ct_svrr,ct_lgin,ct_nlgin = [0] * 5

#线程数量
count_threading = 2

#恢复/失联/异常debug
dc_resm,dc_lost,ct_resm,ct_lost,dc_debg = {},{},0,0,{}

#xls变量和常量
cl_sht2 = 1

cl_vale = 50

#temp变量
tmp_tm,tmp_tp,tmp_gps,tmp_41,tmp_42,tmp_lac = [""] * 6
tmp_dy0,tmp_dy1,tmp_dy2,tmp_dy3,tmp_dy4,tmp_dy5,tmp_dy6 = [0] * 7

#电压/掉电/delay数据
dc_volt,dc_dscn,dc_dlay = {},[],{}



#impyla查询
#sql_hd1,sql_hd2,sql_hd3 = "select category,content,process_time from obd_raw_data where stat_date= '","' and imei = '" ,"'  order by process_time"
sql_hd1,sql_hd2,sql_hd3 = "select category,content,process_time from obd_raw_data_parquet where stat_date= '","' and imei = '" ,"'  order by process_time"
sysstr = platform.system()
if(sysstr =="Windows"):
    path_obd = os.path.join(sys.path[0],"result")
    print path_obd
    path_tst = os.path.join(sys.path[0],"test")
    print path_tst
elif(sysstr == "Linux"):
    path_obd = os.path.join(sys.path[0],"result")
    path_tst = os.path.join(sys.path[0],"test")    
else:
    sys.exit()


#argv 判断
lens = len(sys.argv)
if lens == 1:
    type_imei = "imei"
    mail_recv = "self"
#    print sys.argv
    
    dt = "".join(str(datetime.date.today()- datetime.timedelta(1)).split("-"))
    path_mail = path_obd + "obd.zip"
elif lens == 4:
    type_imei = sys.argv[1]
    #mail_recv = sys.argv[2]
    mail_recv = "self"
 #   print sys.argv
    dt = "".join(str(datetime.date.today()- datetime.timedelta(int(sys.argv[3]))).split("-"))
    path_mail = path_obd + "obd.zip"
else:
    print "input error, form: python d:\\xiao\\dmn\main.py 0(1) ym(nm) 1"

#imei号和result的路径
path_imei = os.path.join(sys.path[0],"imei",type_imei + ".txt")
path_rslt = os.path.join(sys.path[0],"result",type_imei + "-" + dt + "-" + datetime.datetime.now().strftime("%H%M%S") + ".xls")
path_lrcd = os.path.join(sys.path[0],"result","lred_" + type_imei + ".xls")
print path_imei
print path_rslt
print path_lrcd


sn_xls,imei_xls = 0,1

dict_xls = {
sn_xls:'№',imei_xls:'imei'
}

if os.path.exists(path_obd) != True:
    os.makedirs(path_obd)

if os.path.exists(path_lrcd) != True:
    wbk = xlwt.Workbook(encoding = 'utf-8')
    sht = wbk.add_sheet('lred',cell_overwrite_ok=True)
    for key in dict_xls.keys():
        sht.write(0,key,dict_xls[key])
    wbk.save(path_lrcd)
    print 'xls make success.'


i = 0
#xls列头
cl_imei,cl_lgin,cl_dscn,cl_dlay,cl_mast,cl_cm33,cl_vinn = [i for i in xrange(i,i+7)]
dict1 = {
cl_imei:"imei",cl_lgin:"登录情况",cl_dscn:"掉电时间",cl_dlay:"延迟详情",cl_mast:"主控版本",cl_cm33:"CM3版本",cl_vinn:"VIN-点火"
}
st_imei,st_lgin,st_mast,st_cm33,st_vinn = [""] * 5


#xls列头
cl_ct_1004,cl_ct_2001,cl_ct_2011,cl_ct_2021,cl_ct_2031,cl_ct_3021,cl_ct_3022,cl_ct_3031,cl_ct_3032,cl_ct_4001,cl_ct_4002,cl_ct_4011,cl_ct_5001,cl_ct_5005,cl_ct_5006,\
cl_ct_6001,cl_ct_9000,cl_ct_9100,cl_ct_9990,cl_ct_9999,cl_ct_dely,cl_ct_rept,cl_ct_bnds,cl_ct_omsn,cl_ct_msjd,cl_ct_vlow,cl_ct_conn = [i for i in xrange(i+1,i+28)]
dict2 = {
cl_ct_1004:"1004数量",cl_ct_2001:"2001数量",cl_ct_2011:"2011数量",cl_ct_2021:"2021数量",cl_ct_2031:"2031数量",cl_ct_3021:"3021数量",cl_ct_3022:"3022数量",\
cl_ct_3031:"3031数量",\
cl_ct_3032:"3032数量",cl_ct_4001:"4001数量",cl_ct_4002:"4002数量",cl_ct_4011:"4011数量",cl_ct_5001:"5001数量",cl_ct_5005:"5005数量",cl_ct_5006:"5006数量",\
cl_ct_6001:"6001数量",cl_ct_9000:"9000数量",cl_ct_9100:"9100数量",cl_ct_9990:"9990数量",cl_ct_9999:"9999数量",cl_ct_dely:"数据延迟",cl_ct_rept:"数据重复",\
cl_ct_bnds:"BNDS数量",cl_ct_omsn:"漏判点火",cl_ct_msjd:"误判熄火",cl_ct_vlow:"低电数量",cl_ct_conn:"登录数量"
}
ct_1004,ct_2001,ct_2011,ct_2021,ct_2031,ct_3021,ct_3022,ct_3031,ct_3032,ct_4001,ct_4002,ct_4011,ct_5001,ct_5005,ct_5006,ct_6001,ct_9000,ct_9100,ct_9990,ct_9999,\
ct_dely,ct_rept,ct_bnds,ct_omsn,ct_msjd,ct_vlow,ct_conn = [0] * 27


#xls列头
cl_er_1004,cl_er_2001,cl_er_2011,cl_er_2021,cl_er_2031,cl_er_3021,cl_er_3022,cl_er_3031,cl_er_3032,cl_er_4001,cl_er_4002,cl_er_4011,cl_er_5001,cl_er_5005,cl_er_5006,\
cl_er_6001,cl_er_9000,cl_er_9100,cl_er_9990,cl_er_9999,cl_er_time = [i for i in xrange(i+1,i+22)]
dict3 = {
cl_er_1004:"1004错误",cl_er_2001:"2001错误",cl_er_2011:"2011错误",cl_er_2021:"2021错误",cl_er_2031:"2031错误",cl_er_3021:"3021错误",cl_er_3022:"3022错误",\
cl_er_3031:"3031错误",\
cl_er_3032:"3032错误",cl_er_4001:"4001错误",cl_er_4002:"4002错误",cl_er_4011:"4011错误",cl_er_5001:"5001错误",cl_er_5005:"5005错误",cl_er_5006:"5006错误",\
cl_er_6001:"6001错误",cl_er_9000:"9000错误",cl_er_9100:"9100错误",cl_er_9990:"9990错误",cl_er_9999:"9999错误",cl_er_time:"时间错误"
}
er_1004,er_2001,er_2011,er_2021,er_2031,er_3021,er_3022,er_3031,er_3032,er_4001,er_4002,er_4011,er_5001,er_5005,er_5006,er_6001,er_9000,er_9100,er_9990,er_9999,\
er_time = [0] * 21


#xls列头
cl_db_0,   cl_db_1,   cl_db_2,   cl_db_3,   cl_db_4,   cl_db_5,   cl_db_6,   cl_db_7,   cl_db_1014,cl_db_9011,cl_db_9021,cl_db_9031,cl_db_9051,cl_db_9052,\
cl_db_9053,cl_db_9054,cl_db_9061,cl_db_9071,cl_db_9072,cl_db_9073,cl_db_9074,cl_db_9075,cl_db_9076,cl_db_9081,cl_db_9082,cl_db_9100,cl_db_9101,cl_db_9102,\
cl_db_9103,cl_db_9109,cl_db_9301,cl_db_9303,cl_db_9304,cl_db_9305,cl_db_9306,cl_db_9307,cl_db_9308,cl_db_9309,cl_db_9310,cl_db_9331,cl_db_9332,cl_db_9333,\
cl_db_9401,cl_db_9993,cl_db_9994,cl_db_9995,cl_dt_volt = [i for i in xrange(i+1,i+48)]
dict4 = {
cl_db_0:"0_数量",      cl_db_1:"1_数量",      cl_db_2:"2_数量",      cl_db_3:"3_数量",      cl_db_4:"4_数量",      cl_db_5:"5_数量",      cl_db_6:"6_数量",\
cl_db_7:"7_数量",      cl_db_1014:"1014_数量",cl_db_9011:"9011_数量",cl_db_9021:"9021_数量",cl_db_9031:"9031_数量",cl_db_9051:"9051_数量",cl_db_9052:"9052_数量",\
cl_db_9053:"9053_数量",cl_db_9054:"9054_数量",cl_db_9061:"9061_数量",cl_db_9071:"9071_数量",cl_db_9072:"9072_数量",cl_db_9073:"9073_数量",cl_db_9074:"9074_数量",\
cl_db_9075:"9075_数量",cl_db_9076:"9076_数量",cl_db_9081:"9081_数量",cl_db_9082:"9082_数量",cl_db_9100:"CSQ值>14" ,cl_db_9101:"5<CSQ<=14",cl_db_9102:"CSQ其他值",\
cl_db_9103:"9103_数量",cl_db_9109:"9109_数量",cl_db_9301:"9301_数量",cl_db_9303:"9303_数量",cl_db_9304:"9304_数量",cl_db_9305:"9305_数量",cl_db_9306:"9306_数量",\
cl_db_9307:"9307_数量",cl_db_9308:"9308_数量",cl_db_9309:"9309_数量",cl_db_9310:"9310_数量",cl_db_9331:"9331_数量",cl_db_9332:"9332_数量",cl_db_9333:"9333_数量",\
cl_db_9401:"9401_数量",cl_db_9993:"9993_数量",cl_db_9994:"9994_数量",cl_db_9995:"9995_数量",cl_dt_volt:"电压数据"
}
ct_0,   ct_1,   ct_2,   ct_3,   ct_4,   ct_5,   ct_6,   ct_7,    ct_1014,ct_9011,ct_9021,ct_9031,ct_9051,ct_9052,ct_9053,ct_9054,ct_9061,ct_9071,ct_9072,ct_9073,\
ct_9074,ct_9075,ct_9076,ct_9081,ct_9082,ctg_9100,ct_9101,ct_9102,ct_9103,ct_9109,ct_9301,ct_9303,ct_9304,ct_9305,ct_9306,ct_9307,ct_9308,ct_9309,ct_9310,ct_9331,\
ct_9332,ct_9333,ct_9401,ct_9993,ct_9994,ct_9995 = [0] * 46


#xls列头
cl_fbox,cl_amvl,cl_shak,cl_agps,cl_coll,cl_imsi,cl_ccid,cl_numb = [i for i in xrange(i+1,i+9)]
dict5 = {
cl_fbox:"邮箱大小",cl_amvl:"报警阈值",cl_shak:"震动阈值",cl_agps:"GPS阈值",cl_coll:"G-S阈值",cl_imsi:"IMSI",cl_ccid:"CCID",cl_numb:"SIM号码"
}

#xls列头
cl_db_3001,cl_db_3002,cl_db_3003,cl_db_3004,cl_db_3005,cl_db_3006,cl_db_3007,cl_db_3008,cl_db_3009,cl_db_3010,cl_db_3011,cl_db_3012,cl_db_3013,cl_db_3014,\
cl_db_3015 = [i for i in xrange(i+1,i+16)]
dict6 = {
cl_db_3001:"3001_数量",cl_db_3002:"3002_数量",cl_db_3003:"3003_数量",cl_db_3004:"3004_数量",cl_db_3005:"3005_数量",cl_db_3006:"3006_数量",cl_db_3007:"3007_数量",\
cl_db_3008:"3008_数量",cl_db_3009:"3009_数量",cl_db_3010:"3010_数量",cl_db_3011:"3011_数量",cl_db_3012:"3012_数量",cl_db_3013:"3013_数量",cl_db_3014:"3014_数量",\
cl_db_3015:"3015_数量"
}
ct_3001,ct_3002,ct_3003,ct_3004,ct_3005,ct_3006,ct_3007,ct_3008,ct_3009,ct_3010,ct_3011,ct_3012,ct_3013,ct_3014,ct_3015 = [0] * 15







#conf 和 sim卡
st_fbox,st_amvl,st_shak,st_agps,st_coll,st_imsi,st_ccid,st_numb = [""] * 8


#车网平台 == "cwhl" or 马来西亚平台 == "mlxy"
ptform = "mlxy"




re_type = "<type>(\d{4})</type><time>"
re_time = "</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time>"
if ptform == "cwhl":
    re_conf = "^<iobd><conf><fbox>(\d{1,3})</fbox><acq><p>\d{1,3}</p><c>\d{1,3}</c><d>\d{1,3}</d></acq><alarm><b>(\d{1,3}.\d{1,2})</b><s>(\d{1,5})</s><acc-gps>(.{19,21})</acc-gps><acc-gsensor>(.{19,21})</acc-gsensor><collision>(\d{1,2}.\d{1,2})</collision></alarm><engine><emission>(-1|\d{1,5})</emission><form>(-1|(\d))</form></engine><smc><cm>\d{3,23}</cm><cu>\d{3,23}</cu><ct>\d{3,23}</ct></smc></conf></iobd>$"
elif ptform == "mlxy":
    re_conf = "^<iobd><conf><fbox>(\d{1,3})</fbox><acq><p>\d{1,3}</p><c>\d{1,3}</c><d>\d{1,3}</d></acq><alarm><b>(\d{1,3}.\d{1,2})</b><s>(\d{1,5})</s><acc-gps>(.{19,21})</acc-gps><acc-gsensor>(.{19,21})</acc-gsensor><collision>(\d{1,2}.\d{1,2})</collision></alarm><engine><emission>(-1|\d{1,5})</emission><form>(-1|(\d))</form></engine><smc><cm>(|\d{3,23})</cm><cu>(|\d{3,23})</cu><ct>(|\d{3,23})</ct></smc></conf></iobd>$"    
re_1004 = "^<iobd><type>(1002|1004)</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><voltage>(\d{1,2}.\d{6})</voltage><connect>1</connect></iobd>$"
re_2001 = "^<iobd><type>2001</type><time>(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)</time><condition><m>(-1|\d{1,10})</m>(|<am>\d{1,5}.\d{1,6}</am>)(|<af>(-1.0|\d{1,5}.\d{1,6})</af>)<f>(-1|.\d{0,2}(,.\d{0,2})*)</f><v>(\d{1,2}.\d{1,6})</v><r>(-1|\d{1,8})</r><i1>(\d{1,3}|-1.0)</i1><i2>-1.0</i2><s>(-1|.\d{0,2}(,.\d{0,2})*)</s>(|<l>(-1|\d{1,2})</l>)</condition></iobd>$"
re_2011 = "<gps><p><a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o>(|<l>.\d{0,3}.\d{6}</l>)<s>(\d{1,3}.\d{6})</s>"
#re_2011 = "^<iobd><type>2011</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<p><a>(-1.0|\d{2}.\d{6})</a><o>(-1.0|\d{2,3}.\d{6})</o><s>(-1.0|\d{1,3}.\d{6})</s>(<t>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</t>){0,1}</p>){1,3}</gps></iobd>$"
re_2021 = "^<iobd><type>2021</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><cellid><mcc>\d{1,5}</mcc><mnc>\d{1,5}</mnc><lac>(\d{1,7})</lac><count>\d{1,2}</count><cells>(\d{1,6},\d{1,3})+(;(\d{1,6},\d{1,3})+)*</cells></cellid></iobd>$"
re_2031 = "^<iobd><type>2031</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><acceleration>(<acc><c>\d</c><v>G,.\d{0,2}.\d{1,6}</v><t>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</t><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps></acc>){1,5}</acceleration></iobd>"
re_3021 = "^<iobd><type>3021</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><sms><from>(10010|10086)</from><msg>\w{1,300}</msg></sms></iobd>$"
re_3022 = "^<iobd><type>3022</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><sim><imsi>(\w{15})</imsi><ccid>(\w{20})</ccid><number>(|\d{11,13}|\+\d{11,15})</number></sim></iobd>$"
re_3031 = "^<iobd><type>3031</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><vin>(null|\w{17})</vin></iobd>$"
#re_3032 = "^<iobd><type>3032</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><pull_out_time>(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)</pull_out_time><gps><a>(-1.0|\d{2}.\d{6})</a><o>(-1.0|\d{2,3}.\d{6})</o><s>(-1.0|\d{1,3}.\d{6})</s></gps></iobd>$"
re_3032 = "^<iobd><type>3032</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><pull_out_time>(.{19,24})</pull_out_time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps></iobd>$"
re_4001 = "^<iobd><type>4001</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><vin>(null|\w{17})</vin></iobd>$"
re_4002 = "^<iobd><type>4002</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps>(|<warmup>\d{1,4}</warmup><idle>\d{1,4}</idle>)</iobd>$"
re_4011 = "^<iobd><type>4011</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><voltage>(\d{1,2}.\d{6})</voltage></iobd>$"
re_5001 = "^<iobd><type>5001</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><grade>\d{1,5}</grade></iobd>$"
re_5005 = "^<iobd><type>5005</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><grade>\d{1,5}</grade></iobd>$"
re_5006 = "^<iobd><type>5006</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><gps>(<a>-1.0</a><o>-1.0</o><s>-1.0</s>|<a>(\d{1,2}.\d{6})</a><o>(\d{2,3}.\d{6})</o><s>(\d{1,3}.\d{6})</s>)</gps><grade>\d{1,5}</grade></iobd>$"
re_6001 = "^<iobd><type>6001</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><diag><status>(\d{3})</status>(|<remain>\d{1,3}</remain>)<d><a>(-1|\d{1,3})</a><c>(.{1,300})</c></d></diag></iobd>$"
re_9000 = "^<iobd><type>9000</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><vin>(null|\w{17})</vin><dtu><signal_intensity>-\d{1,3}</signal_intensity><attach_time>\d{1,3}</attach_time></dtu><gps><fix>\d</fix><dop>(\d{1,2}.\d)(,\d{1,2}.\d)*</dop><satellite>\d{1,2},\d{1,2}</satellite></gps><gsensor><status>0</status><g_h_a>\d{1,3}</g_h_a></gsensor></iobd>$"
re_9100 = "^<iobd><type>9100</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><tacc><status>(\d{3})</status>(|<gps><a>(\d{1,2}.\d{6}</a><o>\d{2,3}.\d{6}</o><s>\d{1,3}.\d{6}</s></gps>\<gps><a>(\d{1,2}.\d{6}</a><o>\d{2,3}.\d{6}</o><s>\d{1,3}.\d{6}</s></gps><speed_list>(\d{1,3}.\d{1,2})(,\d{1,3}.\d{1,2})*</speed_list><speed_interval>\d{3,4}</speed_interval><time_consuming>\d{4,5}</time_consuming>)</tacc></iobd>$"
#re_9101 = "^<iobd><type>9100</type><time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}</time><tacc><status>\d{3}</status><gps><a>(\d{1,2}.\d{6}</a><o>\d{2,3}.\d{6}</o><s>\d{1,3}.\d{6}</s></gps>\<gps><a>(\d{1,2}.\d{6}</a><o>\d{2,3}.\d{6}</o><s>\d{1,3}.\d{6}</s></gps><speed_list>(\d{1,3}.\d{1,2})(,\d{1,3}.\d{1,2})*</speed_list><speed_interval>\d{3,4}</speed_interval><time_consuming>\d{4,5}</time_consuming></tacc></iobd>$"
re_9990 = "^<iobd><type>9990</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><exception>1000</exception></iobd>$"
re_9999 = "^<iobd><type>9999</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><debug><debug_infor>(-1|\d{1,4})</debug_infor>(<debug_string>(|NULL|.{0,70})</debug_string>){0,1}</debug><voltage>(\d{1,2}.\d{6})</voltage></iobd>$"
re_9310 = "^<iobd><type>9999</type><time>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</time><debug><debug_infor>(\d{1,4})</debug_infor><debug_string>221.122.126.9</debug_string></debug><voltage>(\d{1,2}.\d{6})</voltage></iobd>$"



