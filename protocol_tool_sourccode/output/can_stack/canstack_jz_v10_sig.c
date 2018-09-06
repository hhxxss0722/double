#include "canstack_sig.h"

#ifdef CANSTACK_JZ_V10

/* for print */
#define printd  if(0)rt_printf_can
/**************************CAN_0**************************/
/* vehicle_controller_data_1:0XC03A1A7 */
#define CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY			canstack_message_array0[VEHICLE_CONTROLLER_DATA_1].p_u8Data
#define CAN_VEHICLE_CONTROLLER_DATA_1_OUTIND			canstack_timeout_array0[VEHICLE_CONTROLLER_DATA_1].outind

/* vehicle_controller_data_2:0XC04A1A7 */
#define CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY			canstack_message_array0[VEHICLE_CONTROLLER_DATA_2].p_u8Data
#define CAN_VEHICLE_CONTROLLER_DATA_2_OUTIND			canstack_timeout_array0[VEHICLE_CONTROLLER_DATA_2].outind

/* vehicle_controller_data_3:0XC06A1A7 */
#define CAN_VEHICLE_CONTROLLER_DATA_3_DATA_ARRAY			canstack_message_array0[VEHICLE_CONTROLLER_DATA_3].p_u8Data
#define CAN_VEHICLE_CONTROLLER_DATA_3_OUTIND			canstack_timeout_array0[VEHICLE_CONTROLLER_DATA_3].outind

/* vehicle_controller_data_4:0XC0AA1A7 */
#define CAN_VEHICLE_CONTROLLER_DATA_4_DATA_ARRAY			canstack_message_array0[VEHICLE_CONTROLLER_DATA_4].p_u8Data
#define CAN_VEHICLE_CONTROLLER_DATA_4_OUTIND			canstack_timeout_array0[VEHICLE_CONTROLLER_DATA_4].outind

/* vehicle_controller_data_5:0XC0BA1A7 */
#define CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY			canstack_message_array0[VEHICLE_CONTROLLER_DATA_5].p_u8Data
#define CAN_VEHICLE_CONTROLLER_DATA_5_OUTIND			canstack_timeout_array0[VEHICLE_CONTROLLER_DATA_5].outind

/* insulated_test_data_1:0X1819A1A4 */
#define CAN_INSULATED_TEST_DATA_1_DATA_ARRAY			canstack_message_array0[INSULATED_TEST_DATA_1].p_u8Data
#define CAN_INSULATED_TEST_DATA_1_OUTIND			canstack_timeout_array0[INSULATED_TEST_DATA_1].outind

/* dc_dc_data_1:0XC08A79A */
#define CAN_DC_DC_DATA_1_DATA_ARRAY			canstack_message_array0[DC_DC_DATA_1].p_u8Data
#define CAN_DC_DC_DATA_1_OUTIND			canstack_timeout_array0[DC_DC_DATA_1].outind

/* dashboard_data_1:0XC19A7A1 */
#define CAN_DASHBOARD_DATA_1_DATA_ARRAY			canstack_message_array0[DASHBOARD_DATA_1].p_u8Data
#define CAN_DASHBOARD_DATA_1_OUTIND			canstack_timeout_array0[DASHBOARD_DATA_1].outind

/* dashboard_data_2:0XC1AA7A1 */
#define CAN_DASHBOARD_DATA_2_DATA_ARRAY			canstack_message_array0[DASHBOARD_DATA_2].p_u8Data
#define CAN_DASHBOARD_DATA_2_OUTIND			canstack_timeout_array0[DASHBOARD_DATA_2].outind

/* bat_manage_system_1:0X1818D0F3 */
#define CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY			canstack_message_array0[BAT_MANAGE_SYSTEM_1].p_u8Data
#define CAN_BAT_MANAGE_SYSTEM_1_OUTIND			canstack_timeout_array0[BAT_MANAGE_SYSTEM_1].outind

/* bat_manage_system_2:0X181AD0F3 */
#define CAN_BAT_MANAGE_SYSTEM_2_DATA_ARRAY			canstack_message_array0[BAT_MANAGE_SYSTEM_2].p_u8Data
#define CAN_BAT_MANAGE_SYSTEM_2_OUTIND			canstack_timeout_array0[BAT_MANAGE_SYSTEM_2].outind

