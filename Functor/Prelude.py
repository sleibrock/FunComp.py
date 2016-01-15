#!/usr/bin/env python

"""
Prelude.py

Aimed to recreate some basic functions from 
GHC's "Prelude" collection

TODO:
    Range does NOT work with built-in filter()

    * filter(odd, range(10)) works
    * but not Unit(10) | range | select(odd)
    * workaround: Unit(10) | range | list | select(odd)
"""

# If we run into any 2/3 bugs, fix it with version_info
from sys import version_info

# Typeclass stuff
# Use these to enforce rules amongst Unit functions
typeclasses = {
        "num" : (int, float, complex),
        "enum": (int, float, complex),
        "ord" : (int, float, complex, str, bool, str, list),
        "foldable" : (str, list, tuple, dict, set, frozenset, iter),
        "traversable" : (str, list, tuple, dict, set, frozenset, iter),
        "eq" : (), # work on more
}

# Wrapper variables for Typeclasses
# Write a lot less quotes in code (these should be enums)
Num = "num"
Enum = "enum"
Ord = "ord"
Foldable = "foldable"
Traversable = "traversable"
Eq = "eq"

# Typeclass check functions
def is_type(cls, value):
    """
    Check if a value belongs in a typeclass
    """
    return any((isinstance(value, c) for c in typeclasses[cls.lower()]))

def isnt_type(cls, value):
    """
    Wrapper for is_type so you can avoid writing "not is_type"
    """
    return not is_type(cls, value)

# A curried version of is_type so you can pass it to Unit values
def type_of(cls):
    """
    type_of :: String -> a -> Bool
    """
    def itype(data):
        return is_type(cls, data)
    return itype

# This essentially returns the entire Unit container
def id(*data):
    """
    id :: a -> a
    """
    if len(data) > 1:
        return data
    else:
        return data[0]

# Equivalent to putStrLn from Haskell.GHC
def puts(data):
    """
    puts :: String -> IO ()
    Will always return None
    """
    print(data)

# Head and Tail from Haskell.GHC
def head(data):
    """
    head :: [a] -> [a]
    If data is not a list type, return it
    """
    if not isinstance(data, list):
        return data
    return data[0]

# Tail will be undefined (None) if not a list
def tail(data):
    """
    tail :: [a] -> [a]
    If data is not a list, return None
    """
    if not isinstance(data, list):
        return None
    return data[1:]

# Take a number of elements from a list
def take(amount):
    """
    take :: Int -> [a] -> [a]
    If the unit data is not a list, return None
    """
    if not isinstance(amount, int):
        raise Exception("take() - value given not an Integer")
    def itake(data):
        if not isinstance(data, list):
            return None
        return data[:amount]
    return itake

# Drop a number of elements from a list
def drop(amount):
    """
    drop :: Int -> [a] -> [a]
    If the unit data is not a list, return None
    """
    if not isinstance(amount, int):
        raise Exception("drop() - value given not an Integer")
    def idrop(data):
        if not isinstance(data, list):
            return None
        return data[x:]
    return idrop

# Successor of a value (increment on Int)
def succ(value):
    """
    succ :: Enum a => a -> a
    """
    return value + 1

# Predecessor of a value (decrement on Int)
def pred(value):
    """
    pred :: Enum a => a -> a
    """
    return value - 1

# Redefine common math ops so we 
# Don't have to constantly import operator package
def add(left_value, right_value):
    """
    add :: Num a => a -> a -> a
    """
    return left_value + right_value

def sub(left_value, right_value):
    """
    sub :: Num a => a -> a -> a
    """
    return left_value - right_value

def mul(left_value, right_value):
    """
    mul :: Num a => a -> a -> a
    """
    return left_value * right_value

def div(left_value, right_value):
    """
    div :: Num a => a -> a -> a
    """
    if right_value == 0:
        raise ZeroDivisionError
    return left_value / right_value

# Negate a value (Unit(5) | negate => -5)
def neg(value):
    """
    neg :: Num a => a -> a
    """
    return (-value)

# Even and odd (No explanation)
def odd(x):
    """
    odd :: Num a => a -> Bool
    """
    return bool(x&1)

