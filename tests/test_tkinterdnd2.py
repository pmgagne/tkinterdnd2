import unittest

import tkinter
import TkinterDnD2

class TestStringMethods(unittest.TestCase):

    def test_version(self):
        root = TkinterDnD2.Tk()
        root.withdraw()
        self.assertEqual(root.TkdndVersion, '2.9.2')

if __name__ == '__main__':
    unittest.main()