/* bat_manage_system_3:0X181BD0F3 */
#define CAN_BAT_MANAGE_SYSTEM_3_DATA_ARRAY			canstack_message_array0[BAT_MANAGE_SYSTEM_3].p_u8Data
#define CAN_BAT_MANAGE_SYSTEM_3_OUTIND			canstack_timeout_array0[BAT_MANAGE_SYSTEM_3].outind

/* bat_manage_system_4:0X181CD0F3 */
#define CAN_BAT_MANAGE_SYSTEM_4_DATA_ARRAY			canstack_message_array0[BAT_MANAGE_SYSTEM_4].p_u8Data
#define CAN_BAT_MANAGE_SYSTEM_4_OUTIND			canstack_timeout_array0[BAT_MANAGE_SYSTEM_4].outind

/* bat_manage_system_5:0X181DD0F3 */
#define CAN_BAT_MANAGE_SYSTEM_5_DATA_ARRAY			canstack_message_array0[BAT_MANAGE_SYSTEM_5].p_u8Data
#define CAN_BAT_MANAGE_SYSTEM_5_OUTIND			canstack_timeout_array0[BAT_MANAGE_SYSTEM_5].outind

/* bat_manage_system_6:0X181ED0F3 */
#define CAN_BAT_MANAGE_SYSTEM_6_DATA_ARRAY			canstack_message_array0[BAT_MANAGE_SYSTEM_6].p_u8Data
#define CAN_BAT_MANAGE_SYSTEM_6_OUTIND			canstack_timeout_array0[BAT_MANAGE_SYSTEM_6].outind

/* get motor_gear value */
CANSTACK_SET_SIG_BODY(motor_gear)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_2_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY)->vehicle_controller_data_2.motor_gear_1.5;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY)->vehicle_controller_data_2.motor_gear_0.5;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 15.0))
	{return FLOAT_MAX_VALUE;}

	if(fValue == 0 ) {return 0x00;}
	if(fValue == 1 ) {return 0x01;}
	if(fValue == 2 ) {return 0x02;}
	if(fValue == 3 ) {return 0x03;}
	if(fValue == 4 ) {return 0x04;}
	if(fValue == 5 ) {return 0x05;}
	if(fValue == 6 ) {return 0x06;}
	if(fValue == 19 ) {return 0x0d;}
	if(fValue == 20 ) {return 0x0e;}
	if(fValue == 21 ) {return 0x0f;}

	//we only care 'valid' parts
	return FLOAT_MAX_VALUE;
}
/* get vehicle_run_mode value */
CANSTACK_SET_SIG_BODY(vehicle_run_mode)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_2_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY)->vehicle_controller_data_2.vehicle_run_mode_1.875;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY)->vehicle_controller_data_2.vehicle_run_mode_0.875;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 2.0))
	{return FLOAT_MAX_VALUE;}

	if(fValue == 0 ) {return 0x01;}
	if(fValue == 1 ) {return 0x02;}

	//we only care 'valid' parts
	return FLOAT_MAX_VALUE;
}
/* get bat_charge_st value */
CANSTACK_SET_SIG_BODY(bat_charge_st)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_2_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY)->vehicle_controller_data_2.bat_charge_st_1.75;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY)->vehicle_controller_data_2.bat_charge_st_0.75;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 1.0))
	{return FLOAT_MAX_VALUE;}

	if(fValue == 0 ) {return 0x03;}
	if(fValue == 1 ) {return 0x01;}

	//we only care 'valid' parts
	return FLOAT_MAX_VALUE;
}
/* get mileage_acc_pedal value */
CANSTACK_SET_SIG_BODY(mileage_acc_pedal)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_3_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_3_DATA_ARRAY)->vehicle_controller_data_3.mileage_acc_pedal;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.4;
	if((fValue < 0.0) || (fValue > 100.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get mileage_brk_st value */
CANSTACK_SET_SIG_BODY(mileage_brk_st)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_3_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_3_DATA_ARRAY)->vehicle_controller_data_3.mileage_brk_st;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.4;
	if((fValue < 0.0) || (fValue > 100.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get vehicle_st value */
CANSTACK_SET_SIG_BODY(vehicle_st)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_4_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_4_DATA_ARRAY)->vehicle_controller_data_4.vehicle_st_1.75;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_4_DATA_ARRAY)->vehicle_controller_data_4.vehicle_st_0.75;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 3.0))
	{return FLOAT_MAX_VALUE;}

	if(fValue == 0 ) {return 0x01;}
	if(fValue == 1 ) {return 0x02;}
	if(fValue == 2 ) {return 0x03;}
	if(fValue == 3 ) {return 0x03;}

	//we only care 'valid' parts
	return FLOAT_MAX_VALUE;
}
/* get insulation_resist value */
CANSTACK_SET_SIG_BODY(insulation_resist)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_INSULATED_TEST_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_INSULATED_TEST_DATA_1_DATA_ARRAY)->insulated_test_data_1.insulation_resist_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_INSULATED_TEST_DATA_1_DATA_ARRAY)->insulated_test_data_1.insulation_resist_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 65534.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_total_voltage value */
CANSTACK_SET_SIG_BODY(bat_total_voltage)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_DC_DC_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_DC_DC_DATA_1_DATA_ARRAY)->dc_dc_data_1.bat_total_voltage_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_DC_DC_DATA_1_DATA_ARRAY)->dc_dc_data_1.bat_total_voltage_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	fValue += -1000;

	if((fValue < -1000.0) || (fValue > 5553.4))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_total_current value */
