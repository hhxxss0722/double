# -*- coding: utf-8 -*-

'''formula module'''

class Formula(object):
    # class attribute
    sig_name = ''
    offset = 0
    scale = 1
    length = 0
    min_val = 0
    max_val = 0
    invalid_val = 0
    unit = ''

    # class method
    # Formula(return_data_t, name, zh_name, param_str, sig_name, offset_str, scale_str, min_val_str, max_val_str, invalid_val_str, unit_str)
    # (self, sig_name, offset, scale, length, min_val, max_val, invalid_val, unit) new
    def __init__(self, sig_name, offset, scale, length, min_val, max_val, invalid_val, unit):
        self.sig_name = sig_name.lower()

        # if len(offset) == 0:
        #     self.offset = 0.0
        # else:
        self.offset = float(offset)
        # scale can not be zero
        # if len(scale) == 0:
        #     self.scale = 1
        # else:
        self.scale = float(scale)

        self.length = int(length)

        self.min_val = int(min_val)
        self.max_val = int(max_val)

        self.invalid_val = int(invalid_val)

        # self.unit = unit.upper()
        self.unit = unit

    def get_max_limit_value(self):
        if self.length == 8:
            val = '0xFF'
        elif self.length == 16:
            val = '0XFFFF'
        elif self.length == 32:
            val = '0XFFFFFFFF'
        else:
            val = None

        return val

    def get_byte_num(self):
        # 65535 ---> 0xffff ---->ffff
        hex_data_str = str(hex(self.invalid_val))[2:]

        return len(hex_data_str) / 2


    def speak(self):
        print('\n sig_name = [%s]\n offset = [%s]\n  scale = [%s]\n length = [%s]\n min_val = [%s]\n max_val = [%s]\n invalid_val= [%s]\n unit = [%s]\n' % \
              (self.sig_name, self.offset, self.scale, self.length, self.min_val, self.max_val, self.invalid_val, self.unit))