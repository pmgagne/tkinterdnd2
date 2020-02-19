# -*- coding: utf-8 -*-

import os
import platform
from TkinterDnD2 import *
try:
    from Tkinter import *
    from ScrolledText import ScrolledText
except ImportError:
    from tkinter import *
    from tkinter.scrolledtext import ScrolledText

root = TkinterDnD.Tk()
root.withdraw()
root.title('TkinterDnD megawidget demo')
root.grid_rowconfigure(1, weight=1, minsize=250)
root.grid_columnconfigure(0, weight=1, minsize=300)

Label(root, text='Drop text here:').grid(
                    row=0, column=0, padx=10, pady=5)
buttonbox = Frame(root)
buttonbox.grid(row=2, column=0, columnspan=2, pady=5)
Button(buttonbox, text='Quit', command=root.quit).pack(
                    side=LEFT, padx=5)

msg = 'Dropping onto compound widgets works only with the latest versions ' +\
      'of tkdnd.\nIf you can drop text here, the installed version of ' +\
      'tkdnd already supports this feature.\n'

lf = LabelFrame(root, text='"Megawidget" text box')
lf.grid(row=1, column=0, padx=5, pady=5, sticky='news')
text = ScrolledText(lf)
text.pack(fill='both', expand=1)
text.insert('end', msg)

# make the text box a drop target:

def drop_enter(event):
    event.widget.focus_force()
    print('Entering %s' % event.widget)
    return event.action

def drop_position(event):
    print('Position: x %d, y %d' %(event.x_root, event.y_root))
    return event.action

def drop_leave(event):
    print('Leaving %s' % event.widget)
    return event.action

def drop(event):
    if event.data:
        text.insert('end', event.data)
    return event.action

text.drop_target_register(DND_TEXT)
text.dnd_bind('<<DropEnter>>', drop_enter)
text.dnd_bind('<<DropPosition>>', drop_position)
text.dnd_bind('<<DropLeave>>', drop_leave)
text.dnd_bind('<<Drop>>', drop)

root.update_idletasks()
root.deiconify()
root.mainloop()
