#! /usr/bin/env python3
#-*- coding:utf-8 -*-

# demo0.py

import tkinter as tk
import thebigselector as tbs

win= tk.Tk()
win.title("BSB Demo Zero")
win.columnconfigure(0,weight=1)
win.rowconfigure(0,weight=1)

#--
items= [f"item {i:02}." for i in range(1,31)]
intro= f"\n{tbs.__doc__}\nVersion: {tbs.__version__}\n"

def cb(box,actn,index):
    box.set_compl(f"\nAction: {actn}\nIndex: {index}\nSelected: {box.selected}")

#--
bsb= tbs.BigSelBox(win, items= items, callback= cb, intro= intro, see="items_start")
bsb.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W)
win.minsize(width=400, height=400)
win.mainloop()
