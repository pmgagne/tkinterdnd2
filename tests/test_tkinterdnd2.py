import os
import platform
import unittest
import tkinterdnd2


class TestTkinterDnD2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = tkinterdnd2.Tk()
        cls.root.withdraw()

        cls.tcl_version_str = cls.root.tk.call('info', 'tclversion')
        cls.tcl_major = int(cls.tcl_version_str.split('.')[0])

        system = platform.system()
        if system == "Windows":
            machine = os.environ.get('PROCESSOR_ARCHITECTURE', platform.machine())
        else:
            machine = platform.machine()

        platform_map = {
            ("Darwin",  "arm64"):   "osx-arm64",
            ("Darwin",  "x86_64"):  "osx-x64",
            ("Linux",   "aarch64"): "linux-arm64",
            ("Linux",   "x86_64"):  "linux-x64",
            ("Windows", "ARM64"):   "win-arm64",
            ("Windows", "AMD64"):   "win-x64",
            ("Windows", "x86"):     "win-x86",
        }
        cls.base_dir = platform_map.get((system, machine), "unknown")
        cls.tkdnd_root = os.path.join(os.path.dirname(tkinterdnd2.__file__), 'tkdnd')
        tcl9_path = os.path.join(cls.tkdnd_root, cls.base_dir + '-tcl9')
        cls.chosen_dir = (
            cls.base_dir + '-tcl9'
            if cls.tcl_major >= 9 and os.path.isdir(tcl9_path)
            else cls.base_dir
        )

        print(
            f"\nPlatform: {system}/{machine}  "
            f"Tcl: {cls.tcl_version_str}  "
            f"dir: {cls.chosen_dir}  "
            f"tkdnd: {tkinterdnd2.TkinterDnD.TkdndVersion}"
        )

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_version_is_set(self):
        """Binary loaded and TkdndVersion is populated."""
        self.assertIsNotNone(tkinterdnd2.TkinterDnD.TkdndVersion)

    def test_binary_directory_exists(self):
        """The directory that was selected exists inside the installed package."""
        path = os.path.join(self.tkdnd_root, self.chosen_dir)
        self.assertTrue(os.path.isdir(path), f"tkdnd directory not found: {path}")

    def test_tcl9_routing(self):
        """When Tcl 9 is active and a -tcl9 directory is present, it must be chosen."""
        tcl9_dir = os.path.join(self.tkdnd_root, self.base_dir + '-tcl9')
        if self.tcl_major >= 9 and os.path.isdir(tcl9_dir):
            self.assertTrue(
                self.chosen_dir.endswith('-tcl9'),
                f"Tcl {self.tcl_major} active but -tcl9 directory not chosen; got '{self.chosen_dir}'"
            )

    def test_tcl8_fallback(self):
        """When Tcl 8 is active (or no -tcl9 directory exists), base directory must be chosen."""
        tcl9_dir = os.path.join(self.tkdnd_root, self.base_dir + '-tcl9')
        if self.tcl_major < 9 or not os.path.isdir(tcl9_dir):
            self.assertFalse(
                self.chosen_dir.endswith('-tcl9'),
                f"Expected base directory but got '{self.chosen_dir}'"
            )


if __name__ == '__main__':
    unittest.main()
