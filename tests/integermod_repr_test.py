#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of RSA.py testsuite.

"""Tests the repr method of RSA.py's implementation of integers (mod n).
We need the trick with the import because of syntactical incompatibilities
between python2 and python3 w.r.t. the declaration of incompatibilities"""

from .lib import is_py3k

if is_py3k:
    from .integermod_repr_test_py3 import test_integermod_repr
else:
    from .integermod_repr_test_py2 import test_integermod_repr

# vim: et sw=4 ts=4 ft=python
