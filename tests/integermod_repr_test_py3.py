#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of RSA.py testsuite.

"""Tests the repr method of RSA.py's implementation of integers (mod n).
This test is tailored to python 3.x"""

from RSA import IntegerMod

def test_integermod_repr():
    class MyType(type):
        def __repr__(self):
            return self.__name__
    class MyClass(IntegerMod, metaclass = MyType):
        modulo = 5
    class MySubClass(MyClass):
        modulo = 11
    assert (repr(MyClass(23)) == "MyClass(3)"
            and repr(MySubClass(23)) == "MySubClass(1)")

# vim: et sw=4 ts=4 ft=python
