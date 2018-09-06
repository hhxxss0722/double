
#将一列字符串列表转换为float列表
def str_to_flo(var_list):
    var_list = var_list[1:-1].split(',')
    vol_list = list(map(float, var_list))   #将字符列表转换为float列表

    return vol_list

def del_valid(var_list):
    temp_list = []
    for i in range(0,len(var_list)):
        if 'Invalid' not in var_list[i]:
            temp_list.append(var_list[i])

    return temp_list

def delNul(varList):
    while '' in varList:
        varList.remove('')
    return varList