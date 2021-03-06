# -*- coding: utf-8 -*-

'''create_msg_h_file module'''


def _parse_place_bit(start = 0, length = 0, sig = None):
    str1 = ''
    name = ''
    ordering = True
    length_byte = 0

    if sig is not None:
        start = sig.start_bit
        length = sig.length_bit
        name = sig.name
        ordering = sig.ordering
        length_byte = sig.get_length_byte()

    if length == 0:
        return ''

    assumption_len = length + (start % 8)
    assumption_byte = assumption_len / 8
    if (assumption_len % 8) > 0:
        assumption_byte += 1

    byte_count = 1

    # 起始bit不规整
    # 如起始bit为11 (8+3)则需要先补齐上一个字节，这里是(8-3)先补齐5bit
    if (start % 8) > 0:
        pre_len = 8 - start % 8
        if (len(name) == 0) and (assumption_byte == 1):
            str1 += 'uint8_t :' + str(length) + ';\n\t\t' # uint8_t :2
            return str1
        elif (len(name) == 0) and (assumption_byte > 1):
            str1 += 'uint8_t :' + str(pre_len) + ';\n\t\t' # uint8_t :2
        elif (len(name) != 0) and (assumption_byte == 1):
            str1 += 'uint8_t ' + name + ':' + str(length) + ';\n\t\t' # uint8_t gear:3
            return str1
        elif (len(name) != 0) and (assumption_byte > 1):
            if ordering: # 有名称且为升序 intel
                str1 += 'uint8_t ' + name  + '_' + str(assumption_byte) + ':' + str(pre_len) + ';\n\t\t' # uint8_t vehicle_speed_2:4
            else: # 有名称且为降序 motorola
                str1 += 'uint8_t ' + name  + '_' + str(byte_count) + ':' + str(pre_len) + ';\n\t\t' # uint8_t vehicle_speed_1:4
        else:
            pass

    # 起始bit规整，且只有1个字节的
    if (start % 8) == 0 and assumption_byte == 1:
        if len(name) == 0:
            str1 += 'uint8_t :' + str(length) + ';\n\t\t' # uint8_t :2
        else:
            if length == 8:
                str1 += 'uint8_t ' + name + ';\n\t\t' # uint8_t temp
            else:
                str1 += 'uint8_t ' + name + ':' + str(length) + ';\n\t\t' # uint8_t gear:3
        return str1
    # 起始bit规整，且大于1个字节的
    elif (start % 8) == 0 and assumption_byte > 1:
        if len(name) == 0:
            str1 += 'uint8_t :8;' + '\n\t\t' # uint8_t :8;
        else:
            if ordering: # 有名称且为升序 intel
                str1 += 'uint8_t ' + name  + '_' + str(assumption_byte - byte_count + 1) + ';\n\t\t' # uint8_t vehicle_speed_2
            else: # 有名称且为降序 motorola
                str1 += 'uint8_t ' + name  + '_' + str(byte_count) + ';\n\t\t' # uint8_t vehicle_speed_2
    else:
        pass

    # 执行到此都是多于1个字节的
    assumption_len -= 8
    byte_count += 1

    count1 = 0
    sum = int(assumption_len / 8)

    # 处理整字节
    while count1 < sum:
        if len(name) == 0:
            str1 += 'uint8_t :8;' + '\n\t\t' # uint8_t :8;
        else:
            if ordering: # 有名称且为升序 intel
                str1 += 'uint8_t ' + name  + '_' + str(assumption_byte - byte_count + 1) + ';\n\t\t' # uint8_t vehicle_speed_2
            else: # 有名称且为降序 motorola
                str1 += 'uint8_t ' + name  + '_' + str(byte_count) + ';\n\t\t' # uint8_t vehicle_speed_2

        byte_count += 1
        count1 += 1
        assumption_len -= 8

    # 有结余
    if (assumption_len % 8) > 0:
        if len(name) == 0:
            str1 += 'uint8_t :' + str(assumption_len % 8) + ';\n\t\t'
        else:
            if ordering:
                str1 += 'uint8_t ' + name  + '_1' + ':' + str(assumption_len % 8) + ';\n\t\t' # uint8_t vehicle_speed_1:4
            else:
                str1 += 'uint8_t ' + name  + '_' + str(byte_count) + ':' + str(assumption_len % 8) + ';\n\t\t' # uint8_t vehicle_speed_2:4
    else:
        pass

    if len(str1) == 0:
        raise TypeError('parase place bit error!')

    return str1

