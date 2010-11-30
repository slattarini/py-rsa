#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Helper subroutines the RSA.py's testsuite"""

import RSA

class TestError(Exception):
    pass

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


# vim: et sw=4 ts=4 ft=python
