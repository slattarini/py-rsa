#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Helper subroutines and classes for the RSA.py's testsuite"""

class TestError(Exception):
    pass

# Build a proper subclass of RSA.IntegerMod, with the given
# modulo; the class name is set to a sane default if not given
# explicitly.
def integers_mod(n, class_name=None):
    import RSA
    if not isinstance(n, (int, long)) or n <= 0:
        raise TestError("Invalid parameter n: %r" % n)
    if class_name is None:
        class_name = "IntegerMod%u" % n
    class klass(RSA.IntegerMod):
        modulo = n
    klass.__name__ = class_name
    return klass

# Order-preserving sequence uniquification.
def uniquify(seq):
    uniq = []
    for x in seq:
        if x not in uniq:
            uniq.append(x)
    return seq.__class__(uniq)

class TestDataGenerator:
    def __init__(self):
        self._tests_data = {}
    # Here, `args' is expected to be a list of funcarg names.
    # NOTE: This will override previous data with the same `args'
    #       key.
    def update(self, test_generator, args):
        from copy import copy
        if callable(test_generator):
            tests_data = test_generator()
        else:
            tests_data =  [ copy(x) for x in test_generator ]
        self._tests_data[frozenset(args)] = uniquify(tests_data)
    def has(self, args):
        return self._tests_data.has_key(frozenset(args))
    def get(self, args):
        return self._tests_data[frozenset(args)]
    def remove(self, args):
        del self._tests_data[frozenset(args)]

# Decorator that generate parameters for a test function.
# Example of usage:
#   @with_params([dict(a=1, b=2), dict(a=3, b=3)])
#   def test_equals(a, b):
#       assert a == b
def with_params(funcarglist):
    def decorator(function):
        function.pytest_funcarglist = uniquify(funcarglist)
        return function
    return decorator

# Generic decorators-based test parameters generator.
def pytest_generate_tests(metafunc):
    for funcargs in getattr(metafunc.function, 'pytest_funcarglist', ()):
        metafunc.addcall(funcargs=funcargs)

# vim: et sw=4 ts=4 ft=python
