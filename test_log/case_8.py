
def function_8(rows_list):
    result_list8 = []
    for i in range(0, len(rows_list)):
        if rows_list[i]['充电状态'] == '停车充电':
            if [rows_list[i]['驱动电机转速'], rows_list[i]['驱动电机转矩'],\
                rows_list[i]['电机控制器输入电压'], rows_list[i]['电机控制器直流电流'], \
                rows_list[i]['加速踏板行程'],rows_list[i]['制动踏板状态']] != 0:
                result_list8.append(rows_list[i]['log行号'])
                # print(rows_list[i]['log行号'])
    print('case_8:'+ str(result_list8))
    return [result_list8]