# -*- coding: utf-8 -*-
'''create_alarm_sig_infor_file module'''

def create_alarm_sig_infor_file(f_path, dbc_list):
    assert len(f_path) > 0 and len(dbc_list) > 0, 'param error!'

    try:
        tar_f = open(f_path, 'w')
    except:
        raise Exception

    msg_list = []
    for dbc in dbc_list:
        msg_list += dbc.message_list

    exist_alarm_sig_flag = False

    for msg in msg_list:
        str1 = ''
        if len(msg.alarm_sig_list) > 0:
            exist_alarm_sig_flag = True
            str1 += '--------------  ' + msg.name + '  ' + msg.ID+'  --------------\n'

            for sig in msg.alarm_sig_list:
                str1 += sig.name + '  -------\n'
                temp_dic = sig.get_state_dict()
                key_list = sorted(temp_dic.keys())

                for key in key_list:
                    str1 += '\t' + key + '\t-------->\t' + temp_dic[key] + '\n'

            str1 += '\n'
            tar_f.write(str1)

    if not exist_alarm_sig_flag:
        str1 = \
'''\

   寒雨连江夜入吴，
   平明送客楚山孤。
   洛阳亲友如相问，
   一片冰心在玉壶。

             ---唐.王昌龄
'''
        tar_f.write(str1)

    tar_f.close()