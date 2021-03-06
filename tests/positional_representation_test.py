#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of RSA.py testsuite.

"""Tests internal routines for positional representation of integers."""

import pytest
from RSA import int_to_pos, pos_to_int
from .lib import with_params, pytest_generate_tests

# b is the base, n the integer, r its positional representation
# TODO: it should be easy to have more automatically-generated test
#       data here ...
test_data = [
    dict(
        b = 2,
        n = 1,
        r = [1],
    ),
    dict(
        b = 321,
        n = 1,
        r = [1],
    ),
    dict(
        b = 2,
        n = 10,
        r = [0, 1, 0, 1],
    ),
    dict(
        b = 5,
        n = 10,
        r = [0, 2],
    ),
    dict(
        b = 5,
        n = 38,
        r = [3, 2, 1],
    ),
    dict(
        b = 8,
        n = 0o1452565467362345,
        r = [5, 4, 3, 2, 6, 3, 7, 6, 4, 5, 6, 5, 2, 5, 4, 1],
    ),
    dict(
        b = 8,
        n = 0o1000000000000000,
        r = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    ),
    dict(
        b = 16,
        n = 0x1AF43E7,
        r = [7, 14, 3, 4, 15, 10, 1],
    ),
    dict(
        b = 16,
        n = 0x10AC230,
        r = [0, 3, 2, 12, 10, 0, 1],
    ),
    dict(
        b = 11,
        n = 233,
        r = [2, 10, 1],
    ),
    dict(
        b = 10,
        n = 10000,
        r = [0, 0, 0, 0, 1],
    ),
]

@with_params(test_data)
def test_pos_to_int(b, n, r):
    assert pos_to_int(r, b) == n

@with_params(test_data)
def test_int_to_pos(b, n, r):
    assert int_to_pos(n, b) == r

# vim: et sw=4 ts=4 ft=python
