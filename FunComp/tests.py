#!/usr/bin/env python

import unittest
import math

# Test if the package isn't broken locally
try:
    from Unit import *
    from Prelude import *
except ImportError:
    print("Couldn't find the FunComp package")
    quit()

class TestChains(unittest.TestCase):
    """
    Test different operations of 
    Prelude against the Unit class
    """
    def testBasicNumberAddition(self):
        x = Unit(5) | (lambda x: x + 1) | True
        self.assertEqual(x, 6)

    def testTrueFalseReturns(self):
        a = Unit(5) | True
        b = Unit(5) | False
        self.assertEqual(a, 5)
        self.assertEqual(b, None)
    
    def testLengths(self):
        a = Unit(10) | length | True
        b = Unit("Hey") | length | True
        c = Unit(10) | span | length | True
        self.assertEqual(a, 1)
        self.assertEqual(b, 3)
        self.assertEqual(c, 10)

    def testSuccAndPred(self):
        a = Unit(5) | succ | True
        b = Unit(5) | pred | True
        self.assertEqual(a, 6)
        self.assertEqual(b, 4)

    def testHeadAndTail(self):
        a = Unit(10) | span | head | True
        b = Unit(10) | span | tail | True
        self.assertEqual(a, 0)
        self.assertEqual(b, list(range(1,10)))

    def testFilterMap(self):
        a = Unit(100) | span | select(odd) | length | True
        b = Unit(10) | span | fmap(succ) | True
        self.assertEqual(a, 50)
        self.assertEqual(b, list(range(1,11)))

    def testTuples(self):
        a = Unit(2,3) | (lambda x, y: x + y) | True
        b = Unit(2,3) | pow | True
        self.assertEqual(a, 5)
        self.assertEqual(b, 8)

    def testComps(self):
        a = Unit(10) | span | lte(5) | True
        b = Unit(10) | span | lt(3) | True
        c = Unit(10) | span | gt(4) | True
        d = Unit(10) | span | gte(2) | True
        e = Unit(10) | span | equals(7) | True
        f = Unit(10) | span | nequals(8) | True
        self.assertEqual(a, list(range(6)))
        self.assertEqual(b, list(range(3)))
        self.assertEqual(c, list(range(5,10)))
        self.assertEqual(d, list(range(2,10)))
        self.assertEqual(e, [7])
        self.assertEqual(f, [0,1,2,3,4,5,6,7,9])

    def testReduce(self):
        a = Unit(1) | to(10) | reduce(add) | True
        b = Unit(1) | to(10) | reduce(mul) | True
        self.assertEqual(a, 55)
        self.assertEqual(b, 3628800)


if __name__ == "__main__":
    unittest.main()

