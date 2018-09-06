
import file_deal
import win32ui
import time
import case_8,case_1_2,case_6,case_7,case_10,case_11,case_13,case_14,case_18,case_20,case_22

curTime = time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))

def open_file():
    dlg = win32ui.CreateFileDialog(1)   # 1表示打开文件对话框,0表示保存文件对话框,
    dlg.SetOFNInitialDir('C:/Users/Administrator/Desktop/log')
    dlg.DoModal()
    file_path = dlg.GetPathName()
    return file_path
rowsList, colDic = file_deal.data_result(open_file())
case1Rult = case_1_2.function_1_2(rowsList)
case6Rult = case_6.function_6(rowsList)
case7Rult = case_7.function_7(rowsList)
case8Rult = case_8.function_8(rowsList)
case10Rult = case_10.function_10(rowsList)
case11Rult = case_11.function_11(colDic)
case13Rult = case_13.function_13(rowsList)
case14Rult = case_14.function_14(colDic)
case18Rult = case_18.function_18(colDic)
case20Rult = case_20.function_20(colDic)
case22Rult = case_22.function_22(colDic)
resultWB,dataSheet = file_deal.open_xlwt()

work_bk,table,sheet = file_deal.modify_xlrd(r'C:\1work\python\test_log\result.xlsx','Sheet1')
i = 0
for index in range(1,23):
    if 'case'+ str(index) + 'Rult' in dir():
        if len(eval('case'+ str(index) + 'Rult')) != 0:
            for j in range(0,len(eval('case'+ str(index) + 'Rult'))):
                sheet.write(j+i,3,str(eval('case'+ str(index) + 'Rult')[j]))
            i = i + len(eval('case' + str(index) + 'Rult'))
        else:
            i=i+1
work_bk.save(curTime+'_result.xls')
a = input()