#!/usr/bin/env python

import unittest
import math

# Test if the package isn't broken locally
try:
    from Functor import *
except ImportError:
    print("Couldn't find the chain package")
    quit()

class TestChains(unittest.TestCase):

    def setUp(self):
        pass

    def testBasicNumbers(self):
        x = Unit(5) | (lambda x: x + 1) | data
        self.assertTrue(x==6)
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()

