# coding=utf-8

__all__ = ['main']

import dingbot
try:
    import tkinter as tk
except:
    import Tkinter as tk

def new_robot():
    print('new robot')

win = {'main': tk.Tk('main')}
bar = {'menu': tk.Menu(), 'file': tk.Menu(tearoff = False), 'mesg': tk.Menu(tearoff = False)}
div = {'chos': tk.Frame(master = win['main'], container = True, width = 150, height = 310, bg = 'green'),
       'work': tk.Frame(master = win['main'], container = True, width = 350, height = 310, bg = 'pink'),
       'show': tk.Frame(master = win['main'], container = True, width = 500, height = 20, bg = 'blue')}
div['chos'].place(x=0,y=0)
div['work'].place(x=150,y=0)
div['show'].place(x=0,y=310)

win['main'].geometry('500x330')
win['main'].title('Dingbot GUI')

bar['file'].add_command(label = 'New',      command = new_robot)

bar['mesg'].add_command(label = 'Text',     command = object)
bar['mesg'].add_command(label = 'Markdown', command = object)
bar['mesg'].add_command(label = 'Link',     command = object)

bar['menu'].add_cascade(label = 'Robot',    menu = bar['file'])
bar['menu'].add_cascade(label = 'Message',  menu = bar['mesg'])

win['main'].config(menu = bar['menu'])
win['main'].mainloop()