CANSTACK_SET_SIG_BODY(bat_total_current)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_DC_DC_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_DC_DC_DATA_1_DATA_ARRAY)->dc_dc_data_1.bat_total_current_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_DC_DC_DATA_1_DATA_ARRAY)->dc_dc_data_1.bat_total_current_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	fValue += -1000;

	if((fValue < -1000.0) || (fValue > 5553.4))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get vehicle_speed value */
CANSTACK_SET_SIG_BODY(vehicle_speed)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_DASHBOARD_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_DASHBOARD_DATA_1_DATA_ARRAY)->dashboard_data_1.vehicle_speed;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.5;
	if((fValue < 0.0) || (fValue > 127.5))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get vehicle_mileage value */
CANSTACK_SET_SIG_BODY(vehicle_mileage)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_DASHBOARD_DATA_2_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_DASHBOARD_DATA_2_DATA_ARRAY)->dashboard_data_2.vehicle_mileage_4.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_DASHBOARD_DATA_2_DATA_ARRAY)->dashboard_data_2.vehicle_mileage_3.0;
	unData.u8DataArray[2] = ((canstack_msg_data_t *)CAN_DASHBOARD_DATA_2_DATA_ARRAY)->dashboard_data_2.vehicle_mileage_2.0;
	unData.u8DataArray[3] = ((canstack_msg_data_t *)CAN_DASHBOARD_DATA_2_DATA_ARRAY)->dashboard_data_2.vehicle_mileage_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	if((fValue < 0.0) || (fValue > 999999.9))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_soc value */
CANSTACK_SET_SIG_BODY(bat_soc)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.bat_soc;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.4;
	if((fValue < 0.0) || (fValue > 102.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_max_cell_volt value */
CANSTACK_SET_SIG_BODY(bat_max_cell_volt)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_2_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_2_DATA_ARRAY)->bat_manage_system_2.bat_max_cell_volt_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_2_DATA_ARRAY)->bat_manage_system_2.bat_max_cell_volt_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.01;
	fValue += -100;

	if((fValue < -100.0) || (fValue > 555.35))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_min_cell_volt value */
CANSTACK_SET_SIG_BODY(bat_min_cell_volt)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_2_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_2_DATA_ARRAY)->bat_manage_system_2.bat_min_cell_volt_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_2_DATA_ARRAY)->bat_manage_system_2.bat_min_cell_volt_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.01;
	fValue += -100;

	if((fValue < -100.0) || (fValue > 555.35))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_max_temp value */
