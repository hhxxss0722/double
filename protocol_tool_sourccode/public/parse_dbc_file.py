# -*- coding: utf-8 -*-

"""parseDBC module"""
import re
import chardet

from public.sig_class import *
from public.message_class import *
from public.utility import *
from public.formula_class import *

_alarm_sig_prefix = 'alarm_'

GROUP_SIG_LIST = []

valid_encode_list = ['ascii', 'utf-8']

# all_sig_list, bat_alarm_sig_list
# sig_dic, bat_alarm_dic
def parse_dbc_file(file_path, all_sig_infor_dic, bat_alarm_dic, group_infor_dic):
    if len(file_path) == 0 or len(all_sig_infor_dic) == 0 or len(bat_alarm_dic) == 0 or len(group_infor_dic) == 0:
        print('***********************ERROR!***********************')
        print_cur_info()
        quit(1)

    print('enter parse_dbc_file fun!\n')

    global GROUP_SIG_LIST
    GROUP_SIG_LIST = (group_infor_dic['group2list']).keys()

    # if len(file_name) == 0 or len(root_path) == 0:
    #     raise TypeError('root path or file name is none!')
    #
    # file_path = root_path + '\\' + file_name

    dbc_f = open(file_path, 'rb')
    dbc_lines = dbc_f.readlines()
    message_list = []
    sig_state_inf_list =[]
    mes_var1 = re.compile(r'BO_\s+(\d+)\s+(\w+)+.*\s+(\d)')
    sig_var1 = re.compile(r'SG_\s+(\w+)\s:\s(\d+)\|(\d+)@(\d)(.)\s+\((.+),(.+)\)\s+\[(.+)\|(.+)\]\s+\"(.*)\"')
    sig_state_var1 = re.compile(r'VAL_\s+(\d+)\s+(\w+)\s+(.*);')
    # BA_ "GenMsgCycleTime" BO_ 2550267892 100;
    # BA_ "GenSigStartValue" SG_ 2565819119 bat_cell_temp 40;
    mes_var2 = re.compile(r'BO_\s(\d+)\s(\d+)')

    dbc_line_sum = len(dbc_lines)
    # print('dbc_line_sum = %d\n' % dbc_line_sum)
    if dbc_line_sum == 0:
        raise TypeError('dbc readlines fail!')

    cnt = 0
    # 存放sig对象的list
    sig_list = []
    period_dict = dict()

    while cnt < dbc_line_sum:
        text_line = dbc_lines[cnt].strip()
        # print('text_line = %s' % text_line)
        # parse message
        # BO_ 2565866755 ETC2: 8 Vector__XXX
        if text_line.startswith('BO_ '):
            mes_var1_result = mes_var1.search(text_line)
            temp_line = dbc_lines[cnt + 1].strip()
            # 如果只有一行BO_ XXX暂不处理
            if len(temp_line) == 0:
                cnt += 1
                pass
            else:
                try:
                    mes_raw_id = mes_var1_result.group(1)
                    mes_name = mes_var1_result.group(2)
                    dlc = int(mes_var1_result.group(3))
                    # 默认周期是1000ms，后面会调整
                    message1 = Message(mes_name, mes_raw_id, dlc)
                    # 追加到链表中
                    message_list.append(message1)
                except:
                    raise TypeError('parse message error! line = %s' % str(cnt + 1))
        # parse sig
        if text_line.startswith('SG_ '):
            sig_var1_result = sig_var1.search(text_line)
            temp_line = dbc_lines[cnt - 1].strip()
            # 如果只有一行SG_ XXX暂不处理
            if len(temp_line) == 0:
                cnt += 1
                pass
            else:
                sig_name = sig_var1_result.group(1)

                # if sig name is not empty and sig name is valid then save it
                #  SG_ vehicle_speed : 24|8@1+ (1,0) [0|250] "km/h" Vector__XXX
                #           1         2      3     4   5       6    7          8     9          10
                # (r'SG_\s+(\w+)\s:\s(\d+)\|(\d+)@(\d)(.)\s+\((.+),(.+)\)\s+\[(.+)\|(.+)\]\s+\"(.*)\"')
                is_valid, isBatalarm, suffix, zh_name, formula = _is_valid_sig(sig_name, all_sig_infor_dic, bat_alarm_dic)
                if (len(sig_name) > 0) and is_valid:
                    try:
                        sig_start_bit = int(sig_var1_result.group(2))
                        sig_length_bit = int(sig_var1_result.group(3))
                        sig_ordering = int(sig_var1_result.group(4))
                        sig_isSigned = sig_var1_result.group(5)
                        sig_scale = float(sig_var1_result.group(6))
                        sig_offset = int(sig_var1_result.group(7))
                        sig_min_val = float(sig_var1_result.group(8))
                        sig_max_val = float(sig_var1_result.group(9))
                        sig_unit = sig_var1_result.group(10)
                        # flag = False
                        # 1:intel 0:motorola (reversed order)
                        if sig_ordering == 1:
                            flag = True
                        else:
                            flag = False
                        # +:unsigned -:signed
                        if sig_isSigned == '+':
                            flag1 = False
                        else:
                            flag1 = True

                        #if len(sig_unit) > 0:
                            #x = chardet.detect(sig_unit)
                            #if x['encoding'] not in valid_encode_list:
                                ## sig_unit = sig_unit.decode('windows-1252')
                                ## if sig_unit use windows-1252 coding, replace with 口口
                                #sig_unit = u'\u25a1\u25a1'
                            #else:
                                #sig_unit = sig_unit.decode('utf-8')

                        message1 = message_list[-1]
                        # (self, name, zh_name, suffix, start_bit, length_bit, ordering, isSigned, scale, offset, min_val, max_val, unit, message, formula)
                        sig1 = Sig(sig_name, zh_name, suffix, sig_start_bit, sig_length_bit, flag, flag1, sig_scale,
                                   sig_offset, sig_min_val, sig_max_val, sig_unit, message1, formula)

                        sig1.set_bat_alarm_flag(isBatalarm)

                        sig_list.append(sig1)
                    except:
                        raise TypeError('parse sig error! line = %s' % str(cnt + 1))

                # print('cnt = %d' % cnt)
                if cnt + 1 <= dbc_line_sum:
                    temp_line = dbc_lines[cnt + 1].strip()
                    # 如果是最后一行SG_ XXX 就把sig_list放到“最新”的message中
                    if len(temp_line) == 0:
                        if len(message_list) == 0:
                            raise TypeError('no message object!')
                        # 获得最后一个message
                        message1 = message_list[-1]

                        # dbc默认所有信号属于一个默认的报文——vector__independent_sig_msg，ID=0x0
                        # current message's ID is invalid or sig list is empty, delete current message
                        if int(message1.ID, 16) == 0 or len(sig_list) == 0:
                            message_list.pop()
                        elif message1.dlc > 8:
                            raise TypeError('[%s] message\'s dlc greater than 8' % message1.name)
                        else:
                            # 设置message的sig_list
                            message1.set_sig_list(sig_list)
                        # 清空sig_list
                        # print('sig_list len = %d' % len(sig_list))
                        # sig_list.clear()
                        sig_list = list([])
        # parse message period
        if text_line.startswith('BA_ \"GenMsgCycleTime\"'):
            mes_var2_result = mes_var2.search(text_line)
            try:
                mes_raw_id = mes_var2_result.group(1)
                mes_period = mes_var2_result.group(2)
                period_dict[mes_raw_id] = mes_period
            except:
                raise TypeError('parse message period error! line = %s' % str(cnt + 1))
        # parse sig state
        # VAL_ 2566844695 mileage_brk_pedal 3 "Not Available or not installed" 2 "Error " 1 "Brake Pedal Depressed " 0 "Brake Pedal Released" ;
        # VAL_ 2566844704 led_error 18 "0" 19 "1" 20 "2" 21 "3" ;
        #                                   1       2       3
        # sig_s_var = re.compile(r'VAL_\s+(\d+)\s+(\w+)\s+(.*);')
        if text_line.startswith('VAL_ '):
            sig_state_result = sig_state_var1.search(text_line)
            infor_dic = {}

            try:
                infor_dic['msg_raw_id'] = sig_state_result.group(1)
                infor_dic['sig_name'] = sig_state_result.group(2).lower()
                content_str = sig_state_result.group(3)
            except:
                raise Exception('parse sig state error! line = %s' % str(cnt + 1))
            else:
                temp_list = content_str.strip().split('"')
                temp_list.pop()

                key_list = []
                val_list = []

                cnt1 = 0
                while cnt1 < len(temp_list) / 2:
                    key = temp_list[2 * cnt1 + 0].strip()
                    key_list.append(key)

                    val = temp_list[2 * cnt1 + 1].strip()
                    val_list.append(val)
                    cnt1 += 1

                infor_dic['state_dic'] = dict(zip(key_list, val_list))

            sig_state_inf_list.append(infor_dic)

        cnt += 1

    # print(period_dict)

    # 判断有误重复项
    # s1 = set(period_dict.keys())
    # if len(s1) != len(message_list):
    #     raise TypeError('message period block have repetitive item!')
    # 判断
    # if len(s1) != len(message_list):
    #     raise TypeError('message infor and message period do not correspond!')
    raw_id_key_list = list(period_dict.keys())
    for msg in message_list:
        # 查看在id表中是否存在该id
        if raw_id_key_list.count(msg.raw_id) > 0:
            msg.period = period_dict[msg.raw_id]

        for dic in sig_state_inf_list:
            if dic['msg_raw_id'] == msg.raw_id:
                for sig in msg.all_sig_list:
                    if dic['sig_name'] == sig.name:
                        sig.set_state_dict(dic['state_dic'])

    dbc_f.close()

    print('parse dbc file success!')
    return message_list

