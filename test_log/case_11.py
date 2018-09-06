
def function_11(col_dic):
    err_vol_result = []
    err_tpr_result = []
    vol_total = col_dic['单体电池电压']
    tpr_total = col_dic['探针温度值']
    for i in range(0,len(vol_total)):
        temp_err_result = col_dic['log行号'][i]
        # print(vol_list[i])
        vol_list = eval(vol_total[i])    #把字符串中的内容变成有效的值  eval('[1,2,3,4]')=[1,2,3,4]
        tpr_list = eval(tpr_total[i])
        d_vol_value = max(vol_list) - min(vol_list)
        d_tpr_value = max(tpr_list) - min(tpr_list)
        if d_vol_value >= 1.0:
            err_vol_result.append(temp_err_result)
        if d_tpr_value >2.0:
            err_tpr_result.append(temp_err_result)
    print('case_11结果：'+ str(err_vol_result))
    print( '           ' + str(err_tpr_result))
    return  [err_vol_result,err_tpr_result]