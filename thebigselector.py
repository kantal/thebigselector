#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""THE BIG SELECTOR BOX
====================

## A Tkinter text widget based option selector
____

Copyright (C) 2020, Antal Koós \
License: MIT

#### Use

mouse buttons on item:

- left: selects/unselects the item

mouse buttons on group separator:

- left: selects all items in the group
- right: unselects all items in the group

Selecting with dragging the mouse and clicking on "Select/Unselect all"
acts only on the selected items.


    import tkinter as tk
    import thebigselector as tbs
        ...
    bsb= tbs.BigSelBox(win, items= items, callback= cb, intro= intro, see="items_start")
        ...


See the demos for details!

\
\

### BigSelBox
___

BigSelBox is an option selector, derived from ttk.Frame and contains a tk.Text widget
associated with a vertical ttk.Scrollbar.


    BigSelBox(  master, items=[], selections=[], callback=None,
                separators={}, sepprops={}, textprops={},
                frameprops={}, itemprops={},
                pickedprops={}, intro=" ", introprops={},
                compl=" ", complprops={}, see=None)


#### Args:

- master: the master widget
- items: sequence of strings; whitespaces will be replaced with '_'
- selections: indexes of initially selected items
- textprops: dict, text widget properties
- frameprops: dict, main frame (ttk.Frame) properties
- itemprops: dict, item text (tag) properties
- pickedprops: dict, text (tag) properties of selected items
- callback: called by clicking on an item or group separator or button with these arguments:

    - the BigSelBox instance
    - the trigger action that can be:

      - actnOk, actnCancel,
      - actnSelect, actnUnselect,
      - actnSelectAll, actnUnselectAll,
      - actnSelectSeparator, actnUnselectSeparator

    - the index of the selected/unselected item/group separator, or None in case of pressing "Ok", "Select", "Unselect all", "Cancel"

- separators: dict with `index:separator_string` pairs, where `index` is the index of the item before the string must be inserted.
- sepprops: dict, separator (tag) properties
- intro: introductory text string
- introprops: dict, introductory text (tag) properties
- compl: completion text after the item section
- complprops: dict, completion text (tag) properties
- see: a text widget index for scroll the text until the part on that position is visible. \
 Special indexes:

  - Marks: "intro_start", "intro_end", "items_start", "items_end",
            "compl_start", "compl_end"
  - Tags: "#5.first": the 6th item, "$5.first": the 6th group separator

- pickedcolors: (foreground, background) colors of the selected items

#### Attributes:

- *items (ro)*: tuple of strings; whitespaces will be replaced with '_'
- *selected (ro)*: index of selected items
- *intro (ro)*: introductory text
- *compl (ro)*: completion text

The callback can be set two ways, e.g.: `sb.callback=cb` or `sb["callback"]=cb`

#### Methods:

*set_items(items,selections=[], see=None)*: sets the items.

- items: sequence of strings; whitespaces will be replaced with '_'
- selections: indexes of initially selected items
- see: a text widget index

*set_selections(selections, see=None)*: sets the selections.

- selections: indexes of initially selected item
- see: a text widget index

*set_intro(txt, see=None)*: sets the introductory text.

- txt: the text
- see: a text widget index

*set_compl(txt, see=None)*: sets the completion text.

- txt: the text
- see: a text widget index

*see(self,index)*: scrolls the text until the part on that position is visible.

*disable_button(btnstr)*: disables/enables a button. \
*enable_button(btnstr)*: disables/enables a button.

- btnstr can be "ok", "cancel", "select all", "unselect all"

\
\

### TopBSB
___

A Tkinter top level window class with a 'BigSelBox' inside.


    TopBSB(parent, items=[], selections=[], callback=None,
        separators={}, sepprops={}, textprops={},
        frameprops={}, itemprops={},
        pickedprops={}, intro="", introprops={},
        compl="", complprops={},
        **toplevel_kwargs)


#### Args:

- parent: the parent window
- toplevel_kwargs: tk.Toplevel window attributes

The other args will be passed to the inner BigSelBox instance. \
When the window is destroyed, the callback also will be called with `(box, actnCancel, None)`.

\
\

### Module utilities
___

*geom(wdg)*: returns the widget's geometry values as ints: `(width, height, x, y)`.

*fix_minsize(wdg)*: freezes the widget size to the recommended minimal size.

