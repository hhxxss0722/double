
sig_manager_t sig_manager = 
{
	sizeof(sig_infor_array) / sizeof(sig_infor_array[0]),
	sig_infor_array
};

float canstack_read_sig_value(sig_type sig_type)
{
	RT_ASSERT((uint8_t)sig_type < sig_manager.sig_sum);
	
	if((uint8_t)sig_type >= sig_manager.sig_sum)
	{ return FLOAT_MAX_VALUE;}
		
	return sig_manager.sig_infor_array[sig_type].get_sig_value_fun(0);
}

float canstack_read_group_sig_value(sig_type sig_type, rt_uint8_t index)
{
	RT_ASSERT((uint8_t)sig_type < sig_manager.sig_sum);
	
	if((uint8_t)sig_type >= sig_manager.sig_sum)
	{ return FLOAT_MAX_VALUE;}
		
	return sig_manager.sig_infor_array[sig_type].get_sig_value_fun((void*)&index);
}

static uint8_t arg_arry[2] = {0, 0};

float canstack_read_multi_group_sig(sig_type sig_type, rt_uint8_t group_index, rt_uint8_t index)
{
	RT_ASSERT((uint8_t)sig_type < sig_manager.sig_sum);

	if((uint8_t)sig_type >= sig_manager.sig_sum)
	{ return FLOAT_MAX_VALUE;}

	arg_arry[0] = group_index;
	arg_arry[1] = index;

	return sig_manager.sig_infor_array[sig_type].get_sig_value_fun((void*)&arg_arry);
}

sig_invalid_value_type get_sig_invalid_value_type(sig_type sig_type)
{
	return sig_manager.sig_infor_array[sig_type].invalid_value_type;
}

void get_sig_invalid_value(sig_type sig_type, void* invalid_value)
{
	sig_invalid_value_type invalid_type = sig_manager.sig_infor_array[sig_type].invalid_value_type;
	
	switch(invalid_type)
	{
		case INVALID_UINT8:
			*(uint8_t *)invalid_value = 0xff;
		break;
		case INVALID_UINT16:
			*(uint16_t *)invalid_value = 0xffff;
		break;	
		case INVALID_UINT32:
			*(uint32_t *)invalid_value = 0xffffffff;
		break;
		case INVALID_OTHER_1:
			*(uint8_t *)invalid_value = 0xff;
		break;	
		case INVALID_OTHER_2:
			*(uint16_t *)invalid_value = 0xffff;
		break;		
	}
}

