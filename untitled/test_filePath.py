
import win32ui,os
import sys
import xlrd
import re

# sys.setdefaultencoding('utf-8')

# dlg = win32ui.CreateFileDialog(1)
# dlg.DoModal()
dlg = win32ui.CreateFileDialog(1)
# dlg.SetOFNInitialDir('D:/Python27/PYTHON')
dlg.DoModal()
filename = dlg.GetPathName()
print filename
sel_path = os.path.dirname(filename)
print sel_path
basename = os.path.basename(filename)
print basename

basefile_1 = os.path.join(sel_path,"pre_dbc\dbc_pre1.txt")
basefile_2 = os.path.join(sel_path,"pre_dbc\dbc_pre2.txt")
pre_dbc = open(basefile_1,'r')
# print pre_dbc.read()
result_path = os.path.join(sel_path,'result1')
if not os.path.isdir(result_path):
    os.makedirs(result_path)
dbc_file = os.path.join(result_path,'dbc_result.dbc')
open_dbc_file = open(dbc_file,'w')
open_dbc_file.write(pre_dbc.read())
print 'no open execl'
data = xlrd.open_workbook(filename)
print 'open execl'
table = data.sheet_by_index(0)
# s = table.row_values(6)[13].split('\n')
s = [x.strip() for x in table.row_values(6)[13].split('\n')]
for single_vt in s:
    sig_vt_one = re.split(r'\W+', single_vt, 1)
    print sig_vt_one

print s
# print table.row(6)[4].value



