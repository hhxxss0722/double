# -*- coding: utf-8 -*-
'''create_msg_c_file module'''

# msg_c_output_path = output_pre_path + 'canstack_' + dbc_file_name.lower() +'_msg.c'
def create_msg_c_file(root_path, output_pre_path, dbc_list):
    if len(root_path) == 0 or len(dbc_list) == 0:
        raise TypeError('root path or dbc list is error!')

    for dbc in dbc_list:
        output_path = output_pre_path + 'canstack_' + dbc.file_name.lower() +'_msg.c'
        _create_specified_msg_c_file(root_path, output_path, dbc.message_list, dbc.valid_file_name, str(dbc.can_channel))

# create specified msg.c file
def _create_specified_msg_c_file(root_path, out_path, message_list, dbc_file_name, channel_str):
    if len(root_path) == 0 or len(message_list) == 0:
        raise TypeError('root path or message list is error!')
    # 文件“前缀”
    target_f_path = out_path

    try:
        tar_f = open(target_f_path, 'w')

        tar_f.write('\n')

    except:
        raise TypeError('operate msg.c file fail!')

    str1 = '#include \"canstack_sig.h\"\n\n'
    str1 += '#ifdef CANSTACK_' + dbc_file_name.upper() + '\n\n'

    str1 += '#define canstack_print_en               (0)\n'
    str1 += '#define printd                          if(canstack_print_en)rt_printf_can\n'

    tar_f.write(str1)

    str1 = '\n#ifdef CANSTACK_CAN' + channel_str + '\n//CAN' + channel_str
    tar_f.write(str1)

    tar_f.write('\n')

    for message in message_list:
        str2 = \
'''\
/* %(lowername)s:%(msg_id)s */
CANSTACK_DECLARE_MESSAGE(%(lowername)s);
#define CAN_%(uppername)s_NAME					"%(uppername)s"
#define CAN_%(uppername)s_ID					%(msg_id)s
#define CAN_%(uppername)s_CYCLE					%(msg_cycle)s\
'''
        temp_dic = {'lowername': message.name,
                    'msg_id': message.ID,
                    'uppername': message.name.upper(),
                    'msg_cycle': message.period,
                    }
        str1 = str2 % temp_dic
        str1 += '\n\n'

        tar_f.write(str1)

        # str1 = ''
        # upper_name = message.name.upper()
        #
        # # /* hybird_infor:0x18EF4AEF */
        # str1 += '/* ' + message.name + ':'+ message.ID + ' */' + '\n'
        #
        # # CANSTACK_DECLARE_MESSAGE(hybird_infor);
        # str1 += 'CANSTACK_DECLARE_MESSAGE(' + message.name + ');' +'\n'
        #
        # # #define CAN_HYBIRD_INFOR_NAME                   "HYBIRD_INFOR"
        # str1 += '#define CAN_'+ upper_name + '_NAME\t\t\t\t\t' + '\"' + upper_name + '\"' + '\n'
        #
        # # #define CAN_HYBIRD_INFOR_ID                     0x18EF4AEF
        # str1 += '#define CAN_'+ upper_name +'_ID\t\t\t\t\t' + message.ID + '\n'
        #
        # # #define CAN_HYBIRD_INFOR_CYCLE                  200
        # str1 += '#define CAN_'+ upper_name + '_CYCLE\t\t\t\t\t' + message.period + '\n'
        #
        # str1 += '\n'
        # tar_f.write(str1)


    str1 = 'canstack_msg_t canstack_message_array' + channel_str + '[] = \n' + '{\n'
    tar_f.write(str1)

    for message in message_list:
        str2 = \
'''	{(cuint8_t)%(uppername)s,	&%(lowername)s_timer,			CAN_%(uppername)s_NAME,			%(msg_cycle)s,		%(lowername)s_data_array},'''

        temp_dic = {'lowername': message.name,
                    'msg_cycle': str(int(message.period) * 2),
                    'uppername': message.name.upper()
                    }
        str1 = str2 % temp_dic
        str1 += '\n'
        tar_f.write(str1)

        # tar_f.write(str1)
        #
        # str1 = '\t{(cuint8_t)' + upper_name + ',\t\t\t' + '&' + lower_name + '_timer,\t\t\t' \
        #        + 'CAN_' + upper_name + '_NAME,\t\t\t' + message.period + ',\t\t\t' \
        #         + lower_name + '_data_array},\n'
        # tar_f.write(str1)

    tar_f.write('};')

    name_prefix = 'canstack_chn' + channel_str
    array_suffix = 'array' + channel_str

    str1 = '\nconst rt_uint8_t ' + name_prefix + '_size = sizeof(canstack_message_' + array_suffix + ')/sizeof(canstack_message_' + array_suffix + '[0]);'
    tar_f.write(str1)

    str1 = '\nconst rt_uint32_t ' + name_prefix + '_id_filter[] =\n'
    str1 += '{\n'
    tar_f.write(str1)

    str1 = ''
    for message in message_list:
        upper_name = message.name.upper()
        str1 += '\tCAN_' + upper_name + '_ID,\t\t\t0xFFFFFFFF,' + '/* ' + message.ID + ' */\n'

    str1 += '};'

    tar_f.write(str1)

    str1  = '\nconst rt_uint8_t ' + name_prefix + '_id_filter_sum = (sizeof(' + name_prefix + '_id_filter)/sizeof(' + name_prefix + '_id_filter[0]) ) / 2;'
    tar_f.write(str1)

    str1 = '\ncanstack_msgout_t canstack_timeout_' + array_suffix + '[' + name_prefix + '_size] =' \
            + '\n{\n'
    tar_f.write(str1)

    temp_list = ['\tRT_TRUE,'] * len(message_list)
    str1 = '\n'.join(temp_list)
    str1 += '\n};\n\n'
    tar_f.write(str1)

    str2 = \
