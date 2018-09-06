
#include "canstack_sig.h"

#ifdef CANSTACK_JZ_V10

#define canstack_print_en               (0)
#define printd                          if(canstack_print_en)rt_printf_can

#ifdef CANSTACK_CAN0
//CAN0
/* vehicle_controller_data_1:0XC03A1A7 */
CANSTACK_DECLARE_MESSAGE(vehicle_controller_data_1);
#define CAN_VEHICLE_CONTROLLER_DATA_1_NAME					"VEHICLE_CONTROLLER_DATA_1"
#define CAN_VEHICLE_CONTROLLER_DATA_1_ID					0XC03A1A7
#define CAN_VEHICLE_CONTROLLER_DATA_1_CYCLE					100

/* vehicle_controller_data_2:0XC04A1A7 */
CANSTACK_DECLARE_MESSAGE(vehicle_controller_data_2);
#define CAN_VEHICLE_CONTROLLER_DATA_2_NAME					"VEHICLE_CONTROLLER_DATA_2"
#define CAN_VEHICLE_CONTROLLER_DATA_2_ID					0XC04A1A7
#define CAN_VEHICLE_CONTROLLER_DATA_2_CYCLE					100

/* vehicle_controller_data_3:0XC06A1A7 */
CANSTACK_DECLARE_MESSAGE(vehicle_controller_data_3);
#define CAN_VEHICLE_CONTROLLER_DATA_3_NAME					"VEHICLE_CONTROLLER_DATA_3"
#define CAN_VEHICLE_CONTROLLER_DATA_3_ID					0XC06A1A7
#define CAN_VEHICLE_CONTROLLER_DATA_3_CYCLE					100

/* vehicle_controller_data_4:0XC0AA1A7 */
CANSTACK_DECLARE_MESSAGE(vehicle_controller_data_4);
#define CAN_VEHICLE_CONTROLLER_DATA_4_NAME					"VEHICLE_CONTROLLER_DATA_4"
#define CAN_VEHICLE_CONTROLLER_DATA_4_ID					0XC0AA1A7
#define CAN_VEHICLE_CONTROLLER_DATA_4_CYCLE					5000

/* vehicle_controller_data_5:0XC0BA1A7 */
CANSTACK_DECLARE_MESSAGE(vehicle_controller_data_5);
#define CAN_VEHICLE_CONTROLLER_DATA_5_NAME					"VEHICLE_CONTROLLER_DATA_5"
#define CAN_VEHICLE_CONTROLLER_DATA_5_ID					0XC0BA1A7
#define CAN_VEHICLE_CONTROLLER_DATA_5_CYCLE					100

/* insulated_test_data_1:0X1819A1A4 */
CANSTACK_DECLARE_MESSAGE(insulated_test_data_1);
#define CAN_INSULATED_TEST_DATA_1_NAME					"INSULATED_TEST_DATA_1"
#define CAN_INSULATED_TEST_DATA_1_ID					0X1819A1A4
#define CAN_INSULATED_TEST_DATA_1_CYCLE					100

/* dc_dc_data_1:0XC08A79A */
CANSTACK_DECLARE_MESSAGE(dc_dc_data_1);
#define CAN_DC_DC_DATA_1_NAME					"DC_DC_DATA_1"
#define CAN_DC_DC_DATA_1_ID					0XC08A79A
#define CAN_DC_DC_DATA_1_CYCLE					100

/* dashboard_data_1:0XC19A7A1 */
CANSTACK_DECLARE_MESSAGE(dashboard_data_1);
#define CAN_DASHBOARD_DATA_1_NAME					"DASHBOARD_DATA_1"
#define CAN_DASHBOARD_DATA_1_ID					0XC19A7A1
#define CAN_DASHBOARD_DATA_1_CYCLE					100

/* dashboard_data_2:0XC1AA7A1 */
CANSTACK_DECLARE_MESSAGE(dashboard_data_2);
#define CAN_DASHBOARD_DATA_2_NAME					"DASHBOARD_DATA_2"
#define CAN_DASHBOARD_DATA_2_ID					0XC1AA7A1
#define CAN_DASHBOARD_DATA_2_CYCLE					1000

