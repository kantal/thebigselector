#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# toplevel_demo.py

import tkinter as tk
import tkinter.scrolledtext
import thebigselector as tbs
import sys,string

class TestFrame(tk.Frame):

    def __init__(self,parent,items,separators={},sepprops={},selections=[],
                 intro=" ", introprops={}, compl=" ", complprops={},
                  **frm_kwargs):

        super().__init__(parent,**frm_kwargs)

        self.tw= None
        self.parent= parent
        self.items= items
        self.selections= selections
        self.separators= separators
        self.sepprops= sepprops
        self._intro= intro
        self.introprops= introprops
        self._compl= compl
        self.complprops= complprops

        self.stext= tkinter.scrolledtext.ScrolledText(parent)
        self.btnStartSelection= tk.Button(parent,text="Select", command= self.__showSelector)

        self.stext.grid(row=0,column=0,columnspan=2,sticky=tk.N+tk.E+tk.S+tk.W)
        self.btnStartSelection.grid(row=1,column=0)

        self.tw_width,self.tw_height=600,200

        self.stext.insert("end", "** BigSelBox Toplevel Demo **\n\n")

    #--
    def __selectionCallback(self,box,actn,index):
        # The callback function for the BSB in the top level window

        if actn == tbs.actnCancel:
            self.stext.insert("end","< canceled >\n")

        elif actn != tbs.actnOk:
            return

        sels= box.selected
        if sels:

            self.stext.insert("end", " ".join(box.items[i] for i in sels)+"\n")
        else:
            self.stext.insert("end","< no selection >\n")

        self.stext.insert("end","---\n")
        self.stext.see("end -3c")
        self.tw.destroy()
        self.tw=None

    #--
    def __showSelector(self):
        # Show a top level window with the selector
        if self.tw:
            self.tw.deiconify()
            self.tw.lift()
        else:
            self.tw= tbs.TopBSB(self.parent, self.items, separators= self.separators,
                            sepprops= self.sepprops, selections= self.selections,
                            callback= self.__selectionCallback,
                            intro= self._intro, introprops= self.introprops,
                            compl= self._compl, complprops= self.complprops
                            )
            self.tw.title("Items")
            # Place the window above the 'Select' button
            self.tw.geometry(f"{self.tw_width}x{self.tw_height}+" \
                             f"{self.btnStartSelection.winfo_rootx()}+"
                             f"{self.btnStartSelection.winfo_rooty()}" )

        self.tw.minsize(width=self.tw_width,height=self.tw_height)

#--
win= tk.Tk()
win.rowconfigure(0,weight=1)
win.columnconfigure(0,weight=1)
win.title("Toplevel BSB Test")

#-- test data:
chs= string.whitespace + string.punctuation
tbl= str.maketrans(chs," "*len(chs))
with open(sys.argv[0]) as ff:
        items= sorted(set(ff.read().translate(tbl).split()), key=str.lower)

separ={}
prch=""
for index,s in enumerate(items):

    ch=s[0].lower()
    if ch!=prch and not ch.isdigit():
        separ[index]= f" {ch}{ch.upper()} "
        prch= ch

sepprops= {"foreground":"orange","underline":"1"}
#--
fr= TestFrame(win, items, separators=separ, sepprops=sepprops)
fr.grid()

win.mainloop()

