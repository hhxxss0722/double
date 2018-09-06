# !/usr/bin/env python3
# -*- coding: utf-8 -*-

'''message module'''

import operator

class Message(object):
    # class attribute
    name = 'Default_message_Name'
    ID = ''
    period = ''
    # sig_list = []
    # sig_sum = 0
    raw_id = ''
    dlc = 0
    all_sig_list = []
    all_sig_sum = 0
    _general_alarm_sig_list = []
    _general_alarm_sig_sum = 0

    _data_sig_list = []
    _data_sig_sum = 0

    _bat_alarm_sig_list = []
    _bat_alarm_sig_sum = 0

    # class method
    def __init__(self, name, raw_id, dlc, period=1000):
        self.name = name.lower()
        self.ID = str( hex(int(raw_id) & 0x1fffffff) ).upper().strip('L')
        self.raw_id = raw_id
        self.dlc = dlc
        self.period = str(period)

    def set_sig_list(self, new_list):
        # self.sig_list = new_list.copy()
        # self.sig_list = list(new_list)
        # self.sig_list.sort(key = lambda sig1: sig1.start_bit)
        # self.sig_list.sort(key = operator.attrgetter('start_bit'), reverse = False)
        temp_list = list(new_list)
        self.all_sig_list = sorted(temp_list, key=lambda Sig: Sig.start_bit, reverse = False)
        self.all_sig_sum = len(temp_list)


        temp_list_0 = list([x for x in self.all_sig_list if x.is_alarm_sig])

        self._bat_alarm_sig_list = list([x for x in temp_list_0 if x.is_bat_alarm_sig])
        self._bat_alarm_sig_sum = len(self._bat_alarm_sig_list)

        self._general_alarm_sig_list = list(set(temp_list_0) - set(self._bat_alarm_sig_list))
        self._general_alarm_sig_sum = len(self._general_alarm_sig_list)

        temp_list_1 = list(set(self.all_sig_list) - set(temp_list_0))
        self._data_sig_list = sorted(temp_list_1, key=lambda Sig: Sig.start_bit, reverse = False)
        self._data_sig_sum = len(self._data_sig_list)

    def __getattr__(self, item):
        if item == 'sig_list':
            return self._data_sig_list

        if item == 'sig_sum':
            return self._data_sig_sum

        if item == 'alarm_sig_list':
            return self._general_alarm_sig_list

        if item == 'alarm_sig_sum':
            return self._general_alarm_sig_sum + self._bat_alarm_sig_sum

        if item == 'bat_alarm_sig_list':
            return self._bat_alarm_sig_list

        if item == 'bat_alarm_sig_sum':
            return self._bat_alarm_sig_sum

    def get_ordering(self):
        return self.sig_list[0].ordering


    def speak(self):
        # print('ID = %d'% hex(self.ID))
        print('*************************************')
        print('-------message:-------')
        print('\n name:[%s]\n ID:[%s]\n len:[%s]\n period:[%s]\n data sig sum:[%s]\n alarm sig sum:[%s]\n'
              % (self.name, self.ID, self.dlc, self.period, self._data_sig_sum, self._general_alarm_sig_sum))
        print('\n-------data sig list:-------')
        for sig in self._data_sig_list:
            sig.speak()
        print('\n-------alarm sig list:-------')
        for sig in self._general_alarm_sig_list:
            sig.speak()
        for sig in self._bat_alarm_sig_list:
            sig.speak()