import xlrd
from xlutils import copy
import xlwt
import numpy

work_bk = xlrd.open_workbook(r'C:\1work\整理后数据.xlsx')
sheet = work_bk.sheet_by_index(0)
ncols = sheet.col_values(3)
nrows1 = []
for index in ncols:
    if type(index)!=str:
        index = int(index)
        nrows1.append(index)
# print(nrows1)

newTable = copy.copy(work_bk)
newSheet = newTable.get_sheet(0)
for index in range(0,len(nrows1)):
    newSheet.write(index+1,6,nrows1[index])

# newTable.save('newTable2.xls')

# k = 4
# a = numpy.array(newSheet)
# a[numpy.argpartition(a,-4)[-4:]]
# print(a)
import func

s = ['', '', '', '', '', '', '', '', '', '', '', '', '', '54', '57', '58', '59', '62', '', '', '', '', '', '', '', '', '', '78', '79', '82', '83', '88', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '113', '114', '117', '118', '119', '', '', '', '', '', '', '', '', '', '137', '138', '139', '142', '143', '147', '', '', '', '', '', '', '', '', '', '', '203', '', '210', '211', '214', '215', '216', '219', '220', '', '224', '225', '226', '229', '', '231', '234', '', '', '239', '240', '241', '', '245', '246', '249', '', '251', '254', '255', '', '259', '260', '261', '264', '265', '266', '269', '270', '271', '274', '275', '276', '279', '280', '281', '284', '285', '286', '289', '290', '291', '294', '295', '', '299', '300', '', '', '305', '306', '309', '', '311', '314', '315', '316', '319', '320', '321', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '414', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '442', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '503', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '529', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '564', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '592', '', '', '', '', '608', '', '612', '613', '616', '617', '618', '621', '622', '623', '626', '628', '631', '', '633', '636', '637']
s = func.delNul(s)
print(s)

import sys

def append(list_, name):
    list_.append((name, sys._getframe().f_back.f_locals[name]))