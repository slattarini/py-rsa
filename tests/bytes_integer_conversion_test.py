#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests mixin for conversion between generic sequences of bytes and
positive integers."""
import sys
import pytest
from RSA import ByteSequenceConversionMixin
from tests.pyrsa_testlib import with_params, pytest_generate_tests

converter = ByteSequenceConversionMixin()

test_known_input_output = [
    dict(o = '', i = 1),
    dict(o = '\000', i = 256),
    dict(o = '\001', i = 257),
    dict(o = '\377', i = 511),
    dict(o = '\000\000', i = 256**2),
    dict(o = '\000\001', i = 256*257),
    dict(o = '\001\000', i = 1 + 256**2),
    dict(o = '\000' * 100, i = 1 << 800),
    dict(o = '\000' * 101, i = 1 << 808),
    dict(o = 'a', i = 353),
    dict(o = 'x', i = 376),
    dict(o = 'abc', i = 23290465),
]

some_files = [
    '/etc/passwd',
    '/etc/fstab',
    '/etc/aliases.db',
    '/etc/localtime',
    # ELF executables tend to end with null bytes
#    getattr(sys, 'executable', ''),
    '/bin/echo',
    '/bin/cat',
]

def check_converter_reversibility(bytes):
    __tracebackhide__ = True
    assert converter.i2o(converter.o2i(bytes))

@with_params(test_known_input_output)
def test_o2i(o, i):
    assert converter.o2i(o) == i

@with_params(test_known_input_output)
def test_i2o(o, i):
    assert converter.i2o(i) == o

@with_params(some_files, 'path')
def test_converter_reversibility_from_file(path):
    try:
        bytes = open(path).read()
    except IOError:
        pytest.skip("failed to read content of file %s" % path)
    else:
        check_converter_reversibility(bytes)

# Let's try with some random integers.
# XXX

# vim: et sw=4 ts=4 ft=python