def even(x):
    """
    even :: Num a => a -> Bool
    """
    return bool(not x&1)

# Exponentiate a number by a number
# Curries pow(x,y)
def expo(x):
    """
    expo :: Num a => a -> a -> a
    """
    def iexp(base):
        return pow(base, x)
    return iexp

# Square a number (wraps pow)
def square(x):
    """
    square :: Num a => a -> a
    """
    return pow(x,2)

# Cubes a number (wraps pow)
def cube(x):
    """
    cube :: Num a => a -> a
    """
    return pow(x,3)

# Take a function with no arguments and 
# collects the results a number of times
def collect(amount):
    """
    collect :: (a) -> Int -> [a]
    """
    def icoll(fun):
        res = list()
        for x in range(amount):
           res.append(fun())
        return res
    return icoll

# Span a list from 0 to x
# Usage: Unit(10) | span => [0..10]
def span(x):
    """
    span :: Int -> [Int]
    """
    return list(range(x))

# Create a list from Y to X
# Desired use: Unit(0) | to(10) => [0..10]
def to(x):
    """
    to :: Int -> Int -> [Int]
    """
    def ito(y):
        return list(range(y,x))
    return ito

# Wrap len() over an object that may or may 
# not be a list
# Usage: Unit(100) | span | select(odd) | length => 50
def length(x):
    """
    length :: Foldable t => t a -> Int
    """
    if not isinstance(x, list):
        return len(list([x]))
    return len(list(x))

# Apply a map to the data
# If the data isn't a list, turn it into one
def fmap(func):
    """
    fmap :: (a -> b) -> f a -> f b
    """
    def imap(data):
        if not isinstance(data, list):
            return list(map(func, [data]))
        return list(map(func, data))
    return imap

# Select elements where predicate is true
# Wrapper for filter()
# Usage: Unit(100) | span | select(odd) => (all odds) 
def select(func):
    """
    filter :: (a -> Bool) -> [a] -> [a]
    """
    def imap(data):
        if not isinstance(data, list):
            return list(filter(func, [data]))
        return list(filter(func, data))
    return imap

### Comparison operators (shorthand filters)
def comp(comp_fun):
    """
    comp :: (a -> b) -> a -> [a] -> [a]
    """
    def inner1(value):
        def inner2(data):
            if not isinstance(data, list):
                return list(filter(comp_fun, [data]))
            return list(filter(comp_fun, data))
        return inner2
    return inner1

# Yes these look weird, but it's necessary (TODO?)
def lt(y):
    """
    lt :: a -> [a] -> [a]
```
    """
    return comp(lambda x: x < y)(y)

def lte(y):
    """
    lte :: a -> [a] -> [a]
    """
    return comp(lambda x: x <= y)(y)

def gt(y):
    """
    gt :: a -> [a] -> [a]
    """
    return comp(lambda x: x > y)(y)

def gte(y):
    """
    gte :: a -> [a] -> [a]
    """
    return comp(lambda x: x >= y)(y)

def equals(y):
    """
    equals :: a -> [a] -> [a]
    """
    return comp(lambda x: x == y)(y)

def nequals(y):
    """
    nequals :: a -> [a] -> [a]
    """
    return comp(lambda x: x != y)(y)

# Zipping with Units
def zip_with(zipper):
    """
    zip_with :: [a] -> [b] -> [b]
    """
    def izip(data):
        if not isinstance(data, list):
            return list(zip([data], zipper))
        return list(zip(data, zipper))
    return izip

# The return of the "reduce" operation
def reduce(func):
    """
    reduce :: Foldable t => (a -> b -> b) -> t a -> b
    """
    def ired(data):
        accum = None
        if not isinstance(data, list):
            data = list(data)
        for x in data:
            if accum is None:
                accum = x
            else:
                accum = func(accum, x)
        return accum
    return ired

# concat function
# Essentially the same as a reduce operation
# Lists and strings both have + ops
def concat(data):
    """
    concat :: [[a]] -> [a]
    """
    return reduce(add)(data)    

# end
