#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# demo3.py

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
import thebigselector as tbs

STRECH= tk.N+tk.E+tk.S+tk.W

win= tk.Tk()
win.title("BSB Demo 3")

#--
# callback for bsb1
def cb1(box,actn,index,tbox):
        # actn and index not used
        tbox.set_items([box.items[i].upper() for i in box.selected])

#--
# callback for bsb2
def cb2(box,actn,index,tbox):

    if actn == tbs.actnOk:
        its= [box.items[i].lower() for i in box.selected]
        tbox.set_items(its, selections= range(len(its))[1:-1])
        box.set_intro(f"{box.intro.rstrip()} {len(tbox.items)}\n")

    elif actn == tbs.actnCancel:
        box.set_items([])

#--
# callback for bsb3
def cb3(box,actn,index,tbox):

    if actn == tbs.actnOk:
        its= [box.items[i] for i in box.selected]
        tbox.set_items([s for s in tbox.items if s.lower() not in its])

    elif actn == tbs.actnCancel:
        box.set_items([])

#--
items= ["Szia", "Hello", "Ahoj", "Grüss dich", "Здравствуй", "Hi", "Szevasz", "Hali"]

style= ttk.Style()
style.configure("TBigSelBox.TFrame", background="#443831", padding=5)
frameprops= {"style":"TBigSelBox.TFrame"}
pfont= tkfont.Font(family="Helvetica", slant="italic", overstrike=1)

bsb1= tbs.BigSelBox(win, items, selections=[0,1,2],
                frameprops= frameprops,
                textprops= dict(width=20,padx=5,pady=5,spacing2=5),
                pickedprops= dict(background="red", foreground="yellow"),
                itemprops= dict(borderwidth=2,relief=tk.RAISED)
                )

bsb2= tbs.BigSelBox(win, items=[], frameprops= frameprops,
                    pickedprops= dict(background="white", foreground="#3878ff"))

bsb3= tbs.BigSelBox(win, items=[], frameprops= frameprops,
                    pickedprops= dict(font=pfont) )

bsb1["callback"]= lambda box,actn,index: cb1(box,actn,index,tbox=bsb2)
bsb1.disable_button("ok")
bsb1.disable_button("cancel")

bsb2["callback"]= lambda box,actn,index: cb2(box,actn,index,tbox=bsb3)
bsb3["callback"]= lambda box,actn,index: cb3(box,actn,index,tbox=bsb1)

bsb1.grid(row=0,column=0,sticky=STRECH)
bsb2.grid(row=0,column=1,sticky=STRECH)
bsb3.grid(row=0,column=2,sticky=STRECH)

cb1(bsb1,None,None,bsb2)

#--
win.columnconfigure(0,weight=1)
win.rowconfigure(0,weight=1)

tbs.fix_minsize(win)
win.mainloop()