# def create_msg_h_file(root_path, out_path, message_list, dbc_file_name):
def create_msg_h_file(root_path, msg_h_output_path, dbc_list):
    if len(root_path) == 0 or len(dbc_list) == 0:
        raise TypeError('root path or message list is error!')

    target_f_path = msg_h_output_path

    dbc_obj = dbc_list[0]
    valid_file_name = dbc_obj.valid_file_name

    try:
        tar_f = open(target_f_path, 'w')
    except:
        raise TypeError('operate msg.h file fail!')

    str1 = '#ifndef CAN_STACK_' + valid_file_name.upper() + '_MSG_H\n'
    str1 += '#define CAN_STACK_' + valid_file_name.upper() + '_MSG_H\n\n'
    str1 += r'#include "canstack_sig.h"' + '\n\n'
    str1 += '#ifdef CANSTACK_' + valid_file_name.upper() + '\n'

    tar_f.write(str1)

    str1 = '\n' + '/* about messages */'
    tar_f.write(str1)

    str1 = '\ntypedef union' + '\n' + '{' + '\n\t' + 'uint8_t byte[8];'
    tar_f.write(str1)

    for dbc in dbc_list:
        message_list = dbc.message_list
        str1 = '\n/********************' + 'CAN_' + str(dbc.can_channel) + '********************/'
        tar_f.write(str1)
        for message in message_list:
            tar_f.write('\n\n\t')

            str1 = '/* ' + message.name + ':'+ message.ID + ' */' + '\n\t' + 'struct' + '\n\t' + '{' + '\n\t\t'
            tar_f.write(str1)

            count = 0

            while count < message.all_sig_sum - 1:
                sig = message.all_sig_list[count]
                if count == 0 and sig.start_bit > 0:
                    str1 = _parse_place_bit(0, sig.start_bit)
                    tar_f.write(str1)
                # parase_placeholder_bit(start = 0, length = 0, sig = None)
                str1 = _parse_place_bit(0, 0, sig)
                tar_f.write(str1)

                sig1 = message.all_sig_list[count + 1]
                # 如果当前信号跟后一个信号间有空字段
                if (sig1 != None) and ( (sig.start_bit + sig.length_bit) < sig1.start_bit ):
                    str1 = _parse_place_bit(sig.start_bit + sig.length_bit, sig1.start_bit - (sig.start_bit + sig.length_bit))
                    tar_f.write(str1)

                count += 1
            # 处理最后一个sig 也有可能是唯一的一个
            sig = message.all_sig_list[count]
       
            if count == 0 and sig.start_bit > 0:
                str1 = _parse_place_bit(0, sig.start_bit)
                tar_f.write(str1)

            str1 = _parse_place_bit(0, 0, sig)
            tar_f.write(str1)
            # 如果最后一个信号到 bit64间有空字段
            if (sig.start_bit + sig.length_bit) < 64:
                str1 = _parse_place_bit(sig.start_bit + sig.length_bit, 64 - (sig.start_bit + sig.length_bit))
                tar_f.write(str1)

            str1 = '\n\t}' + message.name + ';'
            tar_f.write(str1)

    str1 = '\n}canstack_msg_data_t;'
    tar_f.write(str1)

    str1 = '\n\ntypedef enum\n'
    str1 += '{\n'
    for dbc in dbc_list:
        str1 += '\t/****CAN_' + str(dbc.can_channel) + '****/\n'
        cnt = 0
        for msg in dbc.message_list:
            str1 += '\t' + msg.name.upper() + ' = ' + str(cnt) + ',\n'
            cnt += 1

    str1 += '}msg_type;'

    tar_f.write(str1)

    str1 = '\n\n#endif\n\n#endif\n'
    tar_f.write(str1)

    tar_f.close()

    print('create msg.h file success!')
