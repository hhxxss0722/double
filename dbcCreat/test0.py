import os
import xlrd
import win32ui
import shutil

dlg = win32ui.CreateFileDialog(1)
dlg.SetOFNInitialDir('C:\1work\T-box\Tools')
dlg.DoModal()

filename = dlg.GetPathName()
my_path = os.path.abspath('main.py')
print(my_path)
logpath = os.path.abspath(os.path.join(os.path.dirname(my_path),'19000101150439'))
print(logpath)
if os.path.exists(logpath):
    shutil.rmtree(logpath)

os.makedirs(logpath)

log_name = 'raw_log.txt'
txt_name = 'log_t.txt'
exc_name = 'log_x.xlsx'
err_name = 'log_error.txt'

log_file = open(os.path.join(logpath,log_name),'w')
log_file.write('1111111111111111')

# print(os.path.split(my_path)[0])
# print(os.path.basename(my_path))
print(os.path.dirname(my_path))
base_path = os.path.dirname(my_path)
print(os.path.exists(base_path+'/pre_dbc'))
data = xlrd.open_workbook(filename)
table = data.sheet_by_index(0)
print(table.row_values(13))
print(table.ncols)

# newfile = open(os.path.dirname(my_path)+'\\dbc.txt','w')
# newfile.write('1231231')
# newfile.close()

