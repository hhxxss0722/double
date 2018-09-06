# -*- coding: utf-8 -*-

"""parse_all_sigs_file module"""
import os
import re
import sys

def parse_all_sigs_file(root_path, src_path_component, data_sig_file_name, bat_alarm_sig_file_name):
    print('enter parse_all_sigs_file fun!\n')

    assert len(root_path) > 0 and len(data_sig_file_name) > 0 and len(bat_alarm_sig_file_name) > 0, 'param error!'

    data_sig_path = root_path + '\\' + src_path_component + '\\' + data_sig_file_name
    bat_alarm_sig_path = root_path + '\\' + src_path_component + '\\' + bat_alarm_sig_file_name

    all_sigs_f = open(data_sig_path, 'r')

    data_sig_list = []

    for line in all_sigs_f:
        line = line.strip()
        if len(line) > 0:
            data_sig_list.append(line)

    all_sigs_f.close()

    bat_alarm_sigs_f = open(bat_alarm_sig_path, 'r')

    bat_alarm_sig_list = []

    for line in bat_alarm_sigs_f:
        line = line.strip()
        if len(line) > 0:
            bat_alarm_sig_list.append(line)

    bat_alarm_sigs_f.close()

    print('parse all sigs file success!\n')

    return data_sig_list, bat_alarm_sig_list