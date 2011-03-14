#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of RSA.py testsuite.

"""Unit tests for the RSA.py's implementation of euclidean algorithm"""

from RSA import gcd, extended_gcd
from .lib import is_py3k, pytest_generate_tests, with_params

## PY3K COMPATIBILITY

def assert_is_integer(obj):
    __tracebackhide__ = True
    if is_py3k:
        assert type(obj) == int
    else:
        assert type(obj) in (int, long)


### DATA

known_values = [] # updated later

# most of these obtained with GAP
small_known_values = [
    dict(a = 0,    b = 0,    d = 0,  x = 0,  y = 0  ),
    dict(a = 1,    b = 1,    d = 1,  x = 0,  y = 1  ),
    dict(a = 1,    b = 0,    d = 1,  x = 1,  y = 0  ),
    dict(a = 1,    b = 10,   d = 1,  x = 1,  y = 0  ),
    dict(a = 1,    b = 7,    d = 1,  x = 1,  y = 0  ),
    dict(a = 7,    b = 1,    d = 1,  x = 0,  y = 1  ),
    dict(a = 100,  b = 1,    d = 1,  x = 0,  y = 1  ),
    dict(a = 99,   b = 0,    d = 99, x = 1,  y = 0  ),
    dict(a = 10,   b = 100,  d = 10, x = 1,  y = 0  ),
    dict(a = 33,   b = 69,   d = 3,  x = -2, y = 1  ),
    dict(a = 33,   b = 121,  d = 11, x = 4,  y = -1 ),
    dict(a = 17,   b = 23,   d = 1,  x = -4, y = 3  ),
    dict(a = 124,  b = 123,  d = 1,  x = 1,  y = -1 ),
    dict(a = 128,  b = 42,   d = 2,  x = 1,  y = -3 ),
    dict(a = 117,  b = 27,   d = 9,  x = 1,  y = -4 ),
    dict(a = 125,  b = 95,   d = 5,  x = -3, y = 4  ),
    dict(a = 2059, b = 9088, d = 71, x = 53, y = -12),
]
known_values.extend(small_known_values)

equals_known_values = [
    dict(a=i, b=i, d=i, x=0, y=1)
      for i in [1, 2, 3, 11, 18, 25, 73, 77, 97, 99, 2**127 - 1, 2**10000]
]
known_values.extend(equals_known_values)

# most of these obtained with GAP
big_known_values = [
    dict(
        a = 1,
        b = 764704689598698726872634,
        d = 1,
        x = 1,
        y = 0,
    ),
    dict(
        a = 10,
        b = 764704689598698726872634,
        d = 2,
        x = 152940937919739745374527,
        y = -2,
    ),
    dict(
        a = 0,
        b = 764704689598698726872634,
        d = 764704689598698726872634,
        x = 0,
        y = 1,
    ),
    dict(
        a = 12335353157,
        b = 2357,
        d = 1,
        x = -327,
        y = 1711353620,
    ),
    dict(
        a = 1178452874508256245,
        b = 2425242147636098726872634,
        d = 1,
        x = -662680969444634878977239,
        y = 322004255981257034,
    ),
    dict(
        a = 34789549235789234782575559,
        b = 477634754359254785478547846,
        d = 11,
        x = 12832574912097442466160799,
        y = -934688049083163097679405,
    ),
    dict(
        a = 874676545378924762356334976340796379026,
        b = 373597465983037954479834723894764525,
        d = 1,
        x = -181462761587895153830932213436603799,
        y = 424845551355602155951010071828845332411,
    ),
    dict(
        a = 874654643176545378924762356334976340796379026,
        b = 37359574217465983037954479834723894764525,
        d = 3,
        x = -4753123804506568354291459060440194216747,
        y = 111279153798841651827292981194264417939739277,
    ),
]
known_values.extend(big_known_values)

# all the factors in the comments are primes (< 1000)
# most of values of x and y have been obtained with GAP
handcrafted_known_values = [
    dict(
        # a = 11^3 * 19^1 * 23^4 * 367^2 * 409^1 * 419^2 * 557^3 * 977^1
        # b = 5^2  * 19^3 * 23^1 * 367^1 * 409^2 * 419^1 * 557^2 * 977^3
        # d = 19 * 23 * 367 * 409 * 419 * 557^2 * 977
        a = 11555443865761506491653129797294029,
        b = 29352793027420220932728949662425,
        d = 8330859041729340257,
        x = -756103196117,
        y = 297658489646658,
    ),
    dict(
        # a = 5^28 * 11^19 * 373^2 * 379^3 * 383^5 * 389^2 * 397^2 * 401^3 * 409^1 * 419 * 433
        # b = 5^17 * 11^23 * 373^3 * 379^1 * 383^2 * 389^4 * 397^3 * 401^2 * 409^2 * 421 * 431
        # d = 5^17 * 11^19 * 373^2 * 379^1 * 383^2 * 389^2 * 397^2 * 401^2 * 409^1
        a = 16228891776666484556003101708773497512740920133501110213530703077854535765945911407470703125,
        b = 13783189861105577545653636200053354589935659816703552548978586631578732430267333984375,
        d = 566106032315592078927311947648176530482125911295935821533203125,
        x = 10687629537949505790929,
        y = -12584052375998679649673236496,
    ),
]
known_values.extend(handcrafted_known_values)

gcd_args = [dict(a=x['a'], b=x['b']) for x in known_values]
gcd_data = [dict(a=x['a'], b=x['b'], d=x['d']) for x in known_values]
egcd_data = known_values

### TESTS

@with_params(gcd_args)
def test_gcd_ret_type(a, b):
    assert_is_integer(gcd(a, b))

@with_params(gcd_data)
def test_gcd_known(a, b, d):
    assert gcd(a, b) == d

@with_params(gcd_args)
def test_gcd_commutative(a, b):
    assert gcd(a, b) == gcd(b, a)

@with_params(gcd_args)
def test_gcd_consistency(a ,b):
    d = gcd(a, b)
    if a == b == 0:
        assert (a == b == d == 0)
    elif a == 0:
        assert (a == 0 and d == b)
    elif b == 0:
        assert (b == 0 and d == a)
    else:
        assert (a % d == 0 and b % d == 0)

@with_params(gcd_args)
def test_egcd_seq_type(a, b):
    assert type(extended_gcd(a, b)) == tuple

@with_params(gcd_args)
def test_egcd_ret_type(a ,b):
    d, x, y = extended_gcd(a, b)
    assert_is_integer(d)
    assert_is_integer(x)
    assert_is_integer(y)

@with_params(egcd_data)
def test_egcd_known(a, b, d, x ,y):
    assert (d, x, y) == extended_gcd(a, b)

@with_params(gcd_args)
def test_egcd_reversed(a, b):
    if a != b:
        d0, x0, y0 = extended_gcd(a, b)
        d1, x1, y1 = extended_gcd(b ,a)
        assert (d0, x0, y0) == (d1, y1, x1)

@with_params(gcd_args)
def test_egcd_consistency(a, b):
    d, x, y = extended_gcd(a, b)
    if a == b == 0:
        assert d == x == y == 0
    elif a == 0:
        assert d == b and x == 0 and y == 1
    elif b == 0:
        assert d == a and x == 1 and y == 0
    else:
        qa = max(1, (a / d) / 2)
        qb = max(1, (b / d) / 2)
        assert (a % d == 0 and b % d == 0
                and a * x + b * y == d
                and -qb <= x <= qb
                and -qa <= y <= qa)

# vim: et sw=4 ts=4 ft=python
