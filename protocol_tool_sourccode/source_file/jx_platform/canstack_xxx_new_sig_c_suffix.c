
can_sig_manager_t sig_manager  __at(SIG_MANAGER_ADD)= 
{
	ARRAY_SIZE(sig_infor_array),
	sig_infor_array
};


float canstack_read_sig_value(sig_type sig_type)
{
	if((uint8_t)sig_type >= sig_manager.sig_sum)
	{ return FLOAT_MAX_VALUE;}
		
	return sig_manager.sig_infor_array[sig_type].get_sig_value_fun(0);
}

float canstack_read_group_sig_value(sig_type sig_type, uint8_t index)
{
	if((uint8_t)sig_type >= sig_manager.sig_sum)
	{ return FLOAT_MAX_VALUE;}
		
	return sig_manager.sig_infor_array[sig_type].get_sig_value_fun((void*)&index);
}


#endif
