
import func

def function_14(col_dic):
    errRult = []
    colValue = list(map(float, func.del_valid(col_dic['累计里程'])))
    tOF = all(x<=y for x, y in zip(colValue, colValue[1:]))
    for i in range(1,len(colValue)):
        if colValue[i]<colValue[i-1]:
            print(col_dic['log行号'][i])
            errRult.append(col_dic['log行号'][i])
    print('case_14:'+ str(errRult))
    return [errRult]



