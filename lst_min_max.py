# -*- coding: utf-8 -*-

import os
import re
import win32ui

def run():	 
	dlg = win32ui.CreateFileDialog(1) # 1表示打开文件对话框
	# dlg.SetOFNInitialDir('D:/Python27/PYTHON') # 设置打开文件对话框中的初始显示目录
	dlg.DoModal()
	 
	filename = dlg.GetPathName() # 获取选择的文件名称
	if filename == '':
		quit(1)

	select_path = os.path.split(filename)[0]
	direct_name = os.path.split(filename)[1]
	folder_name = re.split('\.',direct_name)[0]
	
	return filename 

if __name__ == "__main__":
	filename  = run()
	infile  =  open(filename, "r")
	# strr = [3.549, 3.551, 3.552, 3.549, 3.55, 3.552, 3.551, 3.549, 3.551, 3.55, 3.55, 3.548, 3.552, 3.553, 3.553, 3.552, 3.552, 3.552, 3.55, 3.55, 3.551, 3.55, 3.551, 3.548, 3.552, 3.55, 3.547, 3.547, 3.55, 3.552, 3.551, 3.551, 3.551, 3.549, 3.551, 3.545, 3.549, 3.551, 3.549, 3.546, 3.55, 3.55, 3.536, 3.549, 3.548, 3.548, 3.553, 3.546, 3.55, 3.547, 3.55, 3.55, 3.554, 3.55, 3.551, 3.549, 3.55, 3.55, 3.551, 3.552, 3.552, 3.552, 3.552, 3.549, 3.551, 3.552, 3.549, 3.549, 3.552, 3.549, 3.549, 3.551, 3.549, 3.549, 3.552, 3.549, 3.55, 3.549, 3.549, 3.548, 3.555, 3.55, 3.549, 3.55, 3.551, 3.551, 3.551, 3.551, 3.552, 3.55, 3.553, 3.551, 3.549, 3.549, 3.549, 3.549, 3.55, 3.55, 3.55, 3.55, 3.548, 3.548, 3.552, 3.549, 3.551, 3.55, 3.548, 3.548, 3.553, 3.55, 3.551, 3.549]
	
	# print strr
	# print strr.index(min(strr)),min(strr)
	i = 2
	for line in infile: 
		# print line
		curr = [float(x) for x in line.split(',')]
		# curr = list(line)
		# print type(curr),curr
		print ("%s:  %s  ->  %s   ,   %s  ->  %s "%(i,curr.index(max(curr))+1,max(curr),curr.index(min(curr))+1,min(curr)))
		# print ("min index: %s, min value: %s"%(curr.index(min(curr))+1,min(curr)))
		# print ("max index: %s, max value: %s"%(curr.index(max(curr))+1,max(curr)))
		i += 1