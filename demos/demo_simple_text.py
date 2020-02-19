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
root.title('TkinterDnD simple text demo')
root.grid_rowconfigure(1, weight=1, minsize=250)
root.grid_columnconfigure(0, weight=1, minsize=300)

Label(root, text='Drag and drop text here:').grid(
                    row=0, column=0, padx=10, pady=5)
buttonbox = Frame(root)
buttonbox.grid(row=2, column=0, columnspan=2, pady=5)
Button(buttonbox, text='Quit', command=root.quit).pack(
                    side=LEFT, padx=5)

msg = "You can drop text onto the Label to append it to the Label's text "+\
      "string.\nYou can drag the Label's text string into other " +\
      "applications.\n"
label = Label(root, name='dnd_demo_label', bg='white', relief='sunken',
                bd=1, highlightthickness=1, text=msg, takefocus=True,
                justify='left', anchor='nw', padx=5, pady=5)
label.grid(row=1, column=0, padx=5, pady=5, sticky='news')

# make the Label a drop target:

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
        label.configure(text=label['text'] + event.data)
    return event.action

label.drop_target_register(DND_TEXT)
label.dnd_bind('<<DropEnter>>', drop_enter)
label.dnd_bind('<<DropPosition>>', drop_position)
label.dnd_bind('<<DropLeave>>', drop_leave)
label.dnd_bind('<<Drop>>', drop)

# make the Label a drag source:

def drag_init(event):
    data = label['text']
    return (COPY, DND_TEXT, data)

label.drag_source_register(DND_TEXT)
label.dnd_bind('<<DragInitCmd>>', drag_init)

root.update_idletasks()
root.deiconify()
root.mainloop()



