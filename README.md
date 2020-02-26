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

In this project we use the pre-compiled release from https://github.com/petasis/tkdnd/releases/tag/tkdnd-release-test-v2.9.2 and copy them in tkinterdnd2/tkdnd.

# Installation

Nothing fancy:

    python setup.py install

You can then import tkinterdnd2 in your project. See examples in folder "demos".

## pyinstaller

If you want to use pyinstaller, you should use the hook-tkinterdnd2.py file included. Copy it in the base directory of your project, then: 

    pyinstaller -F -w myproject/myproject.py --additional-hooks-dir=.

