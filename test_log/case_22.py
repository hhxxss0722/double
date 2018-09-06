
def function_22(col_dic):
    err_result = {}
    nameList = ['运行模式', 'DC/DC状态', '驱动电机个数', '驱动电机序号', '最高电压电池子系统号', '可充储子系统个数', '可充储子系统号', '单体电池总数', '本帧单体电池总数',
                '本帧起始电池序号']
    for key in nameList:
        temp_list = ''
        err_result[key] = []
        for index in range(0,len(col_dic[key])):
            if temp_list == ''and 'Invalid' not in col_dic[key][index]:
                temp_list = col_dic[key][index]
            elif temp_list != col_dic[key][index]:
                err_result[key].append(col_dic['log行号'][index])
    print('case_22:' + str(err_result))
    return [err_result]
