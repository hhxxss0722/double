#ifndef CAN_STACK_JZ_V10_MSG_H
#define CAN_STACK_JZ_V10_MSG_H

#include "canstack_sig.h"

#ifdef CANSTACK_JZ_V10

/* about messages */
typedef union
{
	uint8_t byte[8];
/********************CAN_0********************/

	/* vehicle_controller_data_1:0XC03A1A7 */
	struct
	{
		uint8_t motor_controller_voltage_1_2.0;
		uint8_t motor_controller_voltage_1_1.0;
		uint8_t motor_controller_current_1_2.0;
		uint8_t motor_controller_current_1_1.0;
		uint8_t motor_torque_1_2.0;
		uint8_t motor_torque_1_1.0;
		uint8_t motor_speed_1_2.0;
		uint8_t motor_speed_1_1.0;
		
	}vehicle_controller_data_1;

	/* vehicle_controller_data_2:0XC04A1A7 */
	struct
	{
		uint8_t motor_temp_1;
		uint8_t motor_controller_temp_1;
		uint8_t :8;
		uint8_t :8;
		uint8_t motor_gear_1.5;
		uint8_t motor_gear_1:4;
		uint8_t :4;
		uint8_t :5;
		uint8_t vehicle_run_mode_1.875:3;
		uint8_t vehicle_run_mode_1:7;
		uint8_t :1;
		uint8_t :5;
		uint8_t bat_charge_st_1.75:3;
		uint8_t bat_charge_st_1:6;
		uint8_t :2;
		uint8_t :8;
		uint8_t :8;
		
	}vehicle_controller_data_2;

	/* vehicle_controller_data_3:0XC06A1A7 */
	struct
	{
		uint8_t mileage_acc_pedal;
		uint8_t mileage_brk_st;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		
	}vehicle_controller_data_3;

	/* vehicle_controller_data_4:0XC0AA1A7 */
	struct
	{
		uint8_t :8;
		uint8_t :4;
		uint8_t vehicle_st_1.75:4;
		uint8_t vehicle_st_1:6;
		uint8_t :2;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		
	}vehicle_controller_data_4;

	/* vehicle_controller_data_5:0XC0BA1A7 */
	struct
	{
		uint8_t motor_temp_2;
		uint8_t motor_controller_temp_2;
		uint8_t motor_controller_current_2_2.0;
		uint8_t motor_controller_current_2_1.0;
		uint8_t motor_torque_2_2.0;
		uint8_t motor_torque_2_1.0;
		uint8_t motor_speed_2_2.0;
		uint8_t motor_speed_2_1.0;
		
	}vehicle_controller_data_5;

	/* insulated_test_data_1:0X1819A1A4 */
	struct
	{
		uint8_t insulation_resist_2.0;
		uint8_t insulation_resist_1.0;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		
	}insulated_test_data_1;

	/* dc_dc_data_1:0XC08A79A */
	struct
	{
		uint8_t bat_total_voltage_2.0;
		uint8_t bat_total_voltage_1.0;
		uint8_t bat_total_current_2.0;
		uint8_t bat_total_current_1.0;
		uint8_t motor_controller_voltage_2_2.0;
		uint8_t motor_controller_voltage_2_1.0;
		uint8_t :8;
		uint8_t :8;
		
	}dc_dc_data_1;

	/* dashboard_data_1:0XC19A7A1 */
	struct
	{
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t vehicle_speed;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		
	}dashboard_data_1;

	/* dashboard_data_2:0XC1AA7A1 */
	struct
	{
		uint8_t vehicle_mileage_4.0;
		uint8_t vehicle_mileage_3.0;
		uint8_t vehicle_mileage_2.0;
		uint8_t vehicle_mileage_1.0;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		
	}dashboard_data_2;

	/* bat_manage_system_1:0X1818D0F3 */
	struct
	{
		uint8_t rechar_energy_volt_2.0;
		uint8_t rechar_energy_volt_1.0;
		uint8_t rechar_energy_curr_2.0;
		uint8_t rechar_energy_curr_1.0;
		uint8_t bat_soc;
		uint8_t alarm_gb_bat_cell_volt_high_1.125;
		uint8_t alarm_gb_bat_cell_volt_high_1:1;
		uint8_t alarm_gb_bat_cell_volt_low_1.25:7;
		uint8_t alarm_gb_bat_cell_volt_low_1:2;
		uint8_t alarm_gb_soc_too_high_1.375:6;
		uint8_t alarm_gb_soc_too_high_1:3;
		uint8_t alarm_gb_soc_low_1.5:5;
		uint8_t alarm_gb_soc_low_1:4;
		uint8_t :4;
		uint8_t :5;
		uint8_t alarm_gb_energy_volt_low_1.75:3;
		uint8_t alarm_gb_energy_volt_low_1:6;
		uint8_t alarm_gb_energy_volt_high_1.875:2;
		uint8_t alarm_gb_energy_volt_high_1:7;
		uint8_t :1;
		uint8_t :2;
		uint8_t alarm_gb_insulation_1.375:6;
		uint8_t alarm_gb_insulation_1:3;
		uint8_t :5;
		uint8_t :5;
		uint8_t alarm_gb_bat_temp_high_1.75:3;
		uint8_t alarm_gb_bat_temp_high_1:6;
		uint8_t :2;
		uint8_t :7;
		uint8_t alarm_gb_temp_diff:1;
		uint8_t :8;
		
	}bat_manage_system_1;

	/* bat_manage_system_2:0X181AD0F3 */
	struct
	{
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t bat_max_cell_volt_2.0;
		uint8_t bat_max_cell_volt_1.0;
		uint8_t bat_min_cell_volt_2.0;
		uint8_t bat_min_cell_volt_1.0;
		
	}bat_manage_system_2;

	/* bat_manage_system_3:0X181BD0F3 */
	struct
	{
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t alarm_gb_soc_altus_1.125;
		uint8_t alarm_gb_soc_altus_1:1;
		uint8_t alarm_gb_energy_overcharge_1.25:7;
		uint8_t alarm_gb_energy_overcharge_1:2;
		uint8_t :6;
		
	}bat_manage_system_3;

	/* bat_manage_system_4:0X181CD0F3 */
	struct
	{
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t rechar_probe_sum;
		
	}bat_manage_system_4;

	/* bat_manage_system_5:0X181DD0F3 */
	struct
	{
		uint8_t bat_max_temp;
		uint8_t bat_max_temp_sub_no;
		uint8_t bat_max_temp_probe_no;
		uint8_t bat_min_temp;
		uint8_t bat_min_temp_sub_no;
		uint8_t bat_min_temp_probe_no;
		uint8_t :8;
		uint8_t :8;
		
	}bat_manage_system_5;

	/* bat_manage_system_6:0X181ED0F3 */
	struct
	{
		uint8_t bat_max_volt_sub_no;
		uint8_t bat_max_cell_volt_no;
		uint8_t bat_min_volt_sub_no;
		uint8_t bat_min_cell_volt_no;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		uint8_t :8;
		
	}bat_manage_system_6;
}canstack_msg_data_t;

typedef enum
{
	/****CAN_0****/
	VEHICLE_CONTROLLER_DATA_1 = 0,
	VEHICLE_CONTROLLER_DATA_2 = 1,
	VEHICLE_CONTROLLER_DATA_3 = 2,
	VEHICLE_CONTROLLER_DATA_4 = 3,
	VEHICLE_CONTROLLER_DATA_5 = 4,
	INSULATED_TEST_DATA_1 = 5,
	DC_DC_DATA_1 = 6,
	DASHBOARD_DATA_1 = 7,
	DASHBOARD_DATA_2 = 8,
	BAT_MANAGE_SYSTEM_1 = 9,
	BAT_MANAGE_SYSTEM_2 = 10,
	BAT_MANAGE_SYSTEM_3 = 11,
	BAT_MANAGE_SYSTEM_4 = 12,
	BAT_MANAGE_SYSTEM_5 = 13,
	BAT_MANAGE_SYSTEM_6 = 14,
}msg_type;

#endif

#endif
