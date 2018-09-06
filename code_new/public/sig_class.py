# -*- coding: utf-8 -*-

"""sig module"""

# ordering=true---> L-M-H
# ordering=false---> H-M-L
class Sig(object):
    # class attribute
    name = 'Default_sig_Name'
    zh_name = ''
    suffix = ''
    start_bit = 0
    length_bit = 0
    ordering = False
    isSigned = False
    __lengthByte = 0
    scale = 0
    offset = 0
    min_val = 0
    max_val = 0
    unit = ''
    parent_message = None
    formula = None
    is_alarm_sig = False
    __alarm_sig_prefix = 'alarm'
    __state_dict = {}
    __display_dict = {}
    is_state_sig = False
    __is_bat_alarm_sig = False
    __alarm_level_list = {'level_0', 'level_1', 'level_2', 'level_3'}
    general_alarm_dtc_str = 'dtc'
    __invalid_alarm_level_value_str = '0xAA'
    __state_segment_str = '##'

    # class method
    def __init__(self, name, zh_name, suffix, start_bit, length_bit, ordering, isSigned, scale, offset, min_val, max_val, unit, message, formula):
        self.name = name.lower()
        self.zh_name = zh_name
        self.suffix = suffix
        self.start_bit = start_bit
        self.length_bit = length_bit
        self.ordering = ordering
        self.isSigned = isSigned
        self.scale = scale
        self.offset = offset
        self.min_val = min_val
        self.max_val = max_val
        # self.unit = unit.upper()
        if len(unit) > 0:
            self.unit = unit
        else:
            self.unit = unit

        self.parent_message = message
        self.formula = formula
        
        if not ordering and start_bit >= 7:
            self.start_bit -= 7

        if name.startswith(self.__alarm_sig_prefix):
            self.is_alarm_sig = True
        else:
            self.is_alarm_sig = False

    # get sig suffix num. like: get 'bat_cell_temp_12' suffix num 12, get 'bat_cell_temp' suffix num -1.
    # this attribute be used for special sort fun.
    def __getattr__(self, item):
        if item == 'suffix_num':
            if self.name.find('_') == -1:
                return -1
            elif not (self.name.split('_')[-1]).isdigit():
                return -1
            else:
                return int(self.name.split('_')[-1])

        if item == 'is_bat_alarm_sig':
            return self.__is_bat_alarm_sig

    def get_length_byte(self):
        prefix_zero = self.start_bit % 8
        suffix_zero = 8 - ((self.start_bit + self.length_bit - 1) % 8) - 1

        byte_sum = (suffix_zero + self.length_bit + prefix_zero) / 8

        return byte_sum

    def get_data_type(self):
        if self.length_bit <= 8:
            data_type = 'uint8_t'
        elif (self.length_bit > 8) and (self.length_bit <= 16):
            data_type = 'uint16_t'
        elif (self.length_bit > 16) and (self.length_bit <= 32):
            data_type = 'uint32_t'
        else:
            data_type = 'uint64_t'

        return data_type

    def get_max_limit_value(self):
        if self.length_bit <= 8:
            val = '0xFF'
        elif (self.length_bit > 8) and (self.length_bit <= 16):
            val = '0XFFFF'
        elif (self.length_bit > 16) and (self.length_bit <= 32):
            val = '0XFFFFFFFF'
        else:
            val = '0XFFFFFFFFFFFFFFFF'

        return val

    def set_state_dict(self, new_dict):
        temp_dict = {}
        disply_dict = {}
        key_list = new_dict.keys()

        for key in key_list:
            result = self.__get_state_valid_data(new_dict[key])
            if result is None:
                pass
            else:
                temp_dict[key.lower()] = result.lower()		#{'charging ##0x02':'0x02'}

            result = self.__get_state_display_str(new_dict[key])
            if result is None:
                pass
            else:
                disply_dict[key.lower()] = result.lower()	#{'charging ##0x02':'charging'}

        self.__state_dict = temp_dict
        self.__display_dict = disply_dict

        self.is_state_sig = True

    # Charging ##0x02   ---> 0x02
    # Charging ##       ---> None
    # Charging 0x02     ---> None
    # dtc/DTC/dTc...    ---> dtc
    def __get_state_valid_data(self, string):

        if string.lower() == self.general_alarm_dtc_str:
            return self.general_alarm_dtc_str

        result_list = string.split(self.__state_segment_str)	
        if len(result_list) != 2:		
            return None

        if len(result_list[1]) == 0:	
            return None
        elif result_list[1].isspace():	
            return None
        else:
            return result_list[1]

        return None

    # Charging ##0x02   ---> Charging
    # Charging ##       ---> None
    # Charging 0x02     ---> None
    def __get_state_display_str(self, string):

        result_list = string.split(self.__state_segment_str)
        if len(result_list) != 2:
            return None

        if len(result_list[0]) == 0:
            return None
        elif result_list[0].isspace():
            return None
        else:
            return result_list[0]

        return None

    def get_state_dict(self):
        return self.__state_dict

    def get_display_dict(self):
        return self.__display_dict

    def set_bat_alarm_flag(self, flag):
        self.__is_bat_alarm_sig = flag

    def get_bat_alarm_flag(self):
        return self.__is_bat_alarm_sig

    # transit part of formula unit
    def get_unit_transition(self):

        formula_unit = self.formula.unit.upper()
        sig_unit = self.unit.upper()

        if (formula_unit == 'MA') and (sig_unit == 'A'):
            return '1000'

        if (formula_unit == 'A') and (sig_unit == 'MA'):
            return '0.001'

        if (formula_unit == 'MV') and (sig_unit == 'V'):
            return '1000'

        if (formula_unit == 'V') and (sig_unit == 'MV'):
            return '0.001'

        return ''

    def get_alarm_level_dic(self):
        if not self.is_alarm_sig:
            return None

        if len(self.__state_dict) == 0:
            return None

        level_dic = {}

        temp_state_dict = {v: k for k, v in self.__state_dict.items()}

        key_list = temp_state_dict.keys()
        # __alarm_level_list = {'level_1', 'level_2', 'level_3'}
        for level in self.__alarm_level_list:
            if level in key_list:
                level_dic[level] = temp_state_dict[level]
            else:
                # set invalid level value
                level_dic[level] = self.__invalid_alarm_level_value_str

        # if sig is general alarm sig
        if not self.__is_bat_alarm_sig:
            # general alarm sig must have 'dtc' item
            if self.general_alarm_dtc_str not in key_list:
                return None
            # set level_dic 'dtc' item
            level_dic[self.general_alarm_dtc_str] = temp_state_dict[self.general_alarm_dtc_str]

        return level_dic

    def speak(self):
        print('\n name:[%s]\n zh_name:[%s]\n startBit:[%s]\n lengthBit:[%s]\n order:[%s]\n signed:[%s]\n scale:[%s]\n offset:[%s]\n' \
              ' min:[%s]\n max:[%s]\n unit:[%r]\n parent message:[%s]\n byte length:[%s]\n'
              % (self.name, self.zh_name, self.start_bit, self.length_bit, self.ordering, self.isSigned, self.scale, self.offset,
                self.min_val, self.max_val, self.unit, self.parent_message.name, self.get_length_byte() ) )