# if sig is valid?
# return isValidSig,isBatalarm,suffix,zh_name,formula

# (self, sig_name, offset, scale, length, min_val, max_val, invalid_val, unit)
def _is_valid_sig(sig_name, all_sig_infor_dic, bat_alarm_sig_dic):

    if sig_name in all_sig_infor_dic.keys():
        sig_infor_dic = all_sig_infor_dic[sig_name]
        zh_name = sig_infor_dic["zh_name"]
        suffix = ''
        valid_name = sig_name
        isBatalarm = False
    elif (sig_name in bat_alarm_sig_dic.keys()):
        sig_infor_dic = all_sig_infor_dic["alarm_sig_name"]
        zh_name = bat_alarm_sig_dic[sig_name]
        suffix = ''
        valid_name = sig_name
        isBatalarm = True
    elif sig_name.startswith(_alarm_sig_prefix):
        sig_infor_dic = all_sig_infor_dic["alarm_sig_name"]
        zh_name = sig_name
        suffix = ''
        valid_name = sig_name
        isBatalarm = False

    else:
        prefix_list = GROUP_SIG_LIST
        suffix = ''
        for prefix in prefix_list:
            if sig_name.startswith(prefix):
                sig_infor_dic = all_sig_infor_dic[prefix]
                suffix = sig_name[len(prefix):]
                zh_name = sig_infor_dic['zh_name'] + suffix
                valid_name = prefix
                isBatalarm = False
        # use suffix as flag, judge if sig in GROUP_SIG_LIST
        if len(suffix) == 0:
            return False,False,'','',None

    sig_formula = sig_infor_dic['formula']

    _check_formula(sig_formula)

    formula = Formula(valid_name, sig_formula['offset'], sig_formula['scale'], \
                      sig_formula['length'], sig_formula['min_val'], sig_formula['max_val'], \
                      sig_formula['invalid_val'], (sig_formula['unit']))

    return True, isBatalarm, suffix, zh_name, formula


def _check_formula(sig_formula):
    try:
        offset  = float(sig_formula["offset"])
        scale   = float(sig_formula["scale"])
        length  = int(sig_formula["length"])
        max_v   = float(sig_formula["max_val"])
        min_v   = float(sig_formula["min_val"])
    except:
        raise Exception('sig: %s config has error' % sig_formula["sig_name"])