/* bat_manage_system_1:0X1818D0F3 */
CANSTACK_DECLARE_MESSAGE(bat_manage_system_1);
#define CAN_BAT_MANAGE_SYSTEM_1_NAME					"BAT_MANAGE_SYSTEM_1"
#define CAN_BAT_MANAGE_SYSTEM_1_ID					0X1818D0F3
#define CAN_BAT_MANAGE_SYSTEM_1_CYCLE					100

/* bat_manage_system_2:0X181AD0F3 */
CANSTACK_DECLARE_MESSAGE(bat_manage_system_2);
#define CAN_BAT_MANAGE_SYSTEM_2_NAME					"BAT_MANAGE_SYSTEM_2"
#define CAN_BAT_MANAGE_SYSTEM_2_ID					0X181AD0F3
#define CAN_BAT_MANAGE_SYSTEM_2_CYCLE					100

/* bat_manage_system_3:0X181BD0F3 */
CANSTACK_DECLARE_MESSAGE(bat_manage_system_3);
#define CAN_BAT_MANAGE_SYSTEM_3_NAME					"BAT_MANAGE_SYSTEM_3"
#define CAN_BAT_MANAGE_SYSTEM_3_ID					0X181BD0F3
#define CAN_BAT_MANAGE_SYSTEM_3_CYCLE					100

/* bat_manage_system_4:0X181CD0F3 */
CANSTACK_DECLARE_MESSAGE(bat_manage_system_4);
#define CAN_BAT_MANAGE_SYSTEM_4_NAME					"BAT_MANAGE_SYSTEM_4"
#define CAN_BAT_MANAGE_SYSTEM_4_ID					0X181CD0F3
#define CAN_BAT_MANAGE_SYSTEM_4_CYCLE					100

/* bat_manage_system_5:0X181DD0F3 */
CANSTACK_DECLARE_MESSAGE(bat_manage_system_5);
#define CAN_BAT_MANAGE_SYSTEM_5_NAME					"BAT_MANAGE_SYSTEM_5"
#define CAN_BAT_MANAGE_SYSTEM_5_ID					0X181DD0F3
#define CAN_BAT_MANAGE_SYSTEM_5_CYCLE					100

/* bat_manage_system_6:0X181ED0F3 */
CANSTACK_DECLARE_MESSAGE(bat_manage_system_6);
#define CAN_BAT_MANAGE_SYSTEM_6_NAME					"BAT_MANAGE_SYSTEM_6"
#define CAN_BAT_MANAGE_SYSTEM_6_ID					0X181ED0F3
#define CAN_BAT_MANAGE_SYSTEM_6_CYCLE					100

