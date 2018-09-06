

def function_20(col_dic):
    err_result = {}
    nameList = ['累计里程', '车速', 'DC/DC状态', '档位', '加速踏板行程', '制动踏板状态', ]
    for key in nameList:
        temp_list = ''
        err_result[key] = []
        for index in range(0,len(col_dic[key])):
            if col_dic['车辆状态'][index] == '熄火' and col_dic['充电状态'][index] == '停车充电' and 'Invalid' not in col_dic[key][index]:
                # print(col_dic[key][index])
                if temp_list == '':
                   temp_list = col_dic[key][index]
                   # print('kongzhi fuzhi'+ str(temp_list))
                elif temp_list != col_dic[key][index]:
                    err_result[key].append(col_dic['log行号'][index])
    print('case_20:'+str(err_result))
    return [err_result]
