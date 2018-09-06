
def function_18(col_dic):
    tempControllerStation = []
    for i in range(0,len(col_dic['充电状态'])):
        if col_dic['充电状态'][i] == '停车充电' and 'Invalid' not in col_dic['驱动电机状态'][i] and col_dic['驱动电机状态'][i] != '准备':
            tempControllerStation.append(col_dic['log行号'][i])
    print('case_18:'+str(tempControllerStation))
    return [tempControllerStation]