"""

__version__= "1.0"
_DEBUG= False

import tkinter as tk
from tkinter import ttk
import string

actnOk, actnCancel, actnSelect, actnUnselect="OCSU"
actnSelectAll="SAll"
actnUnselectAll="UAll"
actnSelectSeparator="SSep"
actnUnselectSeparator="USep"

#--
class BigSelBox(ttk.Frame):

    def __init__(self, master,items=[], selections=[], callback=None,
                 separators={}, sepprops={}, textprops={}, frameprops={},
                 itemprops={}, pickedprops={}, intro=" ", introprops={},
                 compl=" ", complprops={}, see=None):

        super().__init__(master, **frameprops)

        self.callback= callback
        self.separators= separators
        self.sepprops= sepprops
        self._intro= intro
        self.introprops= introprops
        self._compl= compl
        self.complprops= complprops
        self.itemprops= itemprops
        self.pickedprops= pickedprops

        self.tag_selected= "selected"
        self.tag_separator= "sepa"
        self.tag_item= "item"

        textprops.setdefault("width",20)
        textprops.setdefault("height",5)
        textprops.setdefault("cursor","arrow")
        textprops["wrap"]= tk.WORD

        self._stext= tk.Text(self, **textprops)
        self._vscr= ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._stext.yview)
        self._stext['yscrollcommand']= self._vscr.set

        self._stext.grid(row=0,column=0, columnspan=5, sticky=tk.N+tk.E+tk.S+tk.W)
        self._vscr.grid(row=0, column=5, sticky=tk.N+tk.S)
        self.columnconfigure(4,weight=1)
        self.rowconfigure(0,weight=1)

        if "foreground" not in pickedprops:
            pickedprops["foreground"]= self._stext["selectbackground"]
        if "background" not in pickedprops:
            pickedprops["background"]= self._stext["selectforeground"]

        self._stext.tag_config(self.tag_selected, **pickedprops)

        for m1,m2 in [("intro_start","intro_end"), ("items_start","items_end"), ("compl_start","compl_end")]:

            self._stext.insert("end","\n")
            self._stext.mark_set(m1,"insert-1c")
            self._stext.mark_set(m2,"insert-1c")
            self._stext.mark_gravity(m1,tk.LEFT)
            self._stext.mark_gravity(m2,tk.RIGHT)

        #--
        self.set_intro(self._intro)
        self.set_items(items,selections)
        self.set_compl(self._compl, see)

        #--
        self.btn_Clear= ttk.Button(self,text="Unselect all", command=self.__cb_btnClearAll)
        self.btn_Clear.grid(row=1,column=0)
        self.btn_All= ttk.Button(self,text="Select all", command=self.__cb_btnSetAll)
        self.btn_All.grid(row=1,column=1)
        self.btn_Cancel= ttk.Button(self,text="Cancel", command=self.__cb_btnCancel)
        self.btn_Cancel.grid(row=1,column=2)
        self.btn_Ok= ttk.Button(self,text="Ok", command=self.__cb_btnOk)
        self.btn_Ok.grid(row=1,column=3)

        self.btndict={"ok":self.btn_Ok, "cancel":self.btn_Cancel,
                      "select all":self.btn_All, "unselect all":self.btn_Clear }

    #--
    def __check_selections(self,sels):

        if any(i not in range(len(self._items)) for i in sels):
                raise IndexError ("Invalid selection index")

    #--
    def set_items(self, items, selections=[], see=None):
        """
        items: the list of item texts
        selections: indices of initially selected items
        """
        self._items_selected= []

        tbl= str.maketrans(string.whitespace,"_"*len(string.whitespace))
        self._items= tuple( it.strip().translate(tbl) for it in items )

        self.__check_selections(selections)

        """
        separator tags if any: ( "sepa", "$"+str(separator_index) )
            separator index is unique, e.g.: ("sepa","$9")

        item tags: ("item", "#"+str(index in self._items),
                    "$$"+ str(separator index), "selected" )
            e.g.: ("item","#12","$$9","") the first two always exist
        """

        self._stext["state"]="normal"
        self._stext.delete("items_start","items_end")

        self._stext.mark_set(tk.INSERT,"items_start")
        seppos=None
        for idx,itm in enumerate(self._items):

            # insert separator tag if any required
            sep= self.separators.get(idx,None)
            if sep!=None:   # insert separator
                seppos= idx
                tgsp= (self.tag_separator, f"${seppos}")   # ("sepa","$1")
                self._stext.insert(tk.INSERT,"\n")

                # possible whitespaces at the ends of the separator string inserted separately, "\n\n group 1. \n\n"
                l1= len(sep)-len(sep.lstrip())
                l2= len(sep.rstrip())
                if l1:
                    self._stext.insert(tk.INSERT,sep[:l1])

                self._stext.insert(tk.INSERT, sep[l1:l2], (tgsp))

                if l2!=len(sep):
                    self._stext.insert(tk.INSERT,sep[l2:])

                self._stext.insert(tk.INSERT,"\n")
                if _DEBUG:
                    print(f"{sep}: {tgsp}")

            # insert item:
            tags= self.tag_item, f"#{idx}"
            if seppos!=None:
                tags= (*tags, f"$${seppos}")

            if idx in set(selections):
                tags= (*tags,self.tag_selected)
                self._items_selected.append(idx)

            self._stext.insert(tk.INSERT, itm, tags)
            self._stext.insert(tk.INSERT," ")
            if _DEBUG:
                print(f"{itm}: {tags}")

        # select:
        self._stext.tag_bind(self.tag_separator,"<Button-1>",self.__cb_sep_selection)
        # unselect:
        self._stext.tag_bind(self.tag_separator,"<Button-3>",self.__cb_sep_selection)

        self._stext.tag_bind(self.tag_item, "<Button-1>", self.__cb_item_selection)

        if self.sepprops:
            self._stext.tag_config(self.tag_separator,**self.sepprops)
        if self.itemprops:
            self._stext.tag_config(self.tag_item,**self.itemprops)

        self._stext["state"]="disabled"

        if see:
            self.see(see)

    #--
    def __get_item_textindexes(self,lico):

        line,col= lico.split('.')
        lstart, lend= f"{line}.0", f"{line}.end"

        # search wraps around if stopindex not given
        lc1= self._stext.search("\s", lico, backwards=True, regexp=True, stopindex=lstart) or lstart
        if lc1!=lstart:
            lc1+= "+1c" # skip the starting whitespace

        lc2= self._stext.search("\s|$", lico, regexp=True, stopindex=lend)
        # as the second index is an exclusive one, not correction is required

        return lc1,lc2

    #--
    def __get_item_index(self, tags):
        return int([t for t in tags if t.startswith("#")][0][1:])

    #--
    def __select(self, tags, i1,i2):

        index= self.__get_item_index(tags)

        if  self.tag_selected in tags:

            self._stext.tag_remove(self.tag_selected, i1,i2)
            self._items_selected.remove(index)
            actn= actnUnselect
        else:
            self._stext.tag_add(self.tag_selected, i1,i2)
            self._items_selected.append(index)
            actn= actnSelect

        return actn,index

    #--
    def __cb_item_selection(self,event):
        # tags: ("item","#12","$$9","selected")

        # calculate 'line.column' position of the click
        lico= self._stext.index(f"@{event.x},{event.y}")
        i1,i2= self.__get_item_textindexes(lico)
        # get the tag names associated with that text
        tags= self._stext.tag_names(lico)

        actn,index= self.__select(tags,i1,i2)

        if self.callback:
            self.callback(self, actn,index)

    #--
    def __cb_btnOk(self):

        if self.callback:
            self.callback(self, actnOk,None)


    def __cb_btnClearAll(self):

        try:
            sel1,sel2= self._stext.index(tk.SEL_FIRST), self._stext.index(tk.SEL_LAST)

        except tk.TclError: # no dragging selection
            # all items will be unselected:
            self._items_selected=[]
            self._stext.tag_delete(self.tag_selected)
            # After deleting a tag, its configuration also will be lost
            self._stext.tag_config(self.tag_selected, **self.pickedprops)

        else: # dragging selection
            item_tag_pos= self._stext.tag_ranges(self.tag_item)
            tx= self._stext.compare
            for i1,i2 in zip(item_tag_pos[0::2],item_tag_pos[1::2]):

                if tx(i1,">=",sel1) and tx(i1,"<",sel2):

                    self._stext.tag_remove(self.tag_selected,i1,i2)
                    index= self.__get_item_index(self._stext.tag_names(i1))

                    # Remove the new selections from the `selected_items`
                    if index in self._items_selected:
                        self._items_selected.remove(index)

        if self.callback:
            self.callback(self, actnUnselectAll,None)


    def __cb_btnSetAll(self):

        item_tag_pos= self._stext.tag_ranges(self.tag_item)

        try:
            sel1,sel2= self._stext.index(tk.SEL_FIRST), self._stext.index(tk.SEL_LAST)

        except tk.TclError: # no dragging selection
            # all items will be selected:
            self._items_selected= list(range(len(self._items)))

            for i1,i2 in zip(item_tag_pos[0::2],item_tag_pos[1::2]):
                self._stext.tag_add(self.tag_selected,i1,i2)

        else:   # dragging selection
            tx= self._stext.compare
            for i1,i2 in zip(item_tag_pos[0::2],item_tag_pos[1::2]):

                if tx(i1,">=",sel1) and tx(i1,"<",sel2):

                    self._stext.tag_add(self.tag_selected,i1,i2)
                    index= self.__get_item_index(self._stext.tag_names(i1))

                    # Append the new selections to the `selected_items` preserving the position of the earlier selected ones
                    if index not in self._items_selected:
                        self._items_selected.append(index)

        if self.callback:
            self.callback(self, actnSelectAll,None)


    def __cb_btnCancel(self):

        if self.callback:
            self.callback(self, actnCancel,None)

    #--
    def __cb_sep_selection(self,event):

        # calculate 'line.column' position of the click
        lico= self._stext.index(f"@{event.x},{event.y}")
        # get the tag names associated with that separator
        septags= self._stext.tag_names(lico)
        stg= [t for t in septags if t.startswith("$")][0]
        itmtag= "$"+ stg    # $12 -->$$12

        tgrngs= self._stext.tag_ranges(itmtag)
        z= zip(tgrngs[0::2],tgrngs[1::2])

        if event.num==3: # unselect

            for p1,p2 in z:

                tags= self._stext.tag_names(p1)
                index= int([t for t in tags if t.startswith("#")][0][1:])

                if self.tag_selected in tags:

                    self._stext.tag_remove(self.tag_selected, p1,p2)
                    self._items_selected.remove(index)

            actn= actnUnselectSeparator

        elif event.num==1:  # select

            for p1,p2 in z:

                tags= self._stext.tag_names(p1)
                index= int([t for t in tags if t.startswith("#")][0][1:])

                if self.tag_selected not in tags:

                    self._stext.tag_add(self.tag_selected, p1,p2)
                    self._items_selected.append(index)

            actn= actnSelectSeparator

        if self.callback:
            self.callback(self, actn, int(stg[1:]))

    #--
    def set_selections(self,selections, see=None):

        self.__check_selections(selections)
        self.__cb_btnClearAll()
        for idx in selections:

            itmtag= f"#{idx}"
            i1,i2= self._stext.tag_nextrange(itmtag,"intro_start")
            self.__select([itmtag],i1,i2)

        if see:
            self.see(see)

    #--
    def set_intro(self,txt, see=None):

        self._intro= txt or " "

        entry_state= self._stext["state"]
        if entry_state == "disabled":
            self._stext["state"]= "normal"

        self._stext.delete("intro_start","intro_end")

        self._stext.insert("intro_start", self._intro, ("intro"))
        if self.introprops:
            self._stext.tag_config("intro",**self.introprops)

        if entry_state == "disabled":
            self._stext["state"]= "disabled"

        if see:
            self.see(see)

    #--
    def set_compl(self,txt, see=None):

        self._compl= txt or " "

        entry_state= self._stext["state"]
        if entry_state == "disabled":
            self._stext["state"]= "normal"

        self._stext.delete("compl_start","compl_end")

        self._stext.insert("compl_start",self._compl,("compl"))
        if self.complprops:
            self._stext.tag_config("compl",**self.complprops)

        if entry_state == "disabled":
            self._stext["state"]= "disabled"

        if see:
            self.see(see)

    #--
    def enable_button(self, btn):
        self.btndict[btn.lower()]["state"]="normal"

    def disable_button(self, btn):
        self.btndict[btn.lower()]["state"]="disabled"

    #--
    def see(self,index):
        """Scroll the text to make the indexed part visible"""
        self._stext.see(index)

    #--
    def __getitem__(self,index):

        if index=="callback":
            return self.callback
        return super().__getitem__(index)

    def __setitem__(self,index,value):

        if index=="callback":
            self.callback= value
        else:
            super().__setitem__(index,value)

    #--
    @property
    def items(self):
        return self._items  # tuple

    @property
    def selected(self):
        return self._items_selected[:] # list

    @property
    def intro(self):
        return self._intro  # str

    @property
    def compl(self):
        return self._compl  # str

#-----
class TopBSB(tk.Toplevel):

    def __init__(self,parent, items=[], selections=[], callback=None,
                 separators={}, sepprops={}, textprops={}, frameprops={},
                 itemprops={}, pickedprops={}, intro="", introprops={},
                 compl="", complprops={}, **toplevel_kwargs):
        """A top level window class with a 'BigSelBox' inside"""

        super().__init__(parent,**toplevel_kwargs)

        self.bsb= BigSelBox(self, items, selections, callback,
                            separators, sepprops, textprops, frameprops,
                            itemprops, pickedprops, intro, introprops,
                            compl, complprops)

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.bsb.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        self.transient(parent)

        if callback:
            self.protocol("WM_DELETE_WINDOW", lambda: callback(self.bsb,actnCancel,None) )

#----------
# Utilities

def geom(wdg):

    wdg.update_idletasks()
    whxy= wdg.winfo_geometry().partition("x")
    return tuple(map(int,[whxy[0],*whxy[2].split("+")]))

def fix_minsize(wdg):

    width,height,x,y= geom(wdg)
    wdg.minsize(width=width, height=height)
    return width,height
#--



