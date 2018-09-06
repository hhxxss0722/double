import xlrd,xlwt
from xlutils.copy import copy

# work_bk = xlrd.open_workbook(r'c:\\1.xlsx',formatting_info=True)
# rb = work_bk.sheet_by_index(0)
# wb = copy(rb)
# sheet = wb.get_sheet(0)
# sheet.write(5,2,'string')
# wb.save(r'c:\\1.xlsx')

import xlrd
import xlwt
from xlutils.copy import copy
import os.path
rb = xlrd.open_workbook(r'C:\\1work\\csut1.xls')
r_sheet = rb.sheet_by_index(0)
wb = copy(rb)
sheet = wb.get_sheet(0)
sheet.write(6,3,"string11")
wb.save(r'C:\\1work\\csut1.xls')