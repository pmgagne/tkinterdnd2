import os
import platform
import tkinter
import tkinterdnd2
from tkinterdnd2 import TkinterDnD

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
print("OK — drag and drop is available on this root window.")
print("Close the window to exit.")

root.title("tkinterdnd2 load test")
root.geometry("400x100")
tkinter.Label(root, text=f"Loaded tkdnd {tkinterdnd2.TkinterDnD.TkdndVersion} from {chosen_dir}").pack(pady=30)
root.mainloop()
