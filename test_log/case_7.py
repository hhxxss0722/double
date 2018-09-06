
def function_7(rows_list):
    err_result = []
    for i in range(0,len(rows_list)):
        if 'Invalid' not in rows_list[i]['总电流'] or 'Invalid' not in rows_list[i]['装置电流']:
            if float(rows_list[i]['总电流']) != float(rows_list[i]['装置电流']):
                temp_err_result = rows_list[i]['log行号']
                err_result.append(temp_err_result)
    print('case_7:电流值不相等的：'+ str(err_result))
    return [err_result]