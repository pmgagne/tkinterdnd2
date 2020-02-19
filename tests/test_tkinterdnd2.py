import unittest

import tkinter
import TkinterDnD2

class TestStringMethods(unittest.TestCase):

    def test_version(self):
        root = TkinterDnD2.TkinterDnD.Tk()
        root.withdraw()
        self.assertEqual(TkinterDnD2.TkinterDnD.TkdndVersion, '2.9.2')

if __name__ == '__main__':
    unittest.main()