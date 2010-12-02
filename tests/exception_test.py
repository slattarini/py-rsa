#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Unit tests for custom exceptions used by the RSA.py"""

import pytest
import RSA

### DATA

exceptions_info = {
    'IMException':  {
        'superclasses': (Exception,),
    },
    'IMRuntimeError': {
        'superclasses': (Exception, 'IMException', RuntimeError),
    },
    'IMTypeError': {
        'superclasses': (Exception, 'IMException', TypeError),
    },
    'IMValueError': {
        'superclasses': (Exception, 'IMException', ValueError),
    },
}

# pytest special hook function to generate test input.
def pytest_generate_tests(metafunc):
    funcargs = metafunc.funcargnames
    addcall = lambda **d: metafunc.addcall(funcargs=d)
    if set(funcargs) == set(["exc"]):
        for exc in exceptions_info:
            addcall(exc=exc)
    elif set(funcargs) == set(["exc", "su_exc"]):
        for exc in exceptions_info:
            for su_exc in exceptions_info[exc]['superclasses']:
                addcall(exc=exc, su_exc=su_exc)
    else: # sanity check
        raise RuntimeError("bad funcargsnames list: %r" % funcargs)

### TESTS

def fix_exception(exc):
    if isinstance(exc, basestring):
        exc = getattr(RSA, exc)
    return exc

def test_exc_subclass(exc, su_exc):
    exc, su_exc = map(fix_exception, (exc, su_exc))
    issubclass(exc, su_exc),

def test_exc_subexception(exc, su_exc):
    exc, su_exc = map(fix_exception, (exc, su_exc))
    pytest.raises(su_exc, "raise exc")

def test_exc_raisable(exc):
    exc = fix_exception(exc)
    pytest.raises(exc, "raise exc")

# vim: et sw=4 ts=4 ft=python