canstack_msg_t canstack_message_array0[] = 
{
	{(cuint8_t)VEHICLE_CONTROLLER_DATA_1,	&vehicle_controller_data_1_timer,			CAN_VEHICLE_CONTROLLER_DATA_1_NAME,			200,		vehicle_controller_data_1_data_array},
	{(cuint8_t)VEHICLE_CONTROLLER_DATA_2,	&vehicle_controller_data_2_timer,			CAN_VEHICLE_CONTROLLER_DATA_2_NAME,			200,		vehicle_controller_data_2_data_array},
	{(cuint8_t)VEHICLE_CONTROLLER_DATA_3,	&vehicle_controller_data_3_timer,			CAN_VEHICLE_CONTROLLER_DATA_3_NAME,			200,		vehicle_controller_data_3_data_array},
	{(cuint8_t)VEHICLE_CONTROLLER_DATA_4,	&vehicle_controller_data_4_timer,			CAN_VEHICLE_CONTROLLER_DATA_4_NAME,			10000,		vehicle_controller_data_4_data_array},
	{(cuint8_t)VEHICLE_CONTROLLER_DATA_5,	&vehicle_controller_data_5_timer,			CAN_VEHICLE_CONTROLLER_DATA_5_NAME,			200,		vehicle_controller_data_5_data_array},
	{(cuint8_t)INSULATED_TEST_DATA_1,	&insulated_test_data_1_timer,			CAN_INSULATED_TEST_DATA_1_NAME,			200,		insulated_test_data_1_data_array},
	{(cuint8_t)DC_DC_DATA_1,	&dc_dc_data_1_timer,			CAN_DC_DC_DATA_1_NAME,			200,		dc_dc_data_1_data_array},
	{(cuint8_t)DASHBOARD_DATA_1,	&dashboard_data_1_timer,			CAN_DASHBOARD_DATA_1_NAME,			200,		dashboard_data_1_data_array},
	{(cuint8_t)DASHBOARD_DATA_2,	&dashboard_data_2_timer,			CAN_DASHBOARD_DATA_2_NAME,			2000,		dashboard_data_2_data_array},
	{(cuint8_t)BAT_MANAGE_SYSTEM_1,	&bat_manage_system_1_timer,			CAN_BAT_MANAGE_SYSTEM_1_NAME,			200,		bat_manage_system_1_data_array},
	{(cuint8_t)BAT_MANAGE_SYSTEM_2,	&bat_manage_system_2_timer,			CAN_BAT_MANAGE_SYSTEM_2_NAME,			200,		bat_manage_system_2_data_array},
	{(cuint8_t)BAT_MANAGE_SYSTEM_3,	&bat_manage_system_3_timer,			CAN_BAT_MANAGE_SYSTEM_3_NAME,			200,		bat_manage_system_3_data_array},
	{(cuint8_t)BAT_MANAGE_SYSTEM_4,	&bat_manage_system_4_timer,			CAN_BAT_MANAGE_SYSTEM_4_NAME,			200,		bat_manage_system_4_data_array},
	{(cuint8_t)BAT_MANAGE_SYSTEM_5,	&bat_manage_system_5_timer,			CAN_BAT_MANAGE_SYSTEM_5_NAME,			200,		bat_manage_system_5_data_array},
	{(cuint8_t)BAT_MANAGE_SYSTEM_6,	&bat_manage_system_6_timer,			CAN_BAT_MANAGE_SYSTEM_6_NAME,			200,		bat_manage_system_6_data_array},
};
const rt_uint8_t canstack_chn0_size = sizeof(canstack_message_array0)/sizeof(canstack_message_array0[0]);
const rt_uint32_t canstack_chn0_id_filter[] =
{
	CAN_VEHICLE_CONTROLLER_DATA_1_ID,			0xFFFFFFFF,/* 0XC03A1A7 */
	CAN_VEHICLE_CONTROLLER_DATA_2_ID,			0xFFFFFFFF,/* 0XC04A1A7 */
	CAN_VEHICLE_CONTROLLER_DATA_3_ID,			0xFFFFFFFF,/* 0XC06A1A7 */
	CAN_VEHICLE_CONTROLLER_DATA_4_ID,			0xFFFFFFFF,/* 0XC0AA1A7 */
	CAN_VEHICLE_CONTROLLER_DATA_5_ID,			0xFFFFFFFF,/* 0XC0BA1A7 */
	CAN_INSULATED_TEST_DATA_1_ID,			0xFFFFFFFF,/* 0X1819A1A4 */
	CAN_DC_DC_DATA_1_ID,			0xFFFFFFFF,/* 0XC08A79A */
	CAN_DASHBOARD_DATA_1_ID,			0xFFFFFFFF,/* 0XC19A7A1 */
	CAN_DASHBOARD_DATA_2_ID,			0xFFFFFFFF,/* 0XC1AA7A1 */
	CAN_BAT_MANAGE_SYSTEM_1_ID,			0xFFFFFFFF,/* 0X1818D0F3 */
	CAN_BAT_MANAGE_SYSTEM_2_ID,			0xFFFFFFFF,/* 0X181AD0F3 */
	CAN_BAT_MANAGE_SYSTEM_3_ID,			0xFFFFFFFF,/* 0X181BD0F3 */
	CAN_BAT_MANAGE_SYSTEM_4_ID,			0xFFFFFFFF,/* 0X181CD0F3 */
	CAN_BAT_MANAGE_SYSTEM_5_ID,			0xFFFFFFFF,/* 0X181DD0F3 */
	CAN_BAT_MANAGE_SYSTEM_6_ID,			0xFFFFFFFF,/* 0X181ED0F3 */
};
const rt_uint8_t canstack_chn0_id_filter_sum = (sizeof(canstack_chn0_id_filter)/sizeof(canstack_chn0_id_filter[0]) ) / 2;
canstack_msgout_t canstack_timeout_array0[canstack_chn0_size] =
{
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
	RT_TRUE,
};