CANSTACK_SET_SIG_BODY(bat_max_temp)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_5_DATA_ARRAY)->bat_manage_system_5.bat_max_temp;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue += -40;

	if((fValue < -40.0) || (fValue > 215.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_max_temp_sub_no value */
CANSTACK_SET_SIG_BODY(bat_max_temp_sub_no)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_5_DATA_ARRAY)->bat_manage_system_5.bat_max_temp_sub_no;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_max_temp_probe_no value */
CANSTACK_SET_SIG_BODY(bat_max_temp_probe_no)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_5_DATA_ARRAY)->bat_manage_system_5.bat_max_temp_probe_no;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_min_temp value */
CANSTACK_SET_SIG_BODY(bat_min_temp)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_5_DATA_ARRAY)->bat_manage_system_5.bat_min_temp;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue += -40;

	if((fValue < -40.0) || (fValue > 215.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_min_temp_sub_no value */
CANSTACK_SET_SIG_BODY(bat_min_temp_sub_no)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_5_DATA_ARRAY)->bat_manage_system_5.bat_min_temp_sub_no;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_min_temp_probe_no value */
CANSTACK_SET_SIG_BODY(bat_min_temp_probe_no)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_5_DATA_ARRAY)->bat_manage_system_5.bat_min_temp_probe_no;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_max_volt_sub_no value */
CANSTACK_SET_SIG_BODY(bat_max_volt_sub_no)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_6_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_6_DATA_ARRAY)->bat_manage_system_6.bat_max_volt_sub_no;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_max_cell_volt_no value */
CANSTACK_SET_SIG_BODY(bat_max_cell_volt_no)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_6_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_6_DATA_ARRAY)->bat_manage_system_6.bat_max_cell_volt_no;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_min_volt_sub_no value */
CANSTACK_SET_SIG_BODY(bat_min_volt_sub_no)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_6_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_6_DATA_ARRAY)->bat_manage_system_6.bat_min_volt_sub_no;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get bat_min_cell_volt_no value */
CANSTACK_SET_SIG_BODY(bat_min_cell_volt_no)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_6_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_6_DATA_ARRAY)->bat_manage_system_6.bat_min_cell_volt_no;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}

/* get motor_controller_temp_1 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_controller_temp, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_2_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY)->vehicle_controller_data_2.motor_controller_temp_1;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue += -40;

	if((fValue < -40.0) || (fValue > 215.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_controller_temp_2 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_controller_temp, 2)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY)->vehicle_controller_data_5.motor_controller_temp_2;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue += -40;

	if((fValue < -40.0) || (fValue > 215.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_controller_temp value */
CANSTACK_SET_GROUP_BODY(motor_controller_temp)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(motor_controller_temp, 1);/* motor_controller_temp_1 */
		break;
		case 1:
			fValue = CANSTACK_GET_GROUP_SIG(motor_controller_temp, 2);/* motor_controller_temp_2 */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}
/* get motor_speed_1 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_speed, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY)->vehicle_controller_data_1.motor_speed_1_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY)->vehicle_controller_data_1.motor_speed_1_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.5;
	if((fValue < 0.0) || (fValue > 9999.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_speed_2 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_speed, 2)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY)->vehicle_controller_data_5.motor_speed_2_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY)->vehicle_controller_data_5.motor_speed_2_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.5;
	if((fValue < 0.0) || (fValue > 9999.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_speed value */
CANSTACK_SET_GROUP_BODY(motor_speed)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(motor_speed, 1);/* motor_speed_1 */
		break;
		case 1:
			fValue = CANSTACK_GET_GROUP_SIG(motor_speed, 2);/* motor_speed_2 */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}
/* get motor_torque_1 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_torque, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY)->vehicle_controller_data_1.motor_torque_1_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY)->vehicle_controller_data_1.motor_torque_1_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue += -32000;

	if((fValue < -3000.0) || (fValue > 3000.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_torque_2 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_torque, 2)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY)->vehicle_controller_data_5.motor_torque_2_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY)->vehicle_controller_data_5.motor_torque_2_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue += -32000;

	if((fValue < -3000.0) || (fValue > 3000.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_torque value */
