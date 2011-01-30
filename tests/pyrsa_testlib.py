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
    if isinstance(n, (tuple, list)) and len(n) == 2:
        class klass(RSA.IntegerModPQ):
            p, q = n[0], n[1]
        n = n[0] * n[1]
    elif isinstance(n, (int, long)) or n <= 0:
        class klass(RSA.IntegerMod):
            modulo = n
    else:
        raise TestError("Invalid parameter n: %r" % n)
    if class_name is None:
        class_name = "IntegerMod%u" % n
    klass.__name__ = class_name
    return klass

# Order-preserving sequence uniquification.
def uniquify(seq):
    uniq = []
    for x in seq:
        if x not in uniq:
            uniq.append(x)
    return seq.__class__(uniq)

# Dumb decorator that removes duplicates from sequences returned by
# the decorated function.  Don't preserve function signature, name,
# docstrings, ... as we don't need these goodies ATM.
def without_duplicates(function):
    def wrapper(*args, **kwargs):
        return uniquify(function(*args, **kwargs))
    return wrapper

# Decorators that generate a list parameters for a test function.
# Examples of usage:
#   @with_params([dict(a=2, b=2L), dict(a=0, b=0.0)])
#   def test_equals(a, b):
#       assert a == b
#   @with_params([1, "", False, None], 'x')
#   def test_nonzero(x):
#       assert x != 0
# Can be composed too:
#   @with_params([dict(x=7, y=2), dict(x=5, y=3)])
#   @with_params([10, 11], 'z')
#   def test_sum_lt(x, y, z):
#       assert x + y < z
#   @with_params([2, 3], 'x')
#   @with_params([dict(y=0), dict(y=1)])
#   def test_gt(x, y):
#       assert x > y
# "Overriding" composition like this should be avoided:
#   @with_params([dict(x=7, y=2), dict(x=5, y=9)])
#   @with_params([dict(x=1, y=2), dict(x=7, y=5)])
#   def test_different(x, y):
#       assert x != y
def with_params(funcarglist, param_name=None):
    if param_name is not None:
        funcarglist = [ {param_name: x} for x in funcarglist ]
    def decorator(function):
        if hasattr(function, 'pytest_funcarglist'):
            # We need to update the previos list of funcargs.
            new_funcarglist = []
            for d0 in function.pytest_funcarglist:
                for d1 in funcarglist:
                    new_funcarglist.append(dict(d0, **d1))
            function.pytest_funcarglist = new_funcarglist
        else:
            function.pytest_funcarglist = funcarglist
        return function
    return decorator

# Generic decorators-based test parameters generator.
def pytest_generate_tests(metafunc):
    for funcargs in getattr(metafunc.function, 'pytest_funcarglist', ()):
        metafunc.addcall(funcargs=funcargs)

# vim: et sw=4 ts=4 ft=python
