# -*- coding: utf-8 -*-

import os
from TkinterDnD2 import *
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

root = TkinterDnD.Tk()
root.withdraw()
root.title('TkinterDnD Canvas demo')
root.grid_rowconfigure(1, weight=1, minsize=250)
root.grid_columnconfigure(0, weight=1, minsize=300)

Label(root, text='Drag and drop files here:').grid(
                    row=0, column=0, padx=10, pady=5)
buttonbox = Frame(root)
buttonbox.grid(row=2, column=0, columnspan=2, pady=5)
Button(buttonbox, text='Quit', command=root.quit).pack(
                    side=LEFT, padx=5)

file_data = ('R0lGODlhGAAYAKIAANnZ2TMzM////wAAAJmZmf///////////yH5BAEAAAAALAA'
        'AAAAYABgAAAPACBi63IqgC4GiyxwogaAbKLrMgSKBoBoousyBogEACIGiyxwoKgGAECI'
        '4uiyCExMTOACBosuNpDoAGCI4uiyCIkREOACBosutSDoAgSI4usyCIjQAGCi63Iw0ACE'
        'oOLrMgiI0ABgoutyMNAAhKDi6zIIiNAAYKLrcjDQAISg4usyCIjQAGCi63Iw0AIGiiqP'
        'LIyhCA4CBosvNSAMQKKo4ujyCIjQAGCi63Iw0AIGiy81IAxCBpMu9GAMAgKPL3QgJADs'
        '=')
folder_data = ('R0lGODlhGAAYAKECAAAAAPD/gP///////yH+EUNyZWF0ZWQgd2l0aCBHSU1QA'
        'CH5BAEKAAIALAAAAAAYABgAAAJClI+pK+DvGINQKhCyztEavGmd5IQmYJXmhi7UC8frH'
        'EL0Hdj4rO/n41v1giIgkWU8cpLK4dFJhAalvpj1is16toICADs=')

file_icon = PhotoImage(data=file_data)
folder_icon = PhotoImage(data=folder_data)

canvas = Canvas(root, name='dnd_demo_canvas', bg='white', relief='sunken',
                bd=1, highlightthickness=1, takefocus=True, width=600)
canvas.grid(row=1, column=0, padx=5, pady=5, sticky='news')

# store the filename associated with each canvas item in a dictionary
canvas.filenames = {}
# store the next icon's x and y coordinates in a list
canvas.nextcoords = [50, 20]
# add a boolean flag to the canvas which can be used to disable
# files from the canvas being dropped on the canvas again
canvas.dragging = False

def add_file(filename):
    icon = file_icon
    if os.path.isdir(filename):
        icon = folder_icon
    id1 = canvas.create_image(canvas.nextcoords[0], canvas.nextcoords[1],
                                image=icon, anchor='n', tags=('file',))
    id2 = canvas.create_text(canvas.nextcoords[0], canvas.nextcoords[1] + 30,
                                text=os.path.basename(filename), anchor='n',
                                justify='center', width=90)
    def select_item(ev):
        canvas.select_from(id2, 0)
        canvas.select_to(id2, 'end')
    canvas.tag_bind(id1, '<ButtonPress-1>', select_item)
    canvas.tag_bind(id2, '<ButtonPress-1>', select_item)
    canvas.filenames[id1] = filename
    canvas.filenames[id2] = filename
    if canvas.nextcoords[0] > 450:
        canvas.nextcoords = [50, canvas.nextcoords[1] + 80]
    else:
        canvas.nextcoords = [canvas.nextcoords[0] + 100, canvas.nextcoords[1]]

# drop methods

def drop_enter(event):
    event.widget.focus_force()
    print('Entering %s' % event.widget)
    return event.action

def drop_position(event):
    return event.action

def drop_leave(event):
    print('Leaving %s' % event.widget)
    return event.action

def drop(event):
    if canvas.dragging:
        # the canvas itself is the drag source
        return REFUSE_DROP
    if event.data:
        files = canvas.tk.splitlist(event.data)
        for f in files:
            add_file(f)
    return event.action

canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<DropEnter>>', drop_enter)
canvas.dnd_bind('<<DropPosition>>', drop_position)
canvas.dnd_bind('<<DropLeave>>', drop_leave)
canvas.dnd_bind('<<Drop>>', drop)

# drag methods

def drag_init(event):
    data = ()
    sel = canvas.select_item()
    if sel:
        # in a decent application we should check here if the mouse
        # actually hit an item, but for now we will stick with this
        data = (canvas.filenames[sel],)
        canvas.dragging = True
        return ((ASK, COPY), (DND_FILES, DND_TEXT), data)
    else:
        # don't start a dnd-operation when nothing is selected; the
        # return "break" here is only cosmetical, return "foobar" would
        # probably do the same
        return 'break'

def drag_end(event):
    # reset the "dragging" flag to enable drops again
    canvas.dragging = False

canvas.drag_source_register(1, DND_FILES)
canvas.dnd_bind('<<DragInitCmd>>', drag_init)
canvas.dnd_bind('<<DragEndCmd>>', drag_end)

root.update_idletasks()
root.deiconify()
root.mainloop()