CANSTACK_SET_GROUP_BODY(motor_torque)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(motor_torque, 1);/* motor_torque_1 */
		break;
		case 1:
			fValue = CANSTACK_GET_GROUP_SIG(motor_torque, 2);/* motor_torque_2 */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}
/* get motor_temp_1 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_temp, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_2_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_2_DATA_ARRAY)->vehicle_controller_data_2.motor_temp_1;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue += -40;

	if((fValue < -40.0) || (fValue > 215.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_temp_2 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_temp, 2)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY)->vehicle_controller_data_5.motor_temp_2;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue += -40;

	if((fValue < -40.0) || (fValue > 215.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_temp value */
CANSTACK_SET_GROUP_BODY(motor_temp)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(motor_temp, 1);/* motor_temp_1 */
		break;
		case 1:
			fValue = CANSTACK_GET_GROUP_SIG(motor_temp, 2);/* motor_temp_2 */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}
/* get motor_controller_voltage_1 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_controller_voltage, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY)->vehicle_controller_data_1.motor_controller_voltage_1_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY)->vehicle_controller_data_1.motor_controller_voltage_1_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	fValue += -1000;

	if((fValue < 0.0) || (fValue > 999.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_controller_voltage_2 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_controller_voltage, 2)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_DC_DC_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_DC_DC_DATA_1_DATA_ARRAY)->dc_dc_data_1.motor_controller_voltage_2_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_DC_DC_DATA_1_DATA_ARRAY)->dc_dc_data_1.motor_controller_voltage_2_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	fValue += -1000;

	if((fValue < -1000.0) || (fValue > 5553.4))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_controller_voltage value */
CANSTACK_SET_GROUP_BODY(motor_controller_voltage)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(motor_controller_voltage, 1);/* motor_controller_voltage_1 */
		break;
		case 1:
			fValue = CANSTACK_GET_GROUP_SIG(motor_controller_voltage, 2);/* motor_controller_voltage_2 */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}
/* get motor_controller_current_1 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_controller_current, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY)->vehicle_controller_data_1.motor_controller_current_1_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_1_DATA_ARRAY)->vehicle_controller_data_1.motor_controller_current_1_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	fValue += -1000;

	if((fValue < -999.0) || (fValue > 999.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_controller_current_2 value */
CANSTACK_SET_GROUP_SIG_BODY(motor_controller_current, 2)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_VEHICLE_CONTROLLER_DATA_5_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY)->vehicle_controller_data_5.motor_controller_current_2_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_VEHICLE_CONTROLLER_DATA_5_DATA_ARRAY)->vehicle_controller_data_5.motor_controller_current_2_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	fValue += -1000;

	if((fValue < -999.0) || (fValue > 999.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get motor_controller_current value */
CANSTACK_SET_GROUP_BODY(motor_controller_current)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(motor_controller_current, 1);/* motor_controller_current_1 */
		break;
		case 1:
			fValue = CANSTACK_GET_GROUP_SIG(motor_controller_current, 2);/* motor_controller_current_2 */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}
/* get rechar_energy_volt value */
CANSTACK_SET_GROUP_SIG_BODY(rechar_energy_volt, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.rechar_energy_volt_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.rechar_energy_volt_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	fValue += -1000;

	if((fValue < -1000.0) || (fValue > 5553.4))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get rechar_energy_volt value */
CANSTACK_SET_GROUP_BODY(rechar_energy_volt)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(rechar_energy_volt, 1);/* rechar_energy_volt */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}
/* get rechar_energy_curr value */
CANSTACK_SET_GROUP_SIG_BODY(rechar_energy_curr, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_1_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.rechar_energy_curr_2.0;
	unData.u8DataArray[1] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.rechar_energy_curr_1.0;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	fValue *= 0.1;
	fValue += -1000;

	if((fValue < -1000.0) || (fValue > 5553.4))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get rechar_energy_curr value */
CANSTACK_SET_GROUP_BODY(rechar_energy_curr)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(rechar_energy_curr, 1);/* rechar_energy_curr */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}
/* get rechar_probe_sum value */
CANSTACK_SET_GROUP_SIG_BODY(rechar_probe_sum, 1)
{
	float fValue = 0.0;
	uint32_t u32Value = 0;
	unData_type unData;
	unData.u32Data = 0;

	if(CAN_BAT_MANAGE_SYSTEM_4_OUTIND)
	{return FLOAT_MAX_VALUE;}

	unData.u8DataArray[0] = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_4_DATA_ARRAY)->bat_manage_system_4.rechar_probe_sum;

	u32Value = unData.u32Data;
	fValue = (float)(u32Value);

	if((fValue < 0.0) || (fValue > 255.0))
	{return FLOAT_MAX_VALUE;}

	return fValue;
}
/* get rechar_probe_sum value */
CANSTACK_SET_GROUP_BODY(rechar_probe_sum)
{
	float fValue = 0.0;
	uint8_t index = *(uint8_t *)param;

	switch(index)
	{
		case 0:
			fValue = CANSTACK_GET_GROUP_SIG(rechar_probe_sum, 1);/* rechar_probe_sum */
		break;
		default:
			fValue = FLOAT_MAX_VALUE;
		break;
	}
	return fValue;
}

