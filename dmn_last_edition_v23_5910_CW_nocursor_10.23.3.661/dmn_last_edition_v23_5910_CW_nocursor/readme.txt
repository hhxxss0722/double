'''
使用方法
1.ctrl_sign : 控制软件运行的平台环境
    'GR' : 车网互联 - 外网环境linux
    'DM' : 车网互联 - demo环境linux
    'JG' : 成都建国 - 外网环境window
    **在其后的条件判断中，按照格式更改保存结果的path，数据库ip/port/权限变化时相应更改**

2.非自动从数据库获取imei号时，需设置存放imei的txt路径，按照格式

3.count_threading : 控制软件线程数量

4.运行方式、数据处理、排查日期可选择

    A.双击main.py
        每天2点自动从数据库获取imei号，查询前一天的数据，处理数据并email结果

    B.其他指定执行方式
        Example:
        python d:\dmn_last_edition_v04_4C01_ALL\main.py 0  ym 4
                                ①                      ② ③ ④
            ① : 运行main.py
            ② : 0表示自动从数据库获取imei号，hour等于02时(每天2点)自动执行程序，主要用于定时执行程序
                 1表示自动从数据库获取imei号，立即执行程序，主要用于定时执行程序出现意外，手动执行程序
                 2表示非自动获取imei号，根据imei.txt的imei查询数据，主要用于一次性指定imei号的数据查询
                 3表示非自动获取imei号，每隔一段时间循环执行数据查询，主要用于循环指定imei号的数据查询
            ③ : ym表示进行数据处理，同时邮件发送结果；nm表示不进行数据处理，不邮件发送结果
            ④ : 该位表示排查日期，比如：今天是12月01日，要查询11月28日的数据，则该位为3，即：12月01日 - 11月28日

5.使用数据库及表的情况 -- 车网平台
    1.mongo "10.21.1.122"
        ①.login_record：获取设备的登录登出时间记录
    2.mysql "10.21.1.189"
        ①.obd.terminal：获取设备的tid、imsi、主控CM3版本、集团、网点、设备类型等
        ②.以下sql：获取车牌、vin、车型、型号
        "select a.* from auto.vehicle a,obd.terminal_vehicles b where b.terminal_id =" +str(terminal_id)+" and b.vehicle_id = a.vehicle_id"
        "select * from auto.style where style_id=" +str(style_id)
        "select * from auto.model where model_id=" +str(model_id)
    3.mysql "10.21.1.33"
        ①.tcm.upgrade_history：获取设备的升级记录
    4.hadoop "10.21.2.129"
        ①.obd_raw_data：获取设备的原始报文
'''



'''
version说明：

十四.dmn_last_edition_v19_5330_cw  ------- 仅获取原始报文和解析原始报文


十三.dmn_last_edition_v18_5330_ALL  ------ 使用impyla获取原始报文完整版本.


十二.dmn_last_edition_v17_5317_ALL
    01.去掉TCM数据库查询的ORDER BY DESC，改为ORDER BY ASC

十一.dmn_last_edition_v16_5303_ALL
    01.增加运行时长、安全域、用户最近登录APP时间、用户手机号码、写包时间错误对应的列
    02.修改时间错误为时间格式错误
    03.运行时长：有绑定时间记录的，将最近登录登出时间 - 绑定时间；无绑定时间记录的，以最近登录登出时间 - 首次登录时间
    04.整理程序使用的sql语句
    05.修改所有re的时间适配，201/d → /d{4}，写包时间错误另行处理
    06.修改re_2001,兼容增加油耗字段的2001包
    07.修复<i1>字段不兼容问题
    08.增加用户登录APP和设备登录登出的行为分析
    09.增加9303包的处理，体现在BUG.xls中
    10.连续运行时，修复imei_list不清空的问题
    11.增加JG主控未升级成功，自动下发，优化逻辑
    12.修正RE_9000的适配问题（dop）字段
    
十.dmn_last_edition_v15_5224_ALL
    01.SELECT * 修改成 SELECT 所需的列，加快速度
    02.增加对配置信息的字段适配解析，<发动机相关的字段>
    03.修改re_2011，兼容之前的2011包

九.dmn_last_edition_v13_5126_ALL
    01.因数据库存放group位置的变化，增加一个mysql连接，并解析
    02.在目录中存放group数字对应客户的名称
    03.增加9304、9305、9306、9307 DEBUG包的解析
    04.model_sign == 2时，开一个线程
    05.修复不break时保存的文件名相同的BUG

八.dmn_last_edition_v12_5110_ALL
    01.优化login和logout的处理，配置较差的设备以便节省时间
    02.优化pymongo的数据处理，节省时间，有待进一步优化
    03.优化全车诊断的写入顺序
    04.修复全车诊断的统计BUG
    05.增加9301\9302\9303 DEBUG包的统计，分别对应SIM卡异常/POWERON引脚重启/RST引脚重启
    06.3021适配10010的转发短信
    07.修复col_dgtg,col_tacc没有递增

七.dmn_last_edition_v11_4C16_ALL
    01.修改正则表达式 2014为201\d
    02.修复设备是否恢复的判断

六.dmn_last_edition_v10_4C16_ALL
    01.增加GPS两点间距离的处理，两点间的直线距离大于3km且有点火，在col_distance显示
    02.C1设备的主控和cm3为出厂版本，自动下发短信重启指令
    03.前第5天正常，后4天连续异常，自动下发短信重启指令

五.dmn_last_edition_v09_4C15_ALL
    01.增加3032包的判断和处理
    02.不再根据配置包的数量作为登录的数据
    03.增加登录、登出的统计count_in and count_out
    04.修改VIN是否支持的条件，4001 + 9061综合判断，避免因重启而上报null
    05.2001时间间隔异常时，不再统计到er_2001,而是er_rate_2001

四.dmn_last_edition_v08_4C12_ALL
    01.增加对2001包时间间隔的判断， col_rate2001栏
    02.6001包内的故障码字段数量增加至300

三.dmn_last_edition_v06_4C11_ALL
    01.增加自动执行程序的设定
    02.增加col_carvin栏，判断4001中是否支持vin
    03.增加col_vin_value栏，填入4001中的vin
    04.在col_date栏增加设备的登录登出情况，用于当前在线状态的判断

二.dmn_last_edition_v05_4C02_ALL
    01.修复ismail参数的错误
    02.model_sign !=0时，修改邮件收件人
    03.修改pk2001方法中mileage的判断条件，两个里程相差大于30，判定为里程异常
    04.xlshd.py对ctrl_sign的值进行不同的gps acc判断
    05.datahd.py对漏报点火的条件修改

一.dmn_last_edition_v04_4C01_ALL 当作初版吧.
    功能如下：
        01.自动获取已使用的C1/C2设备imei号，作为软件要查询的imei号
        02.获取C1/C2设备的起始登录时间
        03.设备排查日期是否登录
        04.设备上报的车辆数据是否存在明显异常
        05.获取设备内的SIM卡号、主控版本、CM3版本、集团、网点信息
        06.获取设备绑定的车型、型号、VIN、车牌信息
        07.解析平台下发的配置信息，油箱大小、低压阈值、震动阈值、GPS加速阈值、碰撞阈值
        08.所有上行数据包的数量统计
        09.登录次数、重复上报、漏报点火、误报熄火、延迟上报、重启次数的统计
        10.所有上行数据包格式的检查
        11.所有DEBUG数据包的数量统计
        12.打印所有数据包中电压集合
        13.根据以上的数据生成BUG.xls供参考
'''

