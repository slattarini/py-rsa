#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests conversion of sequences of bytes into sequences of bits."""

def bytes_to_bits(bytes):
    """A generator that turn a generic sequence of bytes (iterables are
    ok) into an iterable yielding single bits (represented by the integers
    '0' an '1')."""
    masks = [ 1 << i for i in range(0, 8) ]
    for byte in bytes:
        for bit in [ (ord(byte) & masks[i]) >> i for i in range(0, 8) ]:
            yield bit

from tests.lib import with_params, pytest_generate_tests

def infinite_iteration(x):
    while True:
        yield x

def no_iteration():
    while False:
        yield None
    return

def seq2gen(seq):
    for x in seq:
        yield x

known_io = [
    dict(
        bytes = '',
        bits = (),
    ),
    dict(
        bytes = '\x00',
        bits = (0, 0, 0, 0, 0, 0, 0, 0),
    ),
    dict(
        bytes = '\x01',
        bits = (1, 0, 0, 0, 0, 0, 0, 0),
    ),
    dict(
        bytes = '\x80',
        bits = (0, 0, 0, 0, 0, 0, 0, 1),
    ),
    dict(
        bytes = '\xff\x00',
        bits = (1, 1, 1, 1, 1, 1, 1, 1,
                0, 0, 0, 0, 0, 0, 0, 0),
    ),
    dict(
        bytes = '\x88\x8e\x8f\x53\x35\xac',
        bits = (0, 0, 0, 1, 0, 0, 0, 1,
                0, 1, 1, 1, 0, 0, 0, 1,
                1, 1, 1, 1, 0, 0, 0, 1,
                1, 1, 0, 0, 1, 0, 1, 0,
                1, 0, 1, 0, 1, 1, 0, 0,
                0, 0, 1, 1, 0, 1, 0, 1,),
    ),
]

@with_params(known_io)
def test_known_io(bytes, bits):
    assert tuple(bytes_to_bits(bytes)) == bits

@with_params(known_io)
def test_known_io_repeated(bytes, bits):
    assert tuple(bytes_to_bits(bytes * 155)) == bits * 155

@with_params(known_io)
def test_known_io_generator(bytes, bits):
    assert tuple(bytes_to_bits(seq2gen(bytes))) == bits

@with_params([ '', [], (), no_iteration(), ], 'empty_seq')
def test_empty(empty_seq):
    for dummy in bytes_to_bits(empty_seq):
        assert False, "unexpected iteration"

def test_infinite_0():
    i = 1
    for bit in bytes_to_bits(infinite_iteration('\000')):
        assert bit == 0, "i = %s, exp = %s, got = %s" % (i, 0, bit)
        if i > 1001:
            break
        i += 1

def test_infinite_1():
    i = 1
    for bit in bytes_to_bits(infinite_iteration('\xff')):
        assert bit == 1, "i = %s, exp = %s, got = %s" % (i, 0, bit)
        if i > 4096:
            break
        i += 1

def test_infinite_10101010():
    i = 1
    for bit in bytes_to_bits(infinite_iteration('\125')):
        exp = i % 2
        assert bit == exp, "i = %s, exp = %s, got = %s" % (i, exp, bit)
        if i > 999:
            break
        i += 1

# vim: et sw=4 ts=4 ft=python