CANSTACK_SET_SIG_BODY(highest_alarm_level);
/* get invalid_sig's value */
CANSTACK_SET_SIG_BODY(invalid_sig)
{return FLOAT_MAX_VALUE;}

sig_infor_t sig_infor_array[] =
{
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(vehicle_st)},	/* vehicle_st */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_charge_st)},	/* bat_charge_st */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(vehicle_run_mode)},	/* vehicle_run_mode */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(vehicle_speed)},	/* vehicle_speed */
	{ INVALID_UINT32, CANSTACK_SET_SIG_FUN_NAME(vehicle_mileage)},	/* vehicle_mileage */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(bat_total_voltage)},	/* bat_total_voltage */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(bat_total_current)},	/* bat_total_current */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_soc)},	/* bat_soc */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* dc_dc_st */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(motor_gear)},	/* motor_gear */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(insulation_resist)},	/* insulation_resist */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(mileage_acc_pedal)},	/* mileage_acc_pedal */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(mileage_brk_st)},	/* mileage_brk_st */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* motor_sum */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* motor_serial_num */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* motor_st */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(motor_controller_temp)},	/* motor_controller_temp */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(motor_speed)},	/* motor_speed */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(motor_torque)},	/* motor_torque */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(motor_temp)},	/* motor_temp */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(motor_controller_voltage)},	/* motor_controller_voltage */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(motor_controller_current)},	/* motor_controller_current */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* fuel_bat_voltage */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* fuel_bat_current */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* fuel_consumption_rate */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* fuel_bat_temp_probe_sum */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* probe_temp */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* hyd_sys_high_temp */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* hyd_sys_high_temp_probe_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* hyd_high_conc */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* hyd_high_conc_sensor_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* hyd_max_pressure */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* hyd_max_pressure_sensor_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* high_voltage_dc_dc_st */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* engine_st */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* crankshaft_speed */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* oil_consumption_rate */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_max_volt_sub_no)},	/* bat_max_volt_sub_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_max_cell_volt_no)},	/* bat_max_cell_volt_no */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(bat_max_cell_volt)},	/* bat_max_cell_volt */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_min_volt_sub_no)},	/* bat_min_volt_sub_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_min_cell_volt_no)},	/* bat_min_cell_volt_no */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(bat_min_cell_volt)},	/* bat_min_cell_volt */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_max_temp_sub_no)},	/* bat_max_temp_sub_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_max_temp_probe_no)},	/* bat_max_temp_probe_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_max_temp)},	/* bat_max_temp */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_min_temp_sub_no)},	/* bat_min_temp_sub_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_min_temp_probe_no)},	/* bat_min_temp_probe_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(bat_min_temp)},	/* bat_min_temp */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* rechar_energy_sys_sum */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* rechar_energy_sys_no */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(rechar_energy_volt)},	/* rechar_energy_volt */
	{ INVALID_UINT16, CANSTACK_SET_SIG_FUN_NAME(rechar_energy_curr)},	/* rechar_energy_curr */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* rechar_bat_cell_sum */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* rechar_f_bat_start_no */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* rechar_f_bat_cell_sum */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* rechar_bat_cell_volt */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(rechar_probe_sum)},	/* rechar_probe_sum */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(invalid_sig)},	/* rechar_bat_cell_temp */
	{ INVALID_UINT8, CANSTACK_SET_SIG_FUN_NAME(highest_alarm_level)},	/* highest_alarm_level */

};