/* receive fun*/
static void msg_recv_fun_0(cuint8_t *p_u8Data, cuint8_t index)
{
	rt_timer_stop( canstack_message_array0[index].timer);

	rt_memcpy(
			canstack_message_array0[index].p_u8Data,
			p_u8Data,
			DATA_ARRAY_SIZE);

	rt_timer_control(
					canstack_message_array0[index].timer,
					RT_TIMER_CTRL_SET_TIME,
					(void*)&(canstack_message_array0[index].outtime));
	rt_timer_start(canstack_message_array0[index].timer);

	canstack_timeout_array0[index].outind = RT_FALSE;
}
/* public timeout fun */
static void public_timeout_fun_0(void *parameter)
{
	cuint8_t index = *(cuint8_t*)parameter;
	rt_timer_stop( canstack_message_array0[index].timer);
	canstack_timeout_array0[index].outind = RT_TRUE;
}
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
                      public_timeout_fun_0,
                      &canstack_message_array0[i].index,
                      canstack_message_array0[i].outtime,
                      RT_TIMER_FLAG_PERIODIC | RT_TIMER_FLAG_SOFT_TIMER);
    }
    
	TBOX_ASSERT(canstack_chn0_id_filter_sum <= FLEXCAN_MB_NO);    

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

/******************deal error status*******************/
extern void deal_default_msg_error_status(cuint8_t *p_u8Data);
extern void deal_bat_manage_system_1_error_status(cuint8_t *p_u8Data);
extern void deal_bat_manage_system_3_error_status(cuint8_t *p_u8Data);
/******************deal error status*******************/

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

    if(m->data == NULL)
    {
        return -RT_ERROR;
    }

	/* parse */
	switch(m->id)
	{
		case CAN_VEHICLE_CONTROLLER_DATA_1_ID:
			msg_recv_fun_0(m->data, VEHICLE_CONTROLLER_DATA_1);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_VEHICLE_CONTROLLER_DATA_2_ID:
			msg_recv_fun_0(m->data, VEHICLE_CONTROLLER_DATA_2);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_VEHICLE_CONTROLLER_DATA_3_ID:
			msg_recv_fun_0(m->data, VEHICLE_CONTROLLER_DATA_3);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_VEHICLE_CONTROLLER_DATA_4_ID:
			msg_recv_fun_0(m->data, VEHICLE_CONTROLLER_DATA_4);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_VEHICLE_CONTROLLER_DATA_5_ID:
			msg_recv_fun_0(m->data, VEHICLE_CONTROLLER_DATA_5);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_INSULATED_TEST_DATA_1_ID:
			msg_recv_fun_0(m->data, INSULATED_TEST_DATA_1);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_DC_DC_DATA_1_ID:
			msg_recv_fun_0(m->data, DC_DC_DATA_1);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_DASHBOARD_DATA_1_ID:
			msg_recv_fun_0(m->data, DASHBOARD_DATA_1);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_DASHBOARD_DATA_2_ID:
			msg_recv_fun_0(m->data, DASHBOARD_DATA_2);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_BAT_MANAGE_SYSTEM_1_ID:
			msg_recv_fun_0(m->data, BAT_MANAGE_SYSTEM_1);
			deal_bat_manage_system_1_error_status(m->data);
			break;
		case CAN_BAT_MANAGE_SYSTEM_2_ID:
			msg_recv_fun_0(m->data, BAT_MANAGE_SYSTEM_2);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_BAT_MANAGE_SYSTEM_3_ID:
			msg_recv_fun_0(m->data, BAT_MANAGE_SYSTEM_3);
			deal_bat_manage_system_3_error_status(m->data);
			break;
		case CAN_BAT_MANAGE_SYSTEM_4_ID:
			msg_recv_fun_0(m->data, BAT_MANAGE_SYSTEM_4);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_BAT_MANAGE_SYSTEM_5_ID:
			msg_recv_fun_0(m->data, BAT_MANAGE_SYSTEM_5);
			deal_default_msg_error_status(m->data);
			break;
		case CAN_BAT_MANAGE_SYSTEM_6_ID:
			msg_recv_fun_0(m->data, BAT_MANAGE_SYSTEM_6);
			deal_default_msg_error_status(m->data);
			break;
		default:
			break;
	}

	return RT_EOK;
}
#endif /* CANSTACK_CAN0 */

#endif
