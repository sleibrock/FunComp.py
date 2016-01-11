Functor.py
========

Quick and dirty object chaining with some 
hidden goodies, inspired by Haskell.

# What the heck is this and why?

Python's function composition is naturally ugly 
and hideous, so much that they'll probably tell you to 
*not* nest functions within eachother too much.

So here's a way of passing functions to data values 
in a point-free way that's nice and easy.

# Why?

Have you ever had a couple functions and you had to 
nest them together to get a computation? Let's say 
you had these functions.

``` python
def f(x): # do some computation
def g(x): # do another one
def h(x): # etc
def i(x): # ...
```
You wanted to nest these in a way that you got one 
final computation, so here's what you'd do in 
Python naturally.

``` python
# Calculate the value of "x"
final_value = i(h(g(f(x))))
```
Messy, right? Well this happens far too often in 
Python.

Instead, we can write expressions in the format of

``` python
Unit(x) | f | g | h | i # and so on...
```

This creates a much nicer looking function 
composition that can easily be modified and 
extended upon without much confusion.

# What the heck's a Functor?

A Functor is a special data type that follows this rule:
```
fmap :: (a -> b) -> f a -> f b
```

It takes in a function that has a type of (a -> b), 
applies the function to a Functor with a type of A, 
applies it to the A, and turns it into a Functor with a 
type of B.

In Haskell we can write quick expressions that allow 
us to manipulate special data types like Maybe or List.

``` haskell
Prelude> (+1) <$> [1..10]
[2,3,4,5,6,7,8,9,10,11]
```

This applies a (+1) function across the List Functor 
containing all numbers between 1 and 10.

Python doesn't have the same magic rules as Functors and 
the like, but the idea of Functors is what strongly 
influenced this project. Strictly speaking, this isn't 
exactly a "true" Functor unit in Python, but something 
inspired by it.

# Requirements 

Python 3 is the optimal choice, as it changes 
most functions to produce generators as opposed to 
raw lists. Python 2 can still be used, but it 
has some drawbacks:

* _print_ is not a function, it's a keyword
* _map()_ and _filter()_ return lists
* Unicode issues
* Everything else wrong with Python 2

The code will try it's best to work across 
different versions, but will be buggy.

# Install

Now's not the time for install; that comes later.

# Examples

## Hello World

``` python
Unit("Hello world!") | print
```
* _print_ doesn't return a value so we end up with a None
* _print_ also isn't a function in Python 2

## Number Manipulation

``` python
Unit(4) | succ | succ | neg
# => Unit(-6)

Unit(4,3) | (lambda x,y: x*y)
# => Unit(12)
```

## Mapping Functions Across Lists

``` python
Unit(succ, range(10)) | map
# => Unit([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
```

## Mapping and Filtering

For this we have to note that our function chaining 
works really well for functions with consistent 
amounts of arguments (1 value to 1-arg, 2 values to 2-arg, 
etc.), but what if we had 1 value and we wanted to 
apply it to a function that took 2?

In the above example for mapping
``` python
Unit(succ, range(10)) | map
```
Our Unit stores two values, _succ_ and _range(10)_. 
_map()_ takes two values so this is a natural application. 

If we wanted to a map/filter combination, the code 
gets messy real fast because _map()_ only returns 
one value. So we would *have* to nest Unit expressions 
like so.

``` python
Unit(odd, (Unit(succ, range(10)) | map | list | True)) | filter | list
```

Obviously this isn't desirable, so this project also 
includes a special module called *Prelude*, a nod to 
GHC's Prelude library. Prelude contains wrapper 
functions and curried functions to side-step this 
problem.

``` python
Unit(10) | span | select(odd) 
# => Unit([1,3,5,7,9])

Unit(100) | span | fmap(succ) | select(odd) | length
# => Unit(50)
```

Although List Comprehensions are much more effective to 
use in Python (less memory usage), this is just another 
approach of doing things.

## Take / Drop

``` python
Unit(10) | span | take(5)
# => Unit([0, 1, 2, 3, 4])
Unit(10) | span | drop(5)
# => Unit([5, 6, 7, 8, 9])
```

# Disadvantages

Since we're effectively continuously passing functions 
from one data unit to another, it makes it hard to 
access object methods of an object within a container.

Example: if we wanted to add just one value to a 
list within a container, we can't access append 
directly.

``` python
Unit([1,2,3] | append(4) # can't do something like this

# Note that even list.append is an in-memory op 
# So this effectively returns None
Unit([1,2,3]) | (lambda x: x.append(4))
# => None
```

The Unit Functor does not store data between operations 
but rather stores the results of functions that operate 
on the data. _list.append_ doesn't return anything, 
but instead we have to do shortcuts like:

``` python
# This probably won't be added to Prelude
Unit([1,2,3]) | (lambda x: x + [4]) # works but ugly
```

The point of this library is to inspire more 
functional use of Python rather than imperative, OO-style 
code. Accessing an object's methods is not actually 
something to be aimed for currently with this library.

# Notes

Check the Makefile for a quick shell launch option 
so you don't have to keep manually loading the file.

Unit expressions will always return a Unit unless 
it has been told "True" at the end to signify that 
we want to extract the value from the Unit. You can 
also send a "False" to nullify the expression. 
(This means you could in practice nest Unit expressions 
so that one can act as an "If" conditional)

``` python
Unit(4) | succ | neg | True
# => -5

Unit(4) | False
# => None
```

# Credits and Such

If you like this, check out the following:

* [The Haskell Language](https://haskell.org/)
* [PyMonad](https://pypi.python.org/pypi/PyMonad/)

