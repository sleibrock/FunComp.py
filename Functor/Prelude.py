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
# Num - numbers (ints, floats, comp)
# Ord - types that can be ordered based on their value(s)
# Enum - types that have positions or storage of some kind
Int, Num, Real, Ord, Enum = range(5)

# TODO: does this system allow modularity/extendability non-builtins?
typeclasses = {
        Int  : (int, bool),
        Num  : (int, float, complex),
        Real : (int, float),
        Ord  : (int, float, complex, bool, str, list, bytes),
        Enum : (list, tuple, set, frozenset, dict, str),
}

# Typeclass check functions
def is_type(cls, *value):
    """
    Check if value(s) belongs in a typeclass
    is_type :: Int -> a -> Bool
    """
    return any((isinstance(v, c) for v in value for c in typeclasses[cls]))

def isnt_type(cls, *value):
    """
    Wrapper for is_type so you can avoid writing "not is_type"
    isnt_type :: Int -> a -> Bool
    """
    return not is_type(cls, *value)

# A curried version of is_type so you can pass it to Unit values
def type_of(cls):
    """
    type_of :: Int -> a -> Bool
    """
    def itype(data):
        return is_type(cls, data)
    return itype

def type_not(cls):
    """
    type_not :: Int -> a -> Bool
    Inverse type_of for Unit operations
    """
    return not type_of(cls)

# This essentially returns the entire Unit container
def id(*data):
    """
    id :: a -> a
    A mathematical "id" function to return the Unit
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
    if isnt_type(Enum, data):
        return data
    return data[0]

# Tail will be undefined (None) if not a list
def tail(data):
    """
    tail :: [a] -> [a]
    If data is not a list, return None
    """
    if isnt_type(Enum, data):
        return None
    return data[1:]

# Take a number of elements from a list
def take(amount):
    """
    take :: Int -> [a] -> [a]
    If the unit data is not a list, return None
    """
    if isnt_type(Num, amount):
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

# Redefine common math ops so we can enforce types 
def add(left_value, right_value):
    """
    add :: Num a => a -> a -> a
    """
    if isnt_type(Num, left_value, right_value):
        raise Exception("add() -Non-numeric types given")
    return left_value + right_value

def sub(left_value, right_value):
    """
    sub :: Num a => a -> a -> a
    """
    if isnt_type(Num, left_value, right_value):
        raise Exception("sub() -Non-numeric types given")
    return left_value - right_value

def mul(left_value, right_value):
    """
    mul :: Num a => a -> a -> a
    """
    if isnt_type(Num, left_value, right_value):
        raise Exception("mul() -Non-numeric types given")
    return left_value * right_value

def div(left_value, right_value):
    """
    div :: Num a => a -> a -> a
    """
    if isnt_type(Num, left_value, right_value):
        raise Exception("div() -Non-numeric types given")
    if right_value == 0:
        raise ZeroDivisionError
    return left_value / right_value

# Negate a value (Unit(5) | negate => -5)
def neg(value):
    """
    neg :: Num a => a -> a
    """
    if isnt_type(Num, value):
        raise Exception("div() -Non-numeric types given")
    return (-value)

# Even and odd, only works for Real numbers
def odd(value):
    """
    odd :: Real a => a -> Bool
    """
    if isnt_type(Real, value):
        raise Exception("odd() - no complex values")
    return bool(value & 1)

def even(value):
    """
    even :: Real a => a -> Bool
    """
    if isnt_type(Real, value):
        raise Exception("odd() - no complex values")
    return bool(not value & 1)

# Exponentiate a number by a number
# Curries pow(x,y)
def expo(x):
    """
    expo :: Num a => a -> a -> a
    """
    def iexp(base):
        if isnt_type(Num, value, base):
            raise Exception("expo() - invalid input")
        return pow(base, x)
    return iexp

# Square a number (wraps pow)
def square(value):
    """
    square :: Num a => a -> a
    """
    if isnt_type(Num, value):
        raise Exception("square() - invalid input")
    return pow(value, 2)

# Cubes a number (wraps pow)
def cube(value):
    """
    cube :: Num a => a -> a
    """
    if isnt_type(Num, value):
        raise Exception("cube() - invalid input")
    return pow(value, 3)

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
def span(value):
    """
    span :: Int -> [Int]
    """
    if isnt_type(Int, value):
        raise Exception("span() - invalid range type")
    return list(range(value))

# Create a list from Y to X
# Desired use: Unit(0) | to(10) => [0..10]
def to(end):
    """
    to :: Int -> Int -> [Int]
    """
    def ito(begin):
        if isnt_type(Int, begin, end):
            raise Exception("to() - invalid range types")
        return list(range(begin, succ(end)))
    return ito

# Wrap len() over an object that may or may 
# not be a list
# Usage: Unit(100) | span | select(odd) | length => 50
def length(data):
    """
    length :: Enum t => t a -> Int
    """
    if is_type(Enum, data):
        return len(data)
    return len([data])

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
    reduce :: Enum t => (a -> b -> b) -> t a -> b
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
