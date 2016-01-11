chain.py
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
def f(x): ...
def g(x): ...
def h(x): ...
def i(x): ...
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

# Examples

## Hello World

``` python
Unit("Hello world!") | print
```
* _print_ doesn't return a value so we end up with a None

## Number Manipulation

``` python
Unit(4) | succ | succ | neg
# => Unit(-6)

Unit(4,3) | (lambda x,y: x*y)
# => Unit(12)
```

## Mapping Functions Across Lists

``` python
Unit(succ, range(10)) | map | list
# => Unit([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
```

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
# => 4 

Unit(4) | False
# => None
```
