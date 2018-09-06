import func

def function_1_2(rows_list):
    # min_vol_value, max_vol_value, min_vol_index, max_vol_index = [[]]*4
    # min_tpr_value, max_tpr_value, min_tpr_index, max_tpr_index = [[]]*4
    min_vol_value = []
    max_vol_value = []
    min_vol_index = []
    max_vol_index = []
    min_tpr_value = []
    max_tpr_value = []
    min_tpr_index = []
    max_tpr_index = []

    for i in range(0, len(rows_list)):
        if 'Invalid' not in rows_list[i]['电池单体电压最低值']:
            temp_min_vol_value,temp_max_vol_value,temp_min_vol_index,tem_max_vol_index = function(rows_list,i,'电池单体电压最低值','电池单体电压最高值','最低电压电池单体代号','最高电压电池单体代号','单体电池电压')
            temp_min_tpr_value, temp_max_tpr_value, temp_min_tpr_index, temp_max_tpr_index = function(rows_list,i,'最低温度值','最高温度值', '最低温度探针序号','最高温度探针序号','探针温度值')
            min_vol_value.append(temp_min_vol_value)
            max_vol_value.append(temp_max_vol_value)
            min_vol_index.append(temp_min_vol_index)
            max_vol_index.append(tem_max_vol_index)

            min_tpr_value.append(temp_min_tpr_value)
            max_tpr_value.append(temp_max_tpr_value)
            min_tpr_index.append(temp_min_tpr_index)
            max_tpr_index.append(temp_max_tpr_index)
    resultList = [min_vol_value,max_vol_value,min_vol_index,max_vol_index,min_tpr_value,max_tpr_value,min_tpr_index,max_tpr_index]

    for temp in resultList:
        temp = func.delNul(temp)

    print('case_1:电池单体电压最低值错误:'+str(min_vol_value))
    print('       电池单体电压最高值错误:' + str(max_vol_value))
    print('       最低电压电池单体代号错误:' + str(min_vol_index))
    print('       最高电压电池单体代号错误:' + str(max_vol_index))
    print('       最低温度值错误:' + str(min_tpr_value))
    print('       最高温度值错误:' + str(max_tpr_value))
    print('       最低温度探针序号错误:' + str(min_tpr_index))
    print('       最高温度探针序号错误:' + str(max_tpr_index))

    return [min_vol_value,max_vol_value,min_vol_index,max_vol_index,min_tpr_value,max_tpr_value,min_tpr_index,max_tpr_index]

def function(var_rows_list,index, name_min_value, name_max_value, name_min_index, name_max_index, name_total_value):

    vol_list = var_rows_list[index][name_total_value]
    err_min_value = ''
    err_max_value = ''
    err_min_index = ''
    err_max_index = ''

    if vol_list :
        vol_list = vol_list[1:-1].split(',')
        vol_list = list(map(float, vol_list))
        # if 'Invalid' not in rows_list[index][name_min_value] or 'Invalid' not in rows_list[index][name_max_value]:
        if float(var_rows_list[index][name_min_value]) != min(vol_list):
            err_min_value = var_rows_list[index]['log行号']
        if float(var_rows_list[index][name_max_value])!= max(vol_list):
            err_max_value = var_rows_list[index]['log行号']
        # else:
        #     print(rows_list[index]['log行号']+'行存在无效值')

        # if 'Invalid' not in rows_list[index][name_min_index] or 'Invalid' not in rows_list[index][name_max_index]:
        if int(float(var_rows_list[index][name_min_index])) != vol_list.index(min(vol_list)):
            err_min_index = var_rows_list[index]['log行号']
        if int(float(var_rows_list[index][name_max_index])) != vol_list.index(max(vol_list)):
            err_max_index = var_rows_list[index]['log行号']
        # else:
        #     print(rows_list[index]['log行号'] + '行存在无效值')

    return err_min_value,err_max_value,err_min_index,err_max_index



