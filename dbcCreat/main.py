import win32ui
import os
import xlrd

# dbc_pre1_file = open()

if __name__ == '__main__':
    dlg = win32ui.CreateFileDialog(1)
    dlg.SetOFNInitialDir('C:\1work\T-box\Tools\dbc生成工具')
    dlg.DoModal()

    filename = dlg.GetPathName()

    print(filename)
    print(os.path.abspath('main.py'))
    # data = xlrd.open_workbook(filename, app_visible=False)
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_index(0)
    print(table.nrows)