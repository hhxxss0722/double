# -*- coding: utf-8 -*-
__author__ = 'yanshaowei'

'''dbc class module'''

class Dbc_class(object):
    # property
    file_path = ''
    # file_name = ''
    message_sum = 0
    message_list = []
    can_channel = 0

    # class method
    def __init__(self, file_path, message_sum, message_list, can_channel):
        self.file_path = file_path
        self.message_sum = message_sum
        self.message_list = list(message_list)
        self.can_channel = can_channel

    def __getattr__(self, item):
        L1 = self.file_path.split('\\')
        new_file_path = L1[-1]
        L2 = new_file_path.split('.')
        file_name = L2[0]

        if item == 'file_name':
            pass
        elif item == 'valid_file_name':
            if file_name.find('_') != -1:
                L3 = file_name.split('_')

                if L3[-1].isdigit():
                    L3.pop()
                    file_name = '_'.join(L3)
        else:
            file_name = None

        if item == 'data_sig_sum':
            sum = 0
            for msg in self.message_list:
                sum += msg.sig_sum

            return sum

        if item == 'alarm_sig_sum':
            sum = 0
            for msg in self.message_list:
                sum += (msg.alarm_sig_sum + msg.bat_alarm_sig_sum)

            return sum

        return file_name

    def speak(self):
        print('\n file path=%s\n message sum=[%s]\n can channel=[%s]' % (self.file_path, self.message_sum, self.can_channel))
        for message in self.message_list:
            message.speak()
