# -*- coding: utf-8 -*-
'''create_sig_h_file module'''

# def create_sig_h_file(root_path, out_path, message_list, dbc_file_name):
def create_sig_h_file(root_path, sig_h_output_path, dbc_list, platform_mode):
    if len(root_path) == 0 or len(dbc_list) == 0:
        raise TypeError('root path or dbc list is None!')

    target_sig_h_f_path = sig_h_output_path

    dbc_obj = dbc_list[0]
    valid_file_name = dbc_obj.valid_file_name

    try:
        tar_f = open(target_sig_h_f_path, 'w')

    except:
        raise TypeError('operate sig.h file fail!')

    str1 = '#ifndef CAN_STACK_' + valid_file_name.upper() + '_SIG_H\n'
    str1 += '#define CAN_STACK_' + valid_file_name.upper() + '_SIG_H\n\n'
    str1 += '#include \"canstack_sig.h\"\n\n'
    str1 += '#ifdef CANSTACK_' + valid_file_name.upper() + '\n\n'

    tar_f.write(str1)

    str2 = \
'''\
#if 0
#ifdef CANSTACK_%(uppername)s
	#include "canstack_%(lowername)s_sig.h"
	#include "canstack_%(lowername)s_msg.h"
	%(platform_macro)s
#endif
#endif\
'''
    dic1 = {'uppername': valid_file_name.upper(),
            'lowername': valid_file_name,
            'platform_macro': ''}

    if platform_mode == 'gb_platform':
		pass
        # dic1['platform_macro'] = '#define GB_PLATFORM_SIG'
    elif platform_mode == 'jx_platform':
        pass
        # dic1['platform_macro'] = '#define JX_PLATFORM_SIG'
    else:
        pass

    str1 = str2 % dic1

    str1 += '\n\n'

    tar_f.write(str1)

    str1 = '\n' + '#endif' + '\n' + '\n' + '#endif\n'

    tar_f.write(str1)

    tar_f.close()

    print('create sig.h file success!')