'''
数据包解析情况
1.配置信息
<iobd><conf><fbox>52</fbox><acq><p>15</p><c>150</c><d>300</d></acq><alarm><b>11.3</b><s>50</s><acc-gps>0.70,-0.85,25.0,20.0</acc-gps><acc-gsensor>1.20,-1.20,1.60,1.60</acc-gsensor><collision>7.0</collision></alarm><smc><cm>1069013305711</cm><cu>1069013305711</cu><ct>1069013305711</ct></smc></conf></iobd>
解析字段:
	<fbox>52</fbox>
	<b>11.3</b>
	<s>50</s>
	<acc-gps>0.70,-0.85,25.0,20.0</acc-gps>
	<collision>7.0</collision>

2.所有上行数据包
解析字段：
	字段格式匹配
	<type>1004</type>
	<time>2014-12-01 19:13:24</time>
	data_process_time（平台接收数据时间）
	
3.1004
解析字段：
	<voltage>(\d{1,2}.\d{6})</voltage>

4.2001
解析字段：
	<m>(-1|\d{1,10})</m>
	<am>\d{1,5}.\d{1,6}</am>
	<f>(-1|.\d{0,2}(,.\d{0,2})*)</f>
	<v>(\d{1,2}.\d{1,6})</v>
	<r>(-1|\d{1,8})</r>
	<i1>-1.0</i1>
	<i2>-1.0</i2>
	<s>(-1|.\d{0,2}(,.\d{0,2})*)</s>
	<l>\d{1,2}</l>

5.2011
解析字段：
	<s>(\d{1,3}.\d{6})</s>
	
6.2021
解析字段：
	<lac>(\d{1,7})</lac>

7.2031
解析字段：
	暂无
	
8.3021
解析字段：
	暂无

9.3031
解析字段：
	暂无

10.4001
解析字段：
	<vin>(null|\w{17})</vin>

11.4002
解析字段：
	<s>(\d{1,3}.\d{6})</s>

12.4011
解析字段：
	<voltage>(\d{1,2}.\d{6})</voltage>

13.5001
解析字段：
	<s>(\d{1,3}.\d{6})</s>	
	<grade>\d{1,5}</grade>
	
14.5005
解析字段：
	<grade>\d{1,5}</grade>	
	
15.5006
解析字段：
	<grade>\d{1,5}</grade>	
	
16.6001
解析字段：
	<status>\d{3}</status>		
	<a>(-1|\d{1,3})</a>
	<c>(.{1,150})</c>

17.9000
解析字段：
	暂无		
	
18.9100
解析字段：
	暂无		
	
19.9990
解析字段：
	<exception>\d{1,5}</exception>
	
20.9999
解析字段：
	<debug_infor>(\d{1,4})</debug_infor>
	<debug_string>(|NULL)</debug_string>
	<voltage>(\d{1,2}.\d{6})</voltage>			

21.BNDS
解析字段：
	暂无	
'''