'''\
/* receive fun*/
static void msg_recv_fun_%(chn)s(cuint8_t *p_u8Data, cuint8_t index)
{
	rt_timer_stop( canstack_message_array%(chn)s[index].timer);

	rt_memcpy(
			canstack_message_array%(chn)s[index].p_u8Data,
			p_u8Data,
			DATA_ARRAY_SIZE);

	rt_timer_control(
					canstack_message_array%(chn)s[index].timer,
					RT_TIMER_CTRL_SET_TIME,
					(void*)&(canstack_message_array%(chn)s[index].outtime));
	rt_timer_start(canstack_message_array%(chn)s[index].timer);

	canstack_timeout_array%(chn)s[index].outind = RT_FALSE;
}
/* public timeout fun */
static void public_timeout_fun_%(chn)s(void *parameter)
{
	cuint8_t index = *(cuint8_t*)parameter;
	rt_timer_stop( canstack_message_array%(chn)s[index].timer);
	canstack_timeout_array%(chn)s[index].outind = RT_TRUE;
}\
'''
    dic = {'chn': channel_str}
    str1 = str2 % dic
    str1 += '\n'

    tar_f.write(str1)

    str2 = \
'''\
rt_err_t can_config_ch%(chn)s(rt_device_t dev)
{
    rt_uint32_t i = 0;
    flexcan_rxmb_set_t  set;
    flexcan_rxmb_filter_mask_set_t mask_set;

    /* init */
    for(i=0; i<canstack_chn%(chn)s_size; i++)
    {
        rt_timer_init(canstack_message_array%(chn)s[i].timer,
                      canstack_message_array%(chn)s[i].timer_name,
                      public_timeout_fun_%(chn)s,
                      &canstack_message_array%(chn)s[i].index,
                      canstack_message_array%(chn)s[i].outtime,
                      RT_TIMER_FLAG_PERIODIC | RT_TIMER_FLAG_SOFT_TIMER);
    }
    
	TBOX_ASSERT(canstack_chn%(chn)s_id_filter_sum <= FLEXCAN_MB_NO);    

	/* set mailbox id and mask */
	for(i = 0; i < canstack_chn%(chn)s_id_filter_sum; i++)
	{
        set.mb = i;
        set.id = canstack_chn%(chn)s_id_filter[i*2];
        rt_device_control(dev, CAN_CMD_SETRXMB, &set);

		mask_set.mb = i;
		mask_set.mask = canstack_chn%(chn)s_id_filter[i*2+1];
		rt_device_control(dev, CAN_CMD_SET_RX_FILTER_MASK, &mask_set);
	}

    /* start timer */
    for(i=0; i<canstack_chn%(chn)s_size; i++)
    {
        rt_timer_start(canstack_message_array%(chn)s[i].timer);
    }

    return RT_EOK;
}\
'''
    str1 = str2 % dic
    str1 += '\n\n'

    tar_f.write(str1)

    str1 = '/******************deal error status*******************/\n'
    str1 += 'extern void deal_default_msg_error_status(cuint8_t *p_u8Data);\n'

    for msg in message_list:
        if msg.alarm_sig_sum > 0:
            str1 += 'extern void deal_' + msg.name + '_error_status(cuint8_t *p_u8Data);\n'

    str1 += '/******************deal error status*******************/\n\n'
    tar_f.write(str1)

    str1 = 'rt_err_t can_parser_ch' + channel_str + '(CAN_Message_Type * m)'
    tar_f.write(str1)

    str1 = \
r'''
{
    rt_uint32_t i;

    /* display */
    printd("id=0x%08X, dlc=%d, data=", m->id, m->dlc);
    for(i=0; i<m->dlc; i++)
    {
        printd("%02X ", m->data[i]);
    }
    printd("\r\n");

    if(m->dlc != 8) /* project specific */
    {
        return -RT_ERROR;
    }

    if(m->data == NULL)
    {
        return -RT_ERROR;
    }
'''
    tar_f.write(str1)

    str1 = '\n\t/* parse */'
    str1 += '\n\tswitch(m->id)\n\t'
    str1 += '{\n'

    tar_f.write(str1)

    for message in  message_list:
        str2 = \
'''\
		case CAN_%(uppername)s_ID:
			msg_recv_fun_%(chn)s(m->data, %(uppername)s);
			deal_%(fun_name)s_error_status(m->data);
			break;\
'''
        dic2 = {'uppername': message.name.upper(),
                'fun_name':message.name,
                'chn': channel_str}

        if message.alarm_sig_sum == 0:
            dic2['fun_name'] = 'default_msg'

        str1 = str2 % dic2
        str1 += '\n'

        tar_f.write(str1)

    str1 = '\t\tdefault:\n\t\t\t' + 'break;\n\t'
    str1 += '}\n\n'
    str1 += '\treturn RT_EOK;\n'

    str1 += '}'

    str1 += '\n#endif /* CANSTACK_CAN' + channel_str + ' */' + '\n\n#endif\n'

    tar_f.write(str1)

    tar_f.close()

    print('create msg.c file success!')