sig_manager_t sig_manager = 
{
	sizeof(sig_infor_array) / sizeof(sig_infor_array[0]),
	sig_infor_array
};

float canstack_read_sig_value(sig_type sig_type)
{
	TBOX_ASSERT((uint8_t)sig_type < sig_manager.sig_sum);
	
	if((uint8_t)sig_type >= sig_manager.sig_sum)
	{ return FLOAT_MAX_VALUE;}
		
	return sig_manager.sig_infor_array[sig_type].get_sig_value_fun(0);
}

float canstack_read_group_sig_value(sig_type sig_type, uint8_t index)
{
	TBOX_ASSERT((uint8_t)sig_type < sig_manager.sig_sum);
	
	if((uint8_t)sig_type >= sig_manager.sig_sum)
	{ return FLOAT_MAX_VALUE;}
		
	return sig_manager.sig_infor_array[sig_type].get_sig_value_fun((void*)&index);
}

static uint8_t arg_arry[2] = {0, 0};

float canstack_read_multi_group_sig(sig_type sig_type, uint8_t group_index, uint8_t index)
{
	TBOX_ASSERT((uint8_t)sig_type < sig_manager.sig_sum);

	if((uint8_t)sig_type >= sig_manager.sig_sum)
	{ return FLOAT_MAX_VALUE;}

	arg_arry[0] = group_index;
	arg_arry[1] = index;

	return sig_manager.sig_infor_array[sig_type].get_sig_value_fun((void*)&arg_arry);
}

/*
typedef enum
{
	INVALID_UINT8 = 1,
	INVALID_UINT16,
	INVALID_UINT32,
	INVALID_OTHER_1,
	INVALID_OTHER_2,
}sig_invalid_value_type;
*/

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



/******************deal error status*******************/

#define ALARM_LEVEL_0	0
#define ALARM_LEVEL_1	1
#define ALARM_LEVEL_2	2
#define ALARM_LEVEL_3	3		// coresspond gb protocol highest alarm level

#define DEAL_OTHER_ERR(raw_val, level_0, level_1, level_2, level_3, alarm_level, errData) \
							if( raw_val == level_0) \
							{ \
								dat_gb_clear_other_err(errData);	\
								alarm_level = ALARM_LEVEL_0;	\
							} \
							else if( raw_val == level_1) \
							{ \
								dat_gb_add_other_err(errData);	\
								alarm_level = ALARM_LEVEL_1;	\
							} \
							else if( raw_val == level_2) \
							{ \
								dat_gb_add_other_err(errData);	\
								alarm_level = ALARM_LEVEL_2;	\
							} \
							else if( raw_val == level_3) \
							{ \
								dat_gb_add_other_err(errData);	\
								alarm_level = ALARM_LEVEL_3;	\
							} \
							else \
							{	\
								dat_gb_clear_other_err(errData);	\
								alarm_level = ALARM_LEVEL_0;	\
							}

#define DEAL_BAT_ERR(raw_val, level_0, level_1, level_2, level_3, alarm_level, errData) \
							if( raw_val == level_0) \
							{ \
								dat_gb_clear_batalarm_err(errData);	\
								alarm_level = ALARM_LEVEL_0;	\
							} \
							else if( raw_val == level_1) \
							{ \
								dat_gb_add_batalarm_err(errData);	\
								alarm_level = ALARM_LEVEL_1;	\
							} \
							else if( raw_val == level_2) \
							{ \
								dat_gb_add_batalarm_err(errData);	\
								alarm_level = ALARM_LEVEL_2;	\
							} \
							else if( raw_val == level_3) \
							{ \
								dat_gb_add_batalarm_err(errData);	\
								alarm_level = ALARM_LEVEL_3;	\
							} \
							else \
							{	\
								dat_gb_clear_batalarm_err(errData);	\
								alarm_level = ALARM_LEVEL_0;	\
							}
