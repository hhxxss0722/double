
def function_13(rows_list):
    err_result = []
    for i in range(0,len(rows_list)):
        temp_err_result = rows_list[i]['log行号']
        if type(rows_list[i]['总电流']) == str:
            if rows_list[i]['档位'] == '0E'and 'Invalid' not in rows_list[i]['总电流'] :
                if float(rows_list[i]['制动踏板状态']) > 0.0 and float(rows_list[i]['总电流']) > 0.0:
                    err_result.append(temp_err_result)
                if float(rows_list[i]['加速踏板行程']) >= 0.0 and float(rows_list[i]['总电流']) < 0.0:
                    err_result.append(temp_err_result)
        if type(rows_list[i]['总电流']) == float:
            if rows_list[i]['档位'] == '0E' :
                if float(rows_list[i]['制动踏板状态']) > 0.0 and rows_list[i]['总电流'] > 0.0:
                    err_result.append(temp_err_result)
                if float(rows_list[i]['加速踏板行程']) >= 0.0 and rows_list[i]['总电流'] < 0.0:
                    err_result.append(temp_err_result)
    print('case_13:'+ str(err_result))
    return [err_result]