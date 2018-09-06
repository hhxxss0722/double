import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title('test')
window.geometry('611x300')
# tk.Label(window,text = 'on the window').pack()
# mainframe = ttk.Frame(window, padding = '3 3 12 12')

# menuBar = tk.Menu(window)
# fileMenu = tk.Menu(menuBar,tearoff = 0)
# menuBar.add_cascade(label = 'File',menu = fileMenu)
# fileMenu.add_command(label = 'New',command = 'do_job')
# # menuBar.pack()

fm = tk.Frame(window,height = 200,width = 200,bg = 'red',border = 2 )
fm.pack_propagate(0)
# fm.pack(side = 'left')
fm_l = tk.Frame(fm,bg = 'red')
fm_r = tk.Frame(fm)
fm_l.pack(side = 'left')
fm_r.pack(side = 'right')
tk.Label(fm_l,text = 'fm1_left',bg = 'blue').pack(side = 'left')
tk.Label(fm_r,text = 'fmright').pack(side = 'right')

for i in range(4):
    for j in range(3):
        if i == 1:
            tk.Label(window, text=str(i) + str(j),bg = 'red').grid(row=i, column=j, padx=10, pady=10)
        else:
            tk.Label(window,text = str(i)+str(j)).grid(row = i,column = j+30,padx = 10, pady = 10)

# screenw = window.winfo_screenwidth()
# screenh = window.winfo_screenheight()
# print(screenh,screenw)
# window.geometry('300x240+533+264')
# print(window.geometry())
window.mainloop()