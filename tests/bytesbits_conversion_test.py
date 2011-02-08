#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests conversion of sequences of bytes into/from sequences of bits."""

def bytes_to_bits(bytes):
    """A generator that turn a generic sequence of bytes into an iterable
    yielding single bits (represented by the integers 0 and 1)."""
    masks = [ 1 << i for i in range(0, 8) ]
    for byte in bytes:
        for bit in [ (ord(byte) & masks[i]) >> i for i in range(0, 8) ]:
            yield bit

def bits_to_bytes(bits):
    """A generator that turn a generic sequence of bits (represented
    by the integers 0 and 1) into an iterable yielding whole bytes.
    If the total number of bits is not divisible by 8, a ValueError
    exception is raised"""
    count = 0
    one_byte_bits = []
    for bit in bits:
        one_byte_bits.append(bit)
        count += 1
        if count == 8:
            assert(len(one_byte_bits) == 8) # sanity check
            byte = chr(sum([one_byte_bits[i] << i for i in range(0, 8)]))
            one_byte_bits = []
            count = 0
            yield byte
    if count != 0:
        raise ValueError("the number ob bits read is not a multiple of 8")


from tests.lib import with_params, pytest_generate_tests

def infinite_iteration(*lst):
    while True:
        for x in lst:
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
        bytes = '\x00\xff',
        bits = (0, 0, 0, 0, 0, 0, 0, 0,
                1, 1, 1, 1, 1, 1, 1, 1),
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

repeats = [2, 3, 5, 10, 11, 16, 21, 24, 57, 65, 100, 243, 641,
           2 * 73 * 97, 10**5]

@with_params(known_io)
def test_known_io_by2bi(bytes, bits):
    assert tuple(bytes_to_bits(bytes)) == bits

@with_params(known_io)
@with_params(repeats, 'repeat')
def test_known_io_repeated_by2bi(bytes, bits, repeat):
    assert tuple(bytes_to_bits(bytes * repeat)) == bits * repeat

@with_params(known_io)
def test_known_io_generator_by2bi(bytes, bits):
    assert tuple(bytes_to_bits(seq2gen(bytes))) == bits

@with_params([ '', [], (), no_iteration(), ], 'empty_seq')
def test_empty_by2bi(empty_seq):
    for dummy in bytes_to_bits(empty_seq):
        assert False, "unexpected iteration"

@with_params(known_io)
def test_known_io_bi2by(bytes, bits):
    assert ''.join(bits_to_bytes(bits)) == bytes

@with_params(known_io)
@with_params(repeats, 'repeat')
def test_known_io_repeated_bi2by(bytes, bits, repeat):
    assert ''.join(bits_to_bytes(bits * repeat)) == bytes * repeat

@with_params(known_io)
def test_known_io_generator_bi2by(bytes, bits):
    assert ''.join(bits_to_bytes(seq2gen(bits))) == bytes

@with_params([ '', [], (), no_iteration(), ], 'empty_seq')
def test_empty_bi2by(empty_seq):
    for dummy in bits_to_bytes(empty_seq):
        assert False, "unexpected iteration"

def test_infinite_0_by2bi():
    i = 1
    for bit in bytes_to_bits(infinite_iteration('\000')):
        assert (bit == 0,
                "i = %u, exp = %r, got = %r" % (i, 0, bit))
        if i > 1001:
            break
        i += 1

def test_infinite_0_bi2by():
    i = 1
    for byte in bits_to_bytes(infinite_iteration(0)):
        assert (byte == '\0',
                "i = %u, exp = %r, got = %r" % (i, 0, byte))
        if i > 547:
            break
        i += 1

def test_infinite_1_by2bi():
    i = 1
    for bit in bytes_to_bits(infinite_iteration('\xff')):
        assert (bit == 1,
                "i = %s, exp = %s, got = %s" % (i, 0, bit))
        if i > 4096:
            break
        i += 1

def test_infinite_1_bi2by():
    i = 1
    for byte in bits_to_bytes(infinite_iteration(1)):
        assert (byte == '\xff',
                "i = %u, exp = %r, got = %r" % (i, 0, byte))
        if i > 5239:
            break
        i += 1

def test_infinite_10101010_by2bi():
    i = 1
    for bit in bytes_to_bits(infinite_iteration('\x55')):
        exp = i % 2
        assert (bit == exp,
                "i = %u, exp = %r, got = %r" % (i, exp, bit))
        if i > 999:
            break
        i += 1

def test_infinite_10101010_bi2by():
    i = 1
    for byte in bits_to_bytes(infinite_iteration(1, 0, 1, 0, 1, 0, 1, 0)):
        assert (byte == '\x55',
                "i = %u, exp = %r, got = %r" % (i, '\x55', byte))
        if i > 773:
            break
        i += 1

# vim: et sw=4 ts=4 ft=python
