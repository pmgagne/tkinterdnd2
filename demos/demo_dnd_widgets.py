#!/usr/bin/env python3
"""Interactive manual test bed for tkinterdnd2.

Run this, then actually drag files (single and multiple, with and without
spaces in their names) and text from your file manager / another app onto
the zones below. Everything that happens is timestamped in the log panel
at the bottom so behavior can be compared across widget types and across
repeated attempts (e.g. to check whether the *first* drag after launch
behaves differently from later ones).

Not a unittest — this is meant to be run and watched, not asserted on.
"""

import os
import platform
import time
import tkinter as tk
from tkinter import ttk

import tkinterdnd2
from tkinterdnd2 import COPY, DND_ALL, DND_FILES, DND_TEXT, TkinterDnD

root = TkinterDnD.Tk()
root.title("tkinterdnd2 — interactive widget test")
root.geometry("760x680")

# ── info banner ──────────────────────────────────────────────────────────
tcl_version = root.tk.call("info", "tclversion")
system = platform.system()
machine = os.environ.get("PROCESSOR_ARCHITECTURE", platform.machine()) if system == "Windows" else platform.machine()
info_text = (
    f"Platform: {system}/{machine}   Python: {platform.python_version()}   "
    f"Tcl: {tcl_version}   tkdnd: {tkinterdnd2.TkinterDnD.TkdndVersion}"
)
tk.Label(root, text=info_text, font=("Courier", 9), anchor="w", fg="#555").pack(fill="x", padx=8, pady=(6, 0))

# ── shared log panel ─────────────────────────────────────────────────────
log_frame = tk.LabelFrame(root, text="Event log (newest at bottom)")
log_frame.pack(side="bottom", fill="both", padx=8, pady=8)

log_text = tk.Text(log_frame, height=14, wrap="word", font=("Courier", 9), state="disabled")
log_scroll = tk.Scrollbar(log_frame, command=log_text.yview)
log_text.configure(yscrollcommand=log_scroll.set)
log_text.pack(side="left", fill="both", expand=True)
log_scroll.pack(side="right", fill="y")

tk.Button(log_frame, text="Clear log", command=lambda: (
    log_text.configure(state="normal"), log_text.delete("1.0", "end"), log_text.configure(state="disabled")
)).pack(side="bottom", anchor="e", padx=4, pady=4)


def log(msg):
    log_text.configure(state="normal")
    log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    log_text.configure(state="disabled")
    log_text.see("end")
    print(msg, flush=True)


def parse_files(data):
    """Correct way to turn a dropped DND_FILES `data` string into a list of
    real paths: use Tcl's own list parser, which understands the {brace
    quoting} tkdnd uses for entries containing spaces. Do NOT data.split()."""
    return list(root.tk.splitlist(data))


# ── per-zone drop counters (helps spot "first drop doesn't register") ────
counts = {}


def set_bg(widget, color):
    """ttk widgets (Entry, Treeview, ...) don't have a -bg option; they're
    themed via ttk.Style instead. Skip the highlight color-change for them
    rather than erroring, since it's cosmetic only."""
    if isinstance(widget, ttk.Widget):
        return
    widget.configure(bg=color)


def make_common_bindings(widget, name, highlight_bg, base_bg):
    def on_enter(event):
        set_bg(widget, highlight_bg)
        log(f"[{name}] DropEnter  action={event.action} types={event.types}")
        return event.action

    def on_leave(event):
        set_bg(widget, base_bg)
        log(f"[{name}] DropLeave")

    widget.dnd_bind("<<DropEnter>>", on_enter)
    widget.dnd_bind("<<DropLeave>>", on_leave)


def looks_like_file_paths(data):
    """Heuristic used only for this test bed's own display logic (not part of
    tkinterdnd2): DND_ALL/mixed-type zones need to guess whether a drop was
    files or plain text so they can log/render it usefully."""
    data = data.strip()
    if not data:
        return False
    return data.startswith("{") or os.path.exists(data.split()[0])


def make_drop_handler(name, widget, base_bg, on_files=None, on_text=None):
    def on_drop(event):
        set_bg(widget, base_bg)
        counts[name] = counts.get(name, 0) + 1
        n = counts[name]
        log(f"[{name}] Drop #{n} raw event.data = {event.data!r}")

        if looks_like_file_paths(event.data) and on_files is not None:
            files = parse_files(event.data)
            log(f"[{name}] Drop #{n} parsed into {len(files)} path(s):")
            for f in files:
                exists = os.path.isfile(f)
                note = "OK" if exists else "MISSING/UNREADABLE"
                if exists:
                    try:
                        with open(f, "rb") as fh:
                            size = len(fh.read())
                        note = f"OK ({size} bytes)"
                    except OSError as e:
                        note = f"OPEN FAILED: {e}"
                log(f"    - {f!r}  [{note}]")
            on_files(files)
        elif on_text is not None:
            on_text(event.data)
        return event.action

    return on_drop


# ── Notebook of drop-target widget types ─────────────────────────────────
nb = ttk.Notebook(root)
nb.pack(fill="both", expand=True, padx=8, pady=(8, 0))

# 1. tk.Label — DND_FILES + DND_TEXT (baseline, known-good widget class)
tab1 = ttk.Frame(nb)
nb.add(tab1, text="tk.Label")
label_zone = tk.Label(tab1, text="Drop files or text here\n(tk.Label)", bg="#e8f0fe", relief="groove", font=("TkDefaultFont", 12))
label_zone.pack(fill="both", expand=True, padx=10, pady=10)
make_common_bindings(label_zone, "Label", "#c8d8fc", "#e8f0fe")
label_zone.drop_target_register(DND_FILES, DND_TEXT)
label_zone.dnd_bind("<<Drop>>", make_drop_handler(
    "Label", label_zone, "#e8f0fe",
    on_files=lambda files: label_zone.configure(text=f"{len(files)} file(s) dropped, see log"),
    on_text=lambda text: label_zone.configure(text=f"Text dropped:\n{text}"),
))

# 2. tk.Listbox — DND_FILES, inserts each parsed path as its own row
tab2 = ttk.Frame(nb)
nb.add(tab2, text="tk.Listbox")
lb_zone = tk.Listbox(tab2, bg="#fff8e1")
lb_zone.pack(fill="both", expand=True, padx=10, pady=10)
lb_zone.insert("end", "Drop multiple files here — each should appear as its own row")
make_common_bindings(lb_zone, "Listbox", "#ffe9a8", "#fff8e1")
lb_zone.drop_target_register(DND_FILES)
lb_zone.dnd_bind("<<Drop>>", make_drop_handler(
    "Listbox", lb_zone, "#fff8e1",
    on_files=lambda files: [lb_zone.insert("end", f) for f in files],
))

# 3. tk.Text — DND_ALL (generic/any type)
tab3 = ttk.Frame(nb)
nb.add(tab3, text="tk.Text (DND_ALL)")
text_zone = tk.Text(tab3, bg="#f3e5f5", wrap="word")
text_zone.pack(fill="both", expand=True, padx=10, pady=10)
text_zone.insert("end", "Drop files or text here (registered for DND_ALL)")
make_common_bindings(text_zone, "Text", "#e1bee7", "#f3e5f5")
text_zone.drop_target_register(DND_ALL)
text_zone.dnd_bind("<<Drop>>", make_drop_handler(
    "Text", text_zone, "#f3e5f5",
    on_files=lambda files: text_zone.insert("end", "\n" + "\n".join(files)),
    on_text=lambda t: text_zone.insert("end", "\n" + t),
))

# 4. ttk.Entry — DND_FILES (a plain ttk widget, not just ttk.Treeview)
tab4 = ttk.Frame(nb)
nb.add(tab4, text="ttk.Entry")
entry_var = tk.StringVar(value="Drop a single file here (ttk.Entry)")
entry_zone = ttk.Entry(tab4, textvariable=entry_var)
entry_zone.pack(fill="x", padx=10, pady=10)
make_common_bindings(entry_zone, "Entry", "#ffcdd2", "")
entry_zone.drop_target_register(DND_FILES)
entry_zone.dnd_bind("<<Drop>>", make_drop_handler(
    "Entry", entry_zone, "",
    on_files=lambda files: entry_var.set(files[0] if files else ""),
))

# 5. ttk.Treeview — DND_FILES (the exact widget type from the original bug report)
tab5 = ttk.Frame(nb)
nb.add(tab5, text="ttk.Treeview")
tree_zone = ttk.Treeview(tab5, show="tree")
tree_zone.pack(fill="both", expand=True, padx=10, pady=10)
tree_zone.insert("", "end", text="Drop files here (ttk.Treeview, show='tree')")
make_common_bindings(tree_zone, "Treeview", "#c8e6c9", "")
tree_zone.drop_target_register(DND_FILES)
tree_zone.dnd_bind("<<Drop>>", make_drop_handler(
    "Treeview", tree_zone, "",
    on_files=lambda files: [tree_zone.insert("", "end", text=f) for f in files],
))

# ── drag source (for testing dragging text/files *out* of the app) ──────
drag_frame = tk.LabelFrame(root, text="Drag source (drag this out to another app)")
drag_frame.pack(fill="x", padx=8, pady=(8, 0))
drag_label = tk.Label(drag_frame, text="  Drag me (sends text)  ", bg="#fff3cd", relief="raised", cursor="hand2", pady=6)
drag_label.pack(fill="x", padx=4, pady=4)


def on_drag_init(event):
    log("[DragSource] DragInitCmd fired")
    return (COPY, DND_TEXT, "Hello from tkinterdnd2 test_dnd_widgets.py!")


def on_drag_end(event):
    log(f"[DragSource] DragEndCmd action={event.action}")


drag_label.drag_source_register(1, DND_TEXT)
drag_label.dnd_bind("<<DragInitCmd>>", on_drag_init)
drag_label.dnd_bind("<<DragEndCmd>>", on_drag_end)

log("Ready. Drag files/text onto any tab above. Try a single file, multiple files, "
    "and a file with spaces in its name, and compare the first attempt to later ones.")

root.mainloop()
