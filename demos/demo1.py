#! /usr/bin/env python3
#-*- coding:utf-8 -*-

# demo1.py

import tkinter as tk
import tkinter.font as tkfont
import thebigselector as tbs

win= tk.Tk()
win.title("BSB Demo 1")
win.columnconfigure(0,weight=1)
win.rowconfigure(0,weight=1)
#--

items= [f"item {i:02}." for i in range(1,31)]

intro= f"\n{tbs.__doc__}\nVersion: {tbs.__version__}\n"

Actns={tbs.actnOk:"Ok", tbs.actnCancel:"Cancel", tbs.actnSelect:"Select item",
        tbs.actnUnselect:"Unselect item", tbs.actnSelectAll:"Select all",
        tbs.actnUnselectAll:"Unselect all",
        tbs.actnSelectSeparator: "Select group separator",
        tbs.actnUnselectSeparator:"Unselect group separator"}

#--
def cb(box,actn,index):

    l= [ (i,box.items[i]) for i in box.selected ]
    sactn= clicked= Actns[actn]
    if index!=None:
        if actn in (tbs.actnSelect, tbs.actnUnselect):
            clicked= box.items[index]
        else:
            clicked= box.separators[index].replace("\n"," ")

    box.set_compl(f"\n\n\U0001f408\nAction: {sactn}\nIndex: {index}\n"
                  f"Clicked: {clicked}\nSelection: {l}")

#--
dmargos= dict(lmargin1=5,lmargin2=5)
font= tkfont.Font(family="Helvetica",size=12, slant="italic")

bsb= tbs.BigSelBox(win, items= items, selections= [0,9,19,29],
                separators= {0:"--1--",9:"\n--10--\n(tens)",19:"--20--",29:"\n--30--"},
                sepprops= dict(foreground="#e45c09",underline="1"),
                callback= cb,
                intro= intro,
                introprops= dict(background="#ccc39c", **dmargos),
                complprops= dict(foreground="green", font=font, **dmargos),
                textprops= dict(background="lightgray", foreground="black"),
                itemprops= dmargos,
                pickedprops= dict(foreground="white", background="#3160e6"),
                see="items_start"
                )

#--
bsb.grid(row=0,column=0,sticky=tk.N+tk.E+tk.S+tk.W)
win.minsize(width=700, height=800)

cb(bsb,tbs.actnOk,None)
win.mainloop()
