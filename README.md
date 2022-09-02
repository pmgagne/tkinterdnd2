## fork

this is fork of [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) which is a python wrapper for [tkdnd](https://github.com/petasis/tkdnd)
.

this repo forked and edited to be published to pypi so one could simply install this package
with  `pip install tkinterdnd2`.

## install

`python -m pip install tkinterdnd2`

## usage

```python
import tkinter as tk

from tkinterdnd2 import DND_FILES, TkinterDnD

root = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()

lb = tk.Listbox(root)
lb.insert(1, "drag files to here")

# register the listbox as a drop target
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', lambda e: lb.insert(tk.END, e.data))

lb.pack()
root.mainloop()
```
![tkinterdnd2 example usage](https://i.stack.imgur.com/jnOWd.png)


see any of the [demos](./demos) for usage examples.

# tkinterdnd2

Tkinter native drag and drop support for windows, unix and Mac OSX.

## What is TkInterDnD2

[TkinterDnD2](http://tkinterdnd.sourceforge.net) is a python wrapper for George Petasis' tkDnD Tk extension version 2.

It is a domain public project.

## What is TkDnD2

[tkDnD2](https://github.com/petasis/tkdnd) is a tcl/Tk extension adding native drag and drop support.

## What this repository is about

It package TkinterDnD2 and tkdnd2 into a standard python module.

When the extension is imported in python its location will be automatically added to the Tk search path.

In this project we use the pre-compiled release
from https://github.com/petasis/tkdnd/releases/tag/tkdnd-release-test-v2.9.2 and copy them in tkinterdnd2/tkdnd.

## pyinstaller

If you want to use pyinstaller, you should use the hook-tkinterdnd2.py file included. Copy it in the base directory of
your project, then:

    pyinstaller -F -w myproject/myproject.py --additional-hooks-dir=.

