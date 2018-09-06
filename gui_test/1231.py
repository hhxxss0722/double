import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title('SMS_Send')
window.geometry('600x400')


var = tk.StringVar()
# 使用 textvariable 替换 text, 因为这个可以变化
l = tk.Label(window,textvariable=var, bg='green', font=('Arial', 12), width=15, height=2)
l.pack(side = 'left')

on_hit = False  # 默认初始状态为 False
def hit_me():
    global on_hit
    if on_hit == False:     # 从 False 状态变成 True 状态
        on_hit = True
        var.set('you hit me')   # 设置标签的文字为 'you hit me'
    else:       # 从 True 状态变成 False 状态
        on_hit = False
        t.delete(1.0,'end')
        var.set('') # 设置 文字为空

      # 显示在按钮上的文字
b = tk.Button(window,text='hit me',width=15, height=2,command = hit_me)     # 点击按钮式执行的命令
b.pack()    # 按钮位置

t = tk.Text(window, height=2, width=30)
t.insert('end',"Just a text Widget\nin two lines\n")
# t.pack(side = 'bottom')
# result_message = tk.Message(window, bg = 'white',font = ('微软雅黑','12'),width = 20 ,height = 4)
# result_message.pack(side = 'bottom')
# result_message.place(x = 10,y = 300)
# result_label = tk.Text(window, text = var , bg = 'white',font = ('微软雅黑','12'),width = 140,height = 4)
# result_label.place(x = 10,y = 300)
v = tk.StringVar()
lb1 = ttk.Combobox(window,textvariable = var)
lb1['value'] = ('1','2','3','4')
lb1.current(0)
lb1.bind("<<comboboxselected>>",hit_me)
lb1.pack()

window.mainloop()