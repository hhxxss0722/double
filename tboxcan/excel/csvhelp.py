#coding:utf-8
import xlwt
def SaveExcel(path,t):
    i=0
    try:
        head=['id','imei','指令头','状态','数据','时间']
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('EMC Test')
        hl=len(head)
        for i in range(0,hl):
            sheet.write(0,i,head[i])#第0行第一列写入内容
        tl = len(t)
        for i in range(0,tl):
            e=t[i]
            sheet.write(i+1,0,str(e.id))
            sheet.write(i+1,1,str(e.imei))
            sheet.write(i+1,2,str(e.head))
            sheet.write(i+1,3,str(e.state))
            sheet.write(i+1,4,str(e.xml))
            sheet.write(i+1,5,str(e.date))
        wbk.save(path)
        i=1
    except Exception as e:
        i=-1
    return i
