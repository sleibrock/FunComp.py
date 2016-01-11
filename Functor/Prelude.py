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

# This essentially returns the entire Unit container
def id(*x):
    """
    id :: a -> a
    """
    if len(x) > 1:
        return x
    else:
        return x[0]

# Equivalent to putStrLn from Haskell.GHC
def puts(x):
    """
    puts :: String -> IO ()
    Will always return None
    """
    print(x)

# Head and Tail from Haskell.GHC
def head(x):
    """
    head :: [a] -> [a]
    """
    if not isinstance(x, list):
        return x
    return x[0]

# Tail will be undefined (None) if not a list
def tail(x):
    """
    tail :: [a] -> [a]
    """
    if not isinstance(x, list):
        return None
    return x[1:]

# Take a number of elements from a list
def take(x):
    """
    take :: Int -> [a] -> [a]
    """
    def itake(data):
        if not isinstance(data, list):
            return None
        return data[:x]
    return itake

# Drop a number of elements from a list
def drop(x):
    """
    drop :: Int -> [a] -> [a]
    """
    def idrop(data):
        if not isinstance(data, list):
            return None
        return data[x:]
    return idrop

# Successor of a value (increment on Int)
def succ(x):
    """
    succ :: Enum a => a -> a
    """
    return x + 1

# Predecessor of a value (decrement on Int)
def pred(x):
    """
    pred :: Enum a => a -> a
    """
    return x - 1

# Negate a value (Unit(5) | negate => -5)
def neg(x):
    """
    neg :: Num a => a -> a
    """
    return (-x)

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

# Span a list from 0 to x
# Usage: Unit(10) | span => [0..10]
def span(x):
    """
    span :: Num a => a -> [a]
    """
    return list(range(x))

# Create a list from Y to X
# Desired use: Unit(0) | to(10) => [0..10]
def to(x):
    """
    to :: Num a => a -> a -> [a]
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

## Curried (nested) functions
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

# end
