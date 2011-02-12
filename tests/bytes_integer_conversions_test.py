#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Test our methods for [byte sequences] <--> [integer sequences]
conversions."""

import pytest
from tests.lib import with_params, without_duplicates, pytest_generate_tests
from tests.lib import infinite_iteration, seq2gen, TestError
from RSA import ByteSequenceEncrypter, CryptoException

# Return a list of integers that should cause the platexts to be broken
# into chunks of size (in bytes) = n_byte.  This means that n should
# require n_byte + 1 bytes to be represented, i.e. a number ob bits 'x'
# with  8 * n_byte + 8 <= x <= 8 * n_byte + 15.
def n_with_chunklen(n_byte):
    list_of_n = []
    n_bit = 8 * n_byte + 8
    for i in range(n_bit, n_bit + 8):
        n = 1 << i
        list_of_n.extend([n, n + 1, n + 16, n + 55])
        if i < n_bit + 7:
            list_of_n.extend([n * 3, n * 3 + 1, n * 3 + 74])
    return list_of_n

def generate_plain_conversion_data():
    data = []
    for n in (
        1<<16, 1<<17, 1<<23, 1<<24, 1<<25, 1<<31, 1<<32, 1<<64, 1<<65,
        2**16 + 1, 2**16 + 55, 2**16 + 2**13, 2**17 - 1, 2**17 + 523,
        2**31 + 45673, 2**32 + 72, 3 * 2**32 + 679, 2**50, 3**100,
        5**123 + 7**43, 13**57 + 12, 2**1000,  2**2000 + 3**1000
    ):
        data.append(dict(n=n, bytes='', ints=[]))
        data.append(dict(n=n, bytes='\000', ints=[0xff00]))
        data.append(dict(n=n, bytes='\001', ints=[0xff01]))
        if n.bit_length() > 32:
            data.append(dict(n=n, bytes='\000\000', ints=[0xff0000]))
            data.append(dict(n=n, bytes='\000\001', ints=[0xff0100]))
            data.append(dict(n=n, bytes='\001\000', ints=[0xff0001]))
            data.append(dict(n=n, bytes='\001\001', ints=[0xff0101]))
    raw_data = [
        dict(
            n_byte = 1,
            bytes = '\000\000',
            ints = [0xff00, 0xff00],
        ),
        dict(
            n_byte = 1,
            bytes = 'ab',
            ints = [0xff61, 0xff62],
        ),
        dict(
            n_byte = 1,
            bytes = 'abz',
            ints = [0xff61, 0xff62, 0xff7a],
        ),
        dict(
            n_byte = 2,
            bytes = '\000\000\000',
            ints = [0xff0000, 0xff00],
        ),
        dict(
            n_byte = 2,
            bytes = '\001\000\000',
            ints = [0xff0001, 0xff00],
        ),
        dict(
            n_byte = 2,
            bytes = '\000\000\001',
            ints = [0xff0000, 0xff01],
        ),
        dict(
            n_byte = 3,
            bytes = '\001\000\000',
            ints = [0xff000001],
        ),
        dict(
            n_byte = 3,
            bytes = '\000\000\001',
            ints = [0xff010000],
        ),
        dict(
            n_byte = 10,
            bytes = '0123456789',
            ints = [0xff39383736353433323130],
        ),
        dict(
            n_byte = 10,
            bytes = '0123456789\000',
            ints = [0xff39383736353433323130, 0xff00],
        ),
        dict(
            n_byte = 10,
            bytes = 'abcdefghijklmnopqrstuvwxyz',
            ints = [0xff6a696867666564636261,
                    0xff74737271706f6e6d6c6b,
                    0xff7a7978777675],
        ),
        dict(
            n_byte = 10,
            bytes = 'klmnopqrstabcdefghijuvwxyz',
            ints = [0xff74737271706f6e6d6c6b,
                    0xff6a696867666564636261,
                    0xff7a7978777675],
        ),
        dict(
            n_byte = 13,
            # courtesy of random.shuffle()
            bytes = 'wzqtdchpsvolkxargejyubfnim',
            ints = [0xff6b6c6f76737068636474717a77,
                    0xff6d696e666275796a6567726178],
        ),
        dict(
            n_byte = 14,
            bytes = 'ababababababababababababab',
            ints = [0xff6261626162616261626162616261,
                    0xff626162616261626162616261],
        ),
        dict(
            n_byte = 15,
            bytes = 'ababababababababababababab',
            ints = [0xff616261626162616261626162616261,
                    0xff6261626162616261626162],
        ),
        dict(
            n_byte = 1,
            bytes = ''.join([chr(i) for i in range(0, 256)]),
            ints = [0xff00 + i for i in range(0, 256)],
        ),
        dict(
            # Finally a "nice" "stress test".
            n_byte = 22,
            bytes = ''.join([chr(i) for i in range(0, 256)]),
            ints = [0xff1514131211100f0e0d0c0b0a09080706050403020100,
                    0xff2b2a292827262524232221201f1e1d1c1b1a19181716,
                    0xff41403f3e3d3c3b3a393837363534333231302f2e2d2c,
                    0xff57565554535251504f4e4d4c4b4a4948474645444342,
                    0xff6d6c6b6a696867666564636261605f5e5d5c5b5a5958,
                    0xff838281807f7e7d7c7b7a797877767574737271706f6e,
                    0xff999897969594939291908f8e8d8c8b8a898887868584,
                    0xffafaeadacabaaa9a8a7a6a5a4a3a2a1a09f9e9d9c9b9a,
                    0xffc5c4c3c2c1c0bfbebdbcbbbab9b8b7b6b5b4b3b2b1b0,
                    0xffdbdad9d8d7d6d5d4d3d2d1d0cfcecdcccbcac9c8c7c6,
                    0xfff1f0efeeedecebeae9e8e7e6e5e4e3e2e1e0dfdedddc,
                    0xfffffefdfcfbfaf9f8f7f6f5f4f3f2],
        ),
    ]
    for d in raw_data:
        n_byte = d['n_byte']
        del d['n_byte']
        for n in n_with_chunklen(n_byte):
            data.append(dict(d, n=n))
    return data

plain_conversion_data = generate_plain_conversion_data()

chunk_length_data = eval("""[
#------------5432109876543210987654321------------------
    dict(n=0b........................., chunk_length=0),
    dict(n=0b........................1, chunk_length=0),
    dict(n=0b.......................1., chunk_length=0),
    dict(n=0b......................1.., chunk_length=0),
    dict(n=0b......................111, chunk_length=0),
    dict(n=0b.....................1..., chunk_length=0),
    dict(n=0b..................1......, chunk_length=0),
    dict(n=0b.................1......., chunk_length=0),
    dict(n=0b.................11111111, chunk_length=0),
#------------5432109876543210987654321------------------
    dict(n=0b................1........, chunk_length=1),
    dict(n=0b................1.1.11.11, chunk_length=1),
    dict(n=0b...............1........., chunk_length=1),
    dict(n=0b..............1.........., chunk_length=1),
    dict(n=0b.............1..........., chunk_length=1),
    dict(n=0b...........1............., chunk_length=1),
    dict(n=0b...........1..11..11..1.1, chunk_length=1),
    dict(n=0b..........1.............., chunk_length=1),
    dict(n=0b.........1..............., chunk_length=1),
    dict(n=0b.........1111111111111111, chunk_length=1),
#------------5432109876543210987654321------------------
    dict(n=0b........1................, chunk_length=2),
    dict(n=0b........11111111111111111, chunk_length=2),
    dict(n=0b.......1................., chunk_length=2),
    dict(n=0b.......1.1.1.1.1.1.1.1.1., chunk_length=2),
    dict(n=0b......1.................., chunk_length=2),
    dict(n=0b.....1..................., chunk_length=2),
    dict(n=0b....1...................., chunk_length=2),
    dict(n=0b...1....................., chunk_length=2),
    dict(n=0b..1......................, chunk_length=2),
    dict(n=0b.1......................., chunk_length=2),
    dict(n=0b.111111111111111111111111, chunk_length=2),
#------------5432109876543210987654321------------------
    dict(n=0b1........................, chunk_length=3),
#-------------------------------------------------------
    dict(n=1<<26,      chunk_length=3),
    dict(n=1<<27,      chunk_length=3),
    dict(n=1<<28,      chunk_length=3),
    dict(n=1<<29,      chunk_length=3),
    dict(n=1<<30,      chunk_length=3),
    dict(n=1<<31,      chunk_length=3),
    dict(n=1<<32 - 1,  chunk_length=3),
    dict(n=1<<32,      chunk_length=4),
    dict(n=1<<800,     chunk_length=100),
    dict(n=1<<807,     chunk_length=100),
    dict(n=1<<808 - 1, chunk_length=100),
    dict(n=1<<808,     chunk_length=101),
    dict(n=1<<809,     chunk_length=101),
#-------------------------------------------------------
]""".replace('.', '0'))

class ByteSeqConverter(ByteSequenceEncrypter):
    def __init__(self, x):
        self._setup_chunk_length(x)

# -------------------- #
#  Go with the tests.  #
# -------------------- #

@with_params(chunk_length_data)
def test_chunk_length(n, chunk_length):
    assert chunk_length == ByteSeqConverter(n).chunk_byte_length

@with_params(plain_conversion_data)
def test_p2i(n, bytes, ints):
    assert list(ByteSeqConverter(n).p2i(bytes)) == ints

@with_params(plain_conversion_data)
def test_p2i_with_generator(n, bytes, ints):
    assert list(ByteSeqConverter(n).p2i(seq2gen(bytes))) == ints

@with_params(plain_conversion_data)
def test_i2p(n, bytes, ints):
    assert ''.join((ByteSeqConverter(n).i2p(ints))) == bytes

@with_params(plain_conversion_data)
def test_i2p_with_generator(n, bytes, ints):
    assert ''.join((ByteSeqConverter(n).i2p(seq2gen(ints)))) == bytes

@with_params([2 ,3, 4, 5, 100, 997], 'n_byte')
@with_params([1, 2 ,3, 10, 97, 128], 'n_iter')
@with_params(['p2i', 'i2p'], 'convtype')
def test_p2i_or_i2p_with_infinite_generator(n_byte, n_iter, convtype):
    # TODO: using a timeout would be better than risking to let the
    # test hang in case of failure...
    iter_count = 0
    character = 'a'
    string = character * (n_byte - 1)
    integer = int('0xff' + '61' * (n_byte - 1), 16)
    n = 1 << n_byte * 8
    if convtype == 'p2i':
        iterator = ByteSeqConverter(n).p2i(infinite_iteration(character))
        chunk_expected = integer
    elif convtype == 'i2p':
        iterator = ByteSeqConverter(n).i2p(infinite_iteration(integer))
        chunk_expected = string
    else:
        raise TestError("invalid 'convtype' param: '%s'" % convtype)
    for chunk_got in iterator:
        iter_count += 1
        assert chunk_expected == chunk_got
        if iter_count >= n_iter:
            break

@with_params([1 << i for i in range(0, 16)] +
             [3, 55, 80, 157, 999, 1000, 63123, 2**16 - 1], 'n')
@with_params(['', '\000', 'a', 'bc', 'x'*10, 'x'*773], 'bytes')
def test_p2i_key_too_small(n, bytes):
    pytest.raises(CryptoException,
                  "for _ in ByteSeqConverter(n).p2i(bytes): pass")

# vim: et sw=4 ts=4 ft=python
