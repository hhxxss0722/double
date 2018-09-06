
def function_6(rows_list):
    err_result = {}
    for i in range(0,len(rows_list)):
        if 'Invalid' not in rows_list[i]['总电压']:
            vol_list = rows_list[i]['单体电池电压']
            vol_list = vol_list[1:-1].split(',')
            vol_list = list(map(float, vol_list))
            if abs(float(rows_list[i]['总电压']) - sum(vol_list)) >= 2:
                err_result[rows_list[i]['log行号']] = [rows_list[i]['总电压'],round(sum(vol_list),2)]
    print('case_6:电压值不相等的：'+ str(err_result))

    return [err_result]