/* deal default msg error status fun */
void deal_default_msg_error_status(cuint8_t *p_u8Data)
{}

uint8_t bat_manage_system_1_ala_arr[9] = { 0 };
uint8_t bat_manage_system_1_ala_sum = 9;

/* deal bat_manage_system_1(0X1818D0F3) error status fun */
void deal_bat_manage_system_1_error_status(cuint8_t *p_u8Data)
{
	uint8_t data = 0xff;

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_bat_cell_volt_high;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[0], alarm_gb_bat_cell_volt_high);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_bat_cell_volt_low;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[1], alarm_gb_bat_cell_volt_low);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_soc_too_high;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[2], alarm_gb_soc_too_high);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_soc_low;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[3], alarm_gb_soc_low);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_energy_volt_low;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[4], alarm_gb_energy_volt_low);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_energy_volt_high;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[5], alarm_gb_energy_volt_high);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_insulation;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[6], alarm_gb_insulation);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_bat_temp_high;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[7], alarm_gb_bat_temp_high);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_1_DATA_ARRAY)->bat_manage_system_1.alarm_gb_temp_diff;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_1_ala_arr[8], alarm_gb_temp_diff);

}

uint8_t bat_manage_system_3_ala_arr[2] = { 0 };
uint8_t bat_manage_system_3_ala_sum = 2;

/* deal bat_manage_system_3(0X181BD0F3) error status fun */
void deal_bat_manage_system_3_error_status(cuint8_t *p_u8Data)
{
	uint8_t data = 0xff;

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_3_DATA_ARRAY)->bat_manage_system_3.alarm_gb_soc_altus;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_3_ala_arr[0], alarm_gb_soc_altus);

	data = ((canstack_msg_data_t *)CAN_BAT_MANAGE_SYSTEM_3_DATA_ARRAY)->bat_manage_system_3.alarm_gb_energy_overcharge;
	DEAL_BAT_ERR(data, 0, 1, 0xAA, 0xAA, bat_manage_system_3_ala_arr[1], alarm_gb_energy_overcharge);

}

CANSTACK_SET_SIG_BODY(highest_alarm_level)
{
	uint8_t i = 0;
	uint8_t alarm_level = ALARM_LEVEL_0;

	for (i = 0; i < bat_manage_system_1_ala_sum; i++)
		if (bat_manage_system_1_ala_arr[i] >= alarm_level)
			alarm_level = bat_manage_system_1_ala_arr[i];

	for (i = 0; i < bat_manage_system_3_ala_sum; i++)
		if (bat_manage_system_3_ala_arr[i] >= alarm_level)
			alarm_level = bat_manage_system_3_ala_arr[i];

	return alarm_level;
}


/******************deal error status*******************/

#ifdef USING_PROTOCOL_GB

userCode2Index_t st_gb_otherErrMap[] = 
{
	{ 0xffffffff },
};
userCode2IndexMan_t st_gb_otherErrMan =
{
	st_gb_otherErrMap,
	sizeof(st_gb_otherErrMap) / sizeof(st_gb_otherErrMap[0])
};

userCode2Index_t st_gb_chargeErrMap[] = {0};
userCode2IndexMan_t st_gb_chargeErrMan = {NULL, 0};

userCode2Index_t st_gb_motorErrMap[] = {0};
userCode2IndexMan_t st_gb_motorErrMan = {NULL, 0};

userCode2Index_t st_gb_engineErrMap[] = {0};
userCode2IndexMan_t st_gb_engineErrMan = {NULL, 0};

userCode2IndexMan_t* p_dat_gb_Code2IndexMan[] =
{
	(userCode2IndexMan_t*)&st_gb_chargeErrMan,
	(userCode2IndexMan_t*)&st_gb_motorErrMan,
	(userCode2IndexMan_t*)&st_gb_engineErrMan,
	(userCode2IndexMan_t*)&st_gb_otherErrMan,
};

#endif


#endif
