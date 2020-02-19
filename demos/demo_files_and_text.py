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
root.title('TkinterDnD demo')
root.grid_rowconfigure(1, weight=1, minsize=250)
root.grid_columnconfigure(0, weight=1, minsize=300)
root.grid_columnconfigure(1, weight=1, minsize=300)

def print_event_info(event):
    print('\nAction:', event.action)
    print('Supported actions:', event.actions)
    print('Mouse button:', event.button)
    print('Type codes:', event.codes)
    print('Current type code:', event.code)
    print('Common source types:', event.commonsourcetypes)
    print('Common target types:', event.commontargettypes)
    print('Data:', event.data)
    print('Event name:', event.name)
    print('Supported types:', event.types)
    print('Modifier keys:', event.modifiers)
    print('Supported source types:', event.supportedsourcetypes)
    print('Operation type:', event.type)
    print('Source types:', event.sourcetypes)
    print('Supported target types:', event.supportedtargettypes)
    print('Widget:', event.widget, '(type: %s)' % type(event.widget))
    print('X:', event.x_root)
    print('Y:', event.y_root, '\n')

Label(root, text='Drag and drop files here:').grid(
                    row=0, column=0, padx=10, pady=5)
Label(root, text='Drag and drop text here:').grid(
                    row=0, column=1, padx=10, pady=5)
buttonbox = Frame(root)
buttonbox.grid(row=2, column=0, columnspan=2, pady=5)
Button(buttonbox, text='Quit', command=root.quit).pack(
                    side=LEFT, padx=5)

##############################################################################
######   Basic demo window: a Listbox to drag & drop files                  ##
######   and a Text widget to drag & drop text                              ##
##############################################################################
listbox = Listbox(root, name='dnd_demo_listbox',
                    selectmode='extended', width=1, height=1)
listbox.grid(row=1, column=0, padx=5, pady=5, sticky='news')
text = Text(root, name='dnd_demo_text', wrap='word', undo=True, width=1, height=1)
text.grid(row=1, column=1, pady=5, sticky='news')

listbox.insert(END, os.path.abspath(__file__))
info = 'TkinterDnD demo\nDetected versions:\n'
info += '    Python: %s\n' % platform.python_version()
info += '    Tk    : %f\n' % TkVersion
info += '    Tkdnd : %s\n' % TkinterDnD.TkdndVersion
info += 'Use mouse button 3 to drag hightlighted text from the text box.\n'
text.insert(END, info)

# Drop callbacks can be shared between the Listbox and Text;
# according to the man page these callbacks must return an action type,
# however they also seem to work without

def drop_enter(event):
    event.widget.focus_force()
    print('Entering widget: %s' % event.widget)
    #print_event_info(event)
    return event.action

def drop_position(event):
    print('Position: x %d, y %d' %(event.x_root, event.y_root))
    #print_event_info(event)
    return event.action

def drop_leave(event):
    print('Leaving %s' % event.widget)
    #print_event_info(event)
    return event.action

def drop(event):
    if event.data:
        print('Dropped data:\n', event.data)
        #print_event_info(event)
        if event.widget == listbox:
            # event.data is a list of filenames as one string;
            # if one of these filenames contains whitespace characters
            # it is rather difficult to reliably tell where one filename
            # ends and the next begins; the best bet appears to be
            # to count on tkdnd's and tkinter's internal magic to handle
            # such cases correctly; the following seems to work well
            # at least with Windows and Gtk/X11
            files = listbox.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f)
                    listbox.insert('end', f)
                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        elif event.widget == text:
            # calculate the mouse pointer's text index
            bd = text['bd'] + text['highlightthickness']
            x = event.x_root - text.winfo_rootx() - bd
            y = event.y_root - text.winfo_rooty() - bd
            index = text.index('@%d,%d' % (x,y))
            text.insert(index, event.data)
        else:
            print('Error: reported event.widget not known')
    return event.action

# now make the Listbox and Text drop targets
listbox.drop_target_register(DND_FILES, DND_TEXT)
text.drop_target_register(DND_TEXT)

for widget in (listbox, text):
    widget.dnd_bind('<<DropEnter>>', drop_enter)
    widget.dnd_bind('<<DropPosition>>', drop_position)
    widget.dnd_bind('<<DropLeave>>', drop_leave)
    widget.dnd_bind('<<Drop>>', drop)
    #widget.dnd_bind('<<Drop:DND_Files>>', drop)
    #widget.dnd_bind('<<Drop:DND_Text>>', drop)

# define drag callbacks

def drag_init_listbox(event):
    print_event_info(event)
    # use a tuple as file list, this should hopefully be handled gracefully
    # by tkdnd and the drop targets like file managers or text editors
    data = ()
    if listbox.curselection():
        data = tuple([listbox.get(i) for i in listbox.curselection()])
        print('Dragging :', data)
    # tuples can also be used to specify possible alternatives for
    # action type and DnD type:
    return ((ASK, COPY), (DND_FILES, DND_TEXT), data)

def drag_init_text(event):
    print_event_info(event)
    # use a string if there is only a single text string to be dragged
    data = ''
    sel = text.tag_nextrange(SEL, '1.0')
    if sel:
        data = text.get(*sel)
        print('Dragging :\n', data)
    # if there is only one possible alternative for action and DnD type
    # we can also use strings here
    return (COPY, DND_TEXT, data)

def drag_end(event):
    #print_event_info(event)
    # this callback is not really necessary if it doesn't do anything useful
    print('Drag ended for widget:', event.widget)

# finally make the widgets a drag source

listbox.drag_source_register(1, DND_TEXT, DND_FILES)
text.drag_source_register(3, DND_TEXT)

listbox.dnd_bind('<<DragInitCmd>>', drag_init_listbox)
listbox.dnd_bind('<<DragEndCmd>>', drag_end)
text.dnd_bind('<<DragInitCmd>>', drag_init_text)
# skip the useless drag_end() binding for the text widget

root.update_idletasks()
root.deiconify()
root.mainloop()

