
import file_deal
import win32ui
import func

# def open_file():
#     dlg = win32ui.CreateFileDialog(1)   # 1表示打开文件对话框,0表示保存文件对话框,
#     dlg.SetOFNInitialDir('C:/Users/Administrator/Desktop/log')
#     dlg.DoModal()
#
#     file_path = dlg.GetPathName()
#     return file_path
#
# rows_list, col_dic = file_deal.data_result(open_file())

s = ['311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', 'Invalid(FFFFFFFF)', 'Invalid(FFFFFFFF)', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', 'Invalid(FFFFFFFF)', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.5', '311.6', '311.6', '311.7', '311.8', '311.9', '312.0', '312.1', '312.1', '312.2', '312.3', '312.4', '312.4', '312.5', '312.6', '312.7', '312.8', '312.8', '312.9', '313.0', '313.1', '313.2', '313.3', '313.3', '313.4', '313.5', '313.5', '313.6', '313.7', '313.7', '313.8', '313.8', '313.9', '314.0', '314.0', '314.0', '314.1', '314.2', '314.2', '314.3', '314.4', '314.4', '314.4', '314.5', '314.6', '314.6', '314.7', '314.8', '314.9', '314.9', '315.0', '315.1', '315.1', '315.2', '315.2', '315.3', '315.3', '315.3', '315.4', '315.4', '311.5', '311.5', '311.6', '311.6', '311.7', '311.8', '311.9', '312.0', '312.1', '312.1', '312.2', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4', 'Invalid(FFFFFFFF)', '315.4', '315.4', '315.4', '315.4', '315.4', '315.4']
# vol_list = list(map(float, s))
s = func.del_valid(s)
print(s)

