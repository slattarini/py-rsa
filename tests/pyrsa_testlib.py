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

# vim: et sw=4 ts=4 ft=python
