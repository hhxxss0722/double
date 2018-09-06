
rt_err_t can_config_ch0(rt_device_t dev)
{
    rt_uint32_t i = 0;
    flexcan_rxmb_set_t  set;
    flexcan_rxmb_filter_mask_set_t mask_set;
    
    /* init */
    for(i=0; i<canstack_chn0_size; i++)
    {
        rt_timer_init(canstack_message_array0[i].timer, 
                      canstack_message_array0[i].timer_name, 
                      canstack_message_array0[i].timeout_hook, 
                      RT_NULL, 
                      canstack_message_array0[i].outtime, 
                      RT_TIMER_FLAG_PERIODIC | RT_TIMER_FLAG_SOFT_TIMER);
    }

	/* set mailbox id and mask */
	for(i = 0; i < canstack_chn0_id_filter_sum; i++)
	{
        set.mb = i;
        set.id = canstack_chn0_id_filter[i*2];
        rt_device_control(dev, CAN_CMD_SETRXMB, &set);

		mask_set.mb = i;
		mask_set.mask = canstack_chn0_id_filter[i*2+1];
		rt_device_control(dev, CAN_CMD_SET_RX_FILTER_MASK, &mask_set);
	}
    
    /* start timer */
    for(i=0; i<canstack_chn0_size; i++)
    {
        rt_timer_start(canstack_message_array0[i].timer);
    }
    
    return RT_EOK;
}

rt_err_t can_parser_ch0(CAN_Message_Type * m)
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
