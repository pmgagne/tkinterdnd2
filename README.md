## TkinterDnD2

[Eliav2/tkinterdnd2](https://github.com/Eliav2/tkinterdnd2) is a fork of the (unmaintained) [pmgagne/tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) which is a python wrapper for [tkdnd](https://github.com/petasis/tkdnd) . 

This repo was originally forked and edited for the purpose of publishing to pypi so one could simply install this package with  `pip install tkinterdnd2`.

This repository is being maintained to ensure availability of `tkinterdnd2` into the future.

## Install

`python -m pip install tkinterdnd2`

## Usage

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

## What is TkinterDnD2

[TkinterDnD2](http://tkinterdnd.sourceforge.net) is a python wrapper for George Petasis' tkDnD Tk extension version 2.

It is a domain public project.

## What is TkDnD2

[tkDnD2](https://github.com/petasis/tkdnd) is a tcl/Tk extension adding native drag and drop support.

## What this repository is about

This repo package TkinterDnD2 and tkdnd2 into a standard python module.

When the extension is imported in python its location will be automatically added to the Tk search path.

This repository contains the compiled binaries from https://github.com/petasis/tkdnd/releases/tag/tkdnd-release-test-v2.9.4. In order to provide support on ARM, we include built binaries from the now defunct [tkinterdnd2-universal](https://pypi.org/project/tkinterdnd2-universal/#files) which added ARM support.

## pyinstaller

When using `pyinstaller`, you should use the hook-tkinterdnd2.py file included to collect the TkDnD binaries and build them into the project. To use it, copy it into the base directory of your project, then run pyinstaller as follows:

    pyinstaller -F -w myproject/myproject.py --additional-hooks-dir=.
