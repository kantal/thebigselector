#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# demo2.py

import tkinter as tk
import tkinter.ttk as ttk
import thebigselector as tbs

win= tk.Tk()
win.title("BSB Demo 2")

#--
def cb(box,actn,index):

    s="..."
    if box.selected:

        idx1=  min(box.selected)
        s= box.items[idx1]
        idx2= max(box.selected)
        d= idx2-idx1
        if d == 1:
            s+=", " + box.items[idx2]
        elif d>1:
            s+= " - " + box.items[idx2]

    lbl.config(text=s)

#--
items= [f"item-{i:02}." for i in range(1,31)] + ["Hi", "Szia", "Hello", "Ahoj"]

style= ttk.Style()
style.configure("TBigSelBox.TFrame", borderwidth=10, relief=tk.SUNKEN )

bsb= tbs.BigSelBox(win, items, selections=[0,1,2],
                    frameprops= dict(style="TBigSelBox.TFrame"),
                    textprops=  dict(width=20, padx=5, pady=5, spacing2=5 ),
                    itemprops=  dict(borderwidth=3, relief=tk.RAISED),
                    callback= cb,
                    pickedprops= dict(foreground="white",background="darkgreen") )

bsb.grid(row=0,column=0,columnspan=2,sticky=tk.N+tk.E+tk.S+tk.W)

lbl= tk.Label(text="...")
lbl.grid(row=1,column=0)

cb(bsb,tbs.actnOk,None)

#--
win.columnconfigure(1,weight=1)
win.rowconfigure(0,weight=1)

win.minsize(1024,100)
win.mainloop()

