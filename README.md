Functor.py
========

Quick and dirty function chaining with some 
hidden goodies, inspired by Haskell.

# What the heck is this?

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
raw lists. Python 2 can still be used, but it will 
be buggy and issues should be filed immediately.

# Install

Now's not the time for install; that comes later.

# Examples

Most examples below will be using functions defined within 
_Functor.Prelude_. _Prelude_ is a package dedicated at mimicking 
most common functions from Haskell GHC's "Prelude" library.

## Hello World

``` python
Unit("Hello world!") | print
```
* _print_ doesn't return a value so we end up with a None
* _print_ also isn't a function in Python 2

In Prelude is a defined print function that works across 
both versions (as a workaround for the keyword syntax).

``` python
Unit("Hello world!") | puts
```

## Number Manipulation

_succ_ and _pred_ are functions that return the 
successor and predecessor values of a number. 

``` python
Unit(4) | succ 
# => Unit(5)

Unit(4) | pred
# => Unit(3)
```

You can also negate numbers using _neg_.

``` python
Unit(5) | neg
# => Unit(-5)
```

## Tuples and Variable Argument Functions

You can store multiple values in a Unit and 
then apply those values to a function. Let's say 
we wanted to add two numbers together:

``` python
Unit(2, 3) | (lambda x, y: x + y)
# => Unit(5)
```

For any function that accepts multiple values as arguments, 
you can use Unit tuples to apply arguments to them. For 
instance, _max_ works:

``` python
Unit(2,3,4,5,6,7,8,9) | max
# => Unit(9)
```

## Lists and List Functions

Lists are a generally good way of doing procedures 
compared to tuples, as more functions take advantage of list 
versus tuples.

To make a list of numbers, we can use a new function _span_ which 
takes a number and gives us a list of numbers. This is 
different from _range_, as _span_ always returns a list. 
In Python 3 this behaviour was changed.

Make a list of numbers:
``` python
Unit(10) | span 
# => Unit([0,1,2,3,4,5,6,7,8,9])
```

Taking head and tail of a list:
``` python
Unit(5) | span | head
# => Unit(0)

Unit(5) | span | tail
# => Unit([1,2,3,4])
```

Applying a function over a list:
``` python
Unit(5) | span | fmap(suc)
# => Unit([1,2,3,4,5])
```

Filtering elements via a predicate function:
``` python
Unit(10) | span | select(even)
# => Unit([0,2,4,6,8])
```

List length of a Unit list:
``` python
Unit(10) | span | length
# => 10
```

Elements less than a fixed number:
``` python
Unit(10) | span | lt(5)
# => Unit([0,1,2,3,4])
```

Other functions include:
* lte
* gt
* gte
* equals
* nequals

Taking and dropping a number of elements
``` python
Unit(10) | span | take(5)
# => Unit([0,1,2,3,4])

Unit(10) | span | drop(5)
# => Unit([5,6,7,8,9])
```

If you don't want to start a range from 0, you can use the _to_ 
function which takes two numbers and creates a range instead.
``` python
Unit(5) | to(10)
# => Unit([5,6,7,8,9])
```

Example of a "list comprehension":
``` python
# Take numbers from 1 to 10, square, take the even numbers
Unit(1) | to(11) | fmap(square) | select(even)
# => Unit([4, 16, 36, 64, 100])

# The equivalent list comp would be
[square(x) for x in range(1,11) if even(square(x))]
```
The new Unit version looks something more akin to Ruby 
syntax, but in most cases using Python's list comps are 
better to use for performance (less memory usage).

## Reduce on Lists

The latest feature added is a clone of _functools.reduce_. 
It breaks down the elements of a list into a series of 
binary computations and returns the result.

``` python
# Finding the sum of a list of data without reduce
Unit(10) | span | sum
# => Unit(45)

# Doing the same thing as sum()
Unit(10) | span | reduce(add)
# => Unit(45)

# Defining our own product() function
Unit(1) | to(11) | reduce(mul)
# => Unit(3628800)

# Factorial of 5
Unit(1) | to(6) | reduce(mul)
# => Unit(120)
```
## Zipping

_zip_ is a cool function that takes in a number of 
lists and zips the values together to form a list of 
tuples, with matching position elements from each list.

Since _zip_ takes in a number of arguments, you have a few 
options of doing zipping.

Method one: using Unit to store the arguments of _zip_, as 
this lets you use any number of lists and returns the correct 
result.
``` python
Unit([1,2],[3,4]) | zip | list
# => Unit([(1,3), (2,4)])
```

Method two: using the new zip_with method that will perform 
a _zip_ action against a Unit and return the _zip_ of the two 
lists. The downside is that this can't be chained to produce 
the same results as a 3-or-more _zip_ call.
``` python
Unit([1,2]) | zip_with([3,4])
# => Unit([(1,3),(2,4)])
```

But if you keep chaining zip_with calls, it produces 
the same output as chaining _zip_ calls.
``` python
# Equivalent to zip(zip([1,2],[3,4]),[5,6])
Unit([1,2]) | zip_with([3,4]) | zip_with([5,6])
# => Unit([((1,3),5),((2,4),6)])
```

# Disadvantages

Since we're effectively continuously passing functions 
from one data unit to another, it makes it hard to 
access object methods of an object within a container.

Example: if we wanted to add just one value to a 
list within a container, we can't access append 
directly.

``` python
Unit([1,2,3]) | append(4) # can't do something like this

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
There are shells for both normal Python and IPython.

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

