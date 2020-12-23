
# THE BIG SELECTOR BOX

## A Tkinter text widget based option selector

Copyright (c) 2020, Antal Koós \
License: MIT

____


 ![ ](screenshot-1.png)
 ![ ](screenshot-2.png)

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


See the [demos](https://github.com/kantal/thebigselector/tree/main/demos) for the details!

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

