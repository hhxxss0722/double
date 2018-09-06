
def function_10(rows_list):
    err_result = []
    for i in range(0,len(rows_list)):
        temp_err_result = rows_list[i]['log行号']
        if type(rows_list[i]['总电流']) == str:
            if rows_list[i]['总电流'].find("Invalid") == -1:
                if rows_list[i]['充电状态'] == '停车充电' and float(rows_list[i]['总电流']) >= 0.0:
                    err_result.append(temp_err_result)
                if (rows_list[i]['充电状态'] == '充电完成' or rows_list[i]['充电状态'] == '未充电') and float(rows_list[i]['总电流']) < 0.0:
                    err_result.append(temp_err_result)
        if type(rows_list[i]['总电流']) == float:
                if rows_list[i]['充电状态'] == '停车充电' and rows_list[i]['总电流'] >= 0.0:
                    err_result.append(temp_err_result)
                if (rows_list[i]['充电状态'] == '充电完成' or rows_list[i]['充电状态'] == '未充电') and rows_list[i]['总电流'] < 0.0:
                    err_result.append(temp_err_result)

    print('case_10电流值异常：'+ str(err_result)+'/n')
    return [err_result]