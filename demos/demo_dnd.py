import os
import platform
import tkinter as tk
import tkinterdnd2
from tkinterdnd2 import TkinterDnD, DND_FILES, DND_TEXT, DND_ALL

root = TkinterDnD.Tk()

tcl_version = root.tk.call('info', 'tclversion')
tcl_major = int(tcl_version.split('.')[0])

system = platform.system()
if system == "Windows":
    machine = os.environ.get('PROCESSOR_ARCHITECTURE', platform.machine())
else:
    machine = platform.machine()

platform_map = {
    ("Darwin",  "arm64"):  "osx-arm64",
    ("Darwin",  "x86_64"): "osx-x64",
    ("Linux",   "aarch64"):"linux-arm64",
    ("Linux",   "x86_64"): "linux-x64",
    ("Windows", "ARM64"):  "win-arm64",
    ("Windows", "AMD64"):  "win-x64",
    ("Windows", "x86"):    "win-x86",
}
base_dir = platform_map.get((system, machine), "unknown")
tcl9_dir = os.path.join(os.path.dirname(tkinterdnd2.__file__), 'tkdnd', base_dir + '-tcl9')
chosen_dir = (base_dir + '-tcl9') if (tcl_major >= 9 and os.path.isdir(tcl9_dir)) else base_dir

print(f"Platform:      {system} / {machine}")
print(f"Tcl version:   {tcl_version}  (major={tcl_major})")
print(f"tkdnd dir:     {chosen_dir}")
print(f"TkDND version: {tkinterdnd2.TkinterDnD.TkdndVersion}")
print()
print("Drag a file or text onto the drop zone in the window.")

root.title("tkinterdnd2 drag-and-drop test")
root.geometry("520x420")
root.resizable(True, True)

# ── info banner ──────────────────────────────────────────────────────────────
info = (
    f"Platform: {system} / {machine}   "
    f"Tcl: {tcl_version}   "
    f"tkdnd: {tkinterdnd2.TkinterDnD.TkdndVersion}   "
    f"dir: {chosen_dir}"
)
tk.Label(root, text=info, font=("Courier", 9), anchor="w", fg="#555").pack(
    fill="x", padx=8, pady=(6, 0)
)

# ── drop zone ────────────────────────────────────────────────────────────────
drop_frame = tk.LabelFrame(root, text="Drop zone  (files or text)", padx=4, pady=4)
drop_frame.pack(fill="both", expand=True, padx=10, pady=8)

drop_label = tk.Label(
    drop_frame,
    text="Drop files or text here",
    bg="#e8f0fe",
    relief="groove",
    font=("TkDefaultFont", 11),
)
drop_label.pack(fill="both", expand=True)

result_var = tk.StringVar(value="")
result_box = tk.Text(drop_frame, height=6, state="disabled", wrap="word", relief="flat",
                     bg="#f9f9f9", font=("Courier", 9))
result_box.pack(fill="x", pady=(4, 0))

def _set_result(text):
    result_box.configure(state="normal")
    result_box.delete("1.0", "end")
    result_box.insert("end", text)
    result_box.configure(state="disabled")
    print(f"[drop] {text}")

def on_drop_enter(event):
    drop_label.configure(bg="#c8d8fc", text="Release to drop")
    return event.action

def on_drop_leave(event):
    drop_label.configure(bg="#e8f0fe", text="Drop files or text here")

def on_drop(event):
    drop_label.configure(bg="#e8f0fe", text="Drop files or text here")
    data = event.data
    # tkdnd returns file lists enclosed in braces on some platforms
    try:
        files = root.tk.splitlist(data)
    except Exception:
        files = [data]
    if len(files) == 1 and not os.path.exists(files[0]):
        _set_result(f"Text dropped:\n{data}")
    else:
        lines = "\n".join(files)
        _set_result(f"{len(files)} file(s) dropped:\n{lines}")
    return event.action

drop_label.drop_target_register(DND_FILES, DND_TEXT)
drop_label.dnd_bind("<<DropEnter>>",    on_drop_enter)
drop_label.dnd_bind("<<DropLeave>>",    on_drop_leave)
drop_label.dnd_bind("<<Drop>>",         on_drop)

# ── drag source ──────────────────────────────────────────────────────────────
drag_frame = tk.LabelFrame(root, text="Drag source  (drag this label to another app)", padx=4, pady=4)
drag_frame.pack(fill="x", padx=10, pady=(0, 10))

drag_label = tk.Label(
    drag_frame,
    text="  Drag me  ",
    bg="#fff3cd",
    relief="raised",
    cursor="hand2",
    font=("TkDefaultFont", 11, "bold"),
    pady=8,
)
drag_label.pack(fill="x")

def on_drag_init(event):
    drag_label.configure(bg="#ffe08a")
    return (tkinterdnd2.COPY, DND_TEXT, "Hello from tkinterdnd2!")

def on_drag_end(event):
    drag_label.configure(bg="#fff3cd")
    print(f"[drag end] action={event.action}")

drag_label.drag_source_register(1, DND_TEXT)
drag_label.dnd_bind("<<DragInitCmd>>", on_drag_init)
drag_label.dnd_bind("<<DragEndCmd>>",  on_drag_end)

root.mainloop()
