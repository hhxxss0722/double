#!/usr/bin/python
#coding=utf-8

import tkinter as tk
import tkinter.messagebox
import requests
import time
from tkinter import ttk
import os


text_list = []

def judge_simcard(sim_num,deal_type):
    http_url = ''
    sim_num = sim_num.strip()
    if not sim_num.startswith('1064'):
        tkinter.messagebox.showinfo('提示', '号码不是以1064开头')
    elif len(sim_num)!= 13:
        tkinter.messagebox.showinfo('提示', '号码位数不对')
    elif not sim_num.isdigit():
        tkinter.messagebox.showinfo('提示', '号码必须为纯数字')
    else:
        global temp_text
        temp_text = ''
        if sim_num.startswith('10648'):
            http_url = 'http://114.113.238.158:8000/sms/send?to=' + sim_num + '&message=“' + deal_type + '”&channel=13&key=f97f6b3199904693a9bb951f123bb5c8'
            temp_text = '移动：'
        if sim_num.startswith('10646'):
            http_url = 'http://114.113.238.158:8000/sms/send?to=' + sim_num + '&message=“' + deal_type + '”&channel=18&key=f97f6b3199904693a9bb951f123bb5c8'
            temp_text = '联通：'
        rece_data = requests.get(http_url).text
        rece_data = eval(rece_data)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        temp_text = t +  '  ' + temp_text + str(rece_data)
        result_text.delete(1.0, 'end')
        result_text.insert('end', temp_text)

def set_host():
    global temp_text
    temp_text = ''
    sim_num = text_list[0].get()
    host = text_list[2].get()
    deal_type = 'CS/HOST2/' + host + '/'
    judge_simcard(sim_num,deal_type)

def set_vin():
    global temp_text
    temp_text = ''
    sim_num = text_list[0].get()
    vin_str = text_list[1].get().strip()
    if not vin_str.isalnum():
        tkinter.messagebox.showinfo('提示', 'VIN必须为字母数字组合')
    elif len(vin_str) != 17:
        tkinter.messagebox.showinfo('提示', 'VIN位数不对')
    else:
        deal_type = 'CS/VIN/' + vin_str + '/'
        judge_simcard(sim_num,deal_type)

def upgrade():
    global temp_text
    temp_text = ''
    sim_num = text_list[0].get()
    deal_type = 'CS/UPDATE'
    judge_simcard(sim_num, deal_type)

def init_control():
    button_list = ['upgrade','set_vin','set_host']
    l_list = ['SIM:','VIN:','IP&Port:']
    t_list = ['1064808779699','LA678M1E5GKLW3276','124.207.149.200:5002']
    for i in range(3):
        l_lable = tk.Label(window, text=l_list[i], bg='white', font=('微软雅黑', '12'), width=8, height=1)
        t_button = tk.Button(window,text = button_list[i], width = 8,height = 1,command = eval(button_list[i]))
        t_text = tk.Entry(window, bg = 'white', font=('微软雅黑', '12'), width=20)
        l_lable.place(x = 10, y = 10 + 100 * i )
        t_button.place(x = 400, y = 10 + 100 * i )
        t_text.place(x = 150, y = 10 + 100 * i)
        t_text.insert('end', t_list[i])
        text_list.append(t_text)

if __name__ == '__main__':
    window = tk.Tk()
    window.title('SMS_Send')
    window.geometry('600x400')
    result_text = tk.StringVar()
    temp_text = ''
    init_control()
    result_text = tk.Text(window, bg='white', font=('微软雅黑', '12'), width=50, height=4)
    result_text.pack(side='bottom')
    comValue = tkinter.StringVar()
    comBoxlist = ttk.Combobox(window,textvariable = comValue)

    myPath = os.path.dirname(__file__)
    print(myPath)


    window.mainloop()