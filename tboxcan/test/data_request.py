import re
import urllib.request

# para_info = {
#         'bt': '12345',
#         'ws': '1',
#         'csq': '14',
#         'isw': '1',
#         'bsw': '1',
#         'esw': '1',
#         'sbs': '1',
#         'Kl15': '1',
#         'schrg': '1',
#         'fchrg': '1',
#         'ILED': '1',
#         'BLED': '1',
#         'ELED': '1',
#         'HD2': '1',
#         'HD1': '1',
#         'Backup': '1',
#         'Adc3': '(3.7,4.2]',
#         'Adc2': '(11.7,12.3]',
#         'Adc1': '(11.7,12.3]',
#         'eeprom': '1',
#         'wifiap': '1',
#         'call': '1',
#         'imsi': '1',
#         '4gsoft': 'EC20CFAR02A08M4G',
#         'qc': '12345',
#         'app': '12345',
#         'battery': '1',
#         'emmc': '1',
#         'cryc': '1',
#         'crym': '1',
#         'can': '1',
#         'led': '1',
#         'gpsStrength': '(38,50]',
#         'gpsPosiTime': '[10,60]',
#     }
#发送测试结果到平台，可以对测试结果进行筛选排查
#初始化参数为测试结果的字典类型，key必须在para_config.tx中，可以多于该集合

class Data_request():
    #初始化并判断结果是否有错误和遗漏的
    def __init__(self, can_dict):
        # self.para_dict = {
        #     'bt': '',
        #     'ws': '',
        #     'csq': '',
        #     'isw': '',
        #     'bsw': '',
        #     'esw': '',
        #     'sbs': '',
        #     'Kl15': '',
        #     'schrg': '',
        #     'fchrg': '',
        #     'ILED': '',
        #     'BLED': '',
        #     'ELED': '',
        #     'HD2': '',
        #     'HD1': '',
        #     'Backup': '',
        #     'Adc3': '',
        #     'Adc2': '',
        #     'Adc1': '',
        #     'eeprom': '',
        #     'wifiap': '',
        #     'call': '',
        #     'imsi': '',
        #     '4gsoft': '',
        #     'qc': '',
        #     'app': '',
        #     'battery': '',
        #     'emmc': '',
        #     'cryc': '',
        #     'crym': '',
        #     'can': '',
        #     'led': '',
        #     'gpsStrength': '',
        #     'gpsPosiTime': '',
        #     'imei': '',
        #     'model': '',
        #     'batch': ''
        # }
        f = open('para_config.txt')
        self.all_para = eval(f.read())
        f.close()
        self.para_dict = can_dict
        self.data_judge(self.para_dict)
        self.url = self.url_format(self.para_dict)
    #发送结果到平台
    def send_data(self):
        req_result = urllib.request.urlopen(self.url).read()
        return req_result

    def url_format(self,data_dict):
        self.head = 'http://www.che08.com/tcm-ice/ws/0.1/inspections/upload?proc=10&imei={imei}&model={model}&batch={batch}'
        url = self.head.format(imei=data_dict['imei'],model=data_dict['model'],batch=data_dict['batch'])
        for para in self.all_para  :
            if para in data_dict:
                url = url + '&' + para + '=' + data_dict[para]
        print(url)
        return url

    def data_judge(self, can_dict):
        re_open_close = re.compile(r'\((.+),(.+)\]')
        re_close_open = re.compile(r'\[(.+),(.+)\)')
        re_close_close = re.compile(r'\[(.+),(.+)\]')
        re_open_open = re.compile(r'\((.+),(.+)\)')
        lack_para = []
        err_para = []
        #----judge data
        for key in self.all_para :
            if key in can_dict:
                range_value = self.all_para[key]
                can_value = can_dict[key]
                if can_value == range_value:
                    pass
                else:
                    can_value = eval(can_value)
                    if range_value.startswith('(') and range_value.endswith(')'):
                        re_result = re_open_open.search(range_value)
                        if can_value > eval(re_result.group(1)) and can_value < eval(re_result.group(2)):
                            pass
                        else:
                            err_para.append(key)
                    elif range_value.startswith('(') and range_value.endswith(']'):
                        re_result = re_open_close.search(range_value)
                        if can_value > eval(re_result.group(1)) and can_value <= eval(re_result.group(2)):
                            pass
                        else:
                            err_para.append(key)
                    elif range_value.startswith('[') and range_value.endswith(')'):
                        re_result = re_close_open.search(range_value)
                        if can_value >= eval(re_result.group(1)) and can_value < eval(re_result.group(2)):
                            pass
                        else:
                            err_para.append(key)
                    elif range_value.startswith('[') and range_value.endswith(']'):
                        re_result = re_close_close.search(range_value)
                        if can_value >= eval(re_result.group(1)) and can_value <= eval(re_result.group(2)):
                            pass
                        else:
                            err_para.append(key)
                    else:
                        err_para.append(key)
            else:
                lack_para.append(key)
        print('lack para list:' + str(lack_para))
        print('error para list:' + str(err_para))