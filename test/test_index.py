import sys; sys.path.append("../")

import unittest
import copy

from delimited.index import ListIndex


class TestListIndex(unittest.TestCase):

    # __init__

    def test____init__(self):
        a = ListIndex(0)
        self.assertEqual(a.index, 0)
        
    def test____init____raises_TypeError(self):
        with self.assertRaises(TypeError):
            a = ListIndex("foo")

    # __str__
    
    def test____str__(self):
        a = ListIndex(0)
        self.assertEqual(str(a), "0")
        
    # __repr__
    
    def test____repr__(self):
        a = ListIndex(0)
        self.assertEqual(repr(a), "ListIndex(0)")


if __name__ == "__main__":
    unittest.main()
