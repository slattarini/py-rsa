#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Test our methods for [byte sequences] <--> [integer sequences]
conversions."""

import pytest
import random
from tests.lib import with_params, without_duplicates, pytest_generate_tests
from tests.lib import infinite_iteration, seq2gen, TestError
from RSA import ByteSequenceEncrypter, CryptoValueError, CryptoException

# Return "some" random positive integers that requires, to be represented,
# a number of bits `n_bits' with l <= nbits <= u.
def some_ints_with_bits(l, u, count=20):
    assert (1 <= l <= u and count > 0)
    L = 1 << (l - 1)
    U = (1 << u) - 1
    yield L
    yield L + 1
    for i in range(0, count):
        yield random.randint(L, U)
    yield U - 1
    yield U

# Return a random list of integers n that should be represented by the
# given number of bytes `n_byte'.  This means that n should require, to
# be represented, a number of bits 'x' with:
#   8 * n_byte - 7 <= x <= 8 * n_byte
def n_with_bytes(n_byte):
    return some_ints_with_bits(8 * n_byte - 7, 8 * n_byte)

# Return a random list of integers that, when used as the 'n' entry of a
# key, should cause the plaintexts to be broken into chunks of size (in
# bytes) = n_byte.
def n_with_plaintext_chunklen(n_byte):
    return some_ints_with_bits(8 * n_byte + 9, 8 * n_byte + 16)

length_data = eval("""[
#------------5432109876543210987654321---------------------------
    dict(n=0b........................., p_len=None, n_len=None),
    dict(n=0b........................1, p_len=None, n_len=None),
    dict(n=0b.......................1., p_len=None, n_len=None),
    dict(n=0b......................1.., p_len=None, n_len=None),
    dict(n=0b......................111, p_len=None, n_len=None),
    dict(n=0b.....................1..., p_len=None, n_len=None),
    dict(n=0b..................1......, p_len=None, n_len=None),
    dict(n=0b.................1......., p_len=None, n_len=None),
    dict(n=0b.................11111111, p_len=None, n_len=None),
#------------5432109876543210987654321---------------------------
    dict(n=0b................1........, p_len=None, n_len=None),
    dict(n=0b................1.1.11.11, p_len=None, n_len=None),
    dict(n=0b...............1........., p_len=None, n_len=None),
    dict(n=0b..............1.........., p_len=None, n_len=None),
    dict(n=0b.............1..........., p_len=None, n_len=None),
    dict(n=0b...........1............., p_len=None, n_len=None),
    dict(n=0b...........1..11..11..1.1, p_len=None, n_len=None),
    dict(n=0b..........1.............., p_len=None, n_len=None),
    dict(n=0b.........1..............., p_len=None, n_len=None),
    dict(n=0b.........1111111111111111, p_len=None, n_len=None),
#------------5432109876543210987654321---------------------------
    dict(n=0b........1................, p_len=1, n_len=3),
    dict(n=0b........11111111111111111, p_len=1, n_len=3),
    dict(n=0b.......1................., p_len=1, n_len=3),
    dict(n=0b.......1.1.1.1.1.1.1.1.1., p_len=1, n_len=3),
    dict(n=0b......1.................., p_len=1, n_len=3),
    dict(n=0b.....1..................., p_len=1, n_len=3),
    dict(n=0b....1...................., p_len=1, n_len=3),
    dict(n=0b...1....................., p_len=1, n_len=3),
    dict(n=0b..1......................, p_len=1, n_len=3),
    dict(n=0b.1......................., p_len=1, n_len=3),
    dict(n=0b.111111111111111111111111, p_len=1, n_len=3),
#------------5432109876543210987654321---------------------
    dict(n=0b1........................, p_len=2, n_len=4),
#----------------------------------------------------------
    dict(n=1<<26,      p_len=2,   n_len=4),
    dict(n=1<<27,      p_len=2,   n_len=4),
    dict(n=1<<28,      p_len=2,   n_len=4),
    dict(n=1<<29,      p_len=2,   n_len=4),
    dict(n=1<<30,      p_len=2,   n_len=4),
    dict(n=1<<31,      p_len=2,   n_len=4),
    dict(n=1<<32 - 1,  p_len=2,   n_len=4),
    dict(n=1<<32,      p_len=3,   n_len=5),
    dict(n=1<<33,      p_len=3,   n_len=5),
    dict(n=1<<47,      p_len=4,   n_len=6),
    dict(n=1<<48 - 1,  p_len=4,   n_len=6),
    dict(n=1<<48,      p_len=5,   n_len=7),
    dict(n=1<<49,      p_len=5,   n_len=7),
    dict(n=1<<800,     p_len=99,  n_len=101),
    dict(n=1<<807,     p_len=99,  n_len=101),
    dict(n=1<<808 - 1, p_len=99,  n_len=101),
    dict(n=1<<808,     p_len=100, n_len=102),
    dict(n=1<<809,     p_len=100, n_len=102),
#-------------------------------------------------------
]""".replace('.', '0'))

# XXX: some largish known I/O pairs would be nice.
def generate_cipher_conversion_data():
    data = []
    for n_byte in (3, 4, 5, 12, 32, 1000):
        for n in n_with_bytes(n_byte):
            data.append(dict(n=n, bytes='', ints=[]))
            data.append(dict(n=n, bytes='\x00' * n_byte, ints=[0x00]))
            for x in [
                '00', '01', '02', '03', '07', '09', '0a', '41', '61',
                '6a', '7e', '80', '81', '94', 'f1', 'fe', 'ff'
            ]:
                bytes = eval("'\\x%s'" % x)
                bytes += '\x00' * (n_byte - 1)
                ints = [eval("0x%s" % x)]
                data.append(dict(n=n, bytes=bytes, ints=ints))
            for x in [
                '00:00', '00:01', '01:00', '02:03', '07:0a', '43:67',
                '5a:f3', '7e:0f', '80:81', '94:b1', 'bc:ff', '1b:ea',
            ]:
                x1, x2 = x.split(':')
                bytes = eval("'\\x%s\\x%s'" % (x1, x2))
                bytes +='\x00' * (n_byte - 2)
                ints = [eval("0x%s%s" % (x2, x1))]
                data.append(dict(n=n, bytes=bytes, ints=ints))
    raw_data = [
        dict(
            n_byte = 3,
            bytes = '\x44\x3a\x00\x11\xfe\x00',
            ints = [0x3a44, 0xfe11],
        ),
    ]
    for d in raw_data:
        n_byte = d['n_byte']
        del d['n_byte']
        for n in n_with_bytes(n_byte):
            data.append(dict(d, n=n))
    return data

def generate_plain_conversion_data():
    data = []
    miscellaneous_integers_with_17_or_more_bits = [
        1<<16, 1<<17, 1<<23, 1<<24, 1<<25, 1<<31, 1<<32, 1<<64, 1<<65,
        2**16 + 1, 2**16 + 55, 2**16 + 2**13, 2**17 - 1, 2**17 + 523,
        2**31 + 45673, 2**32 + 72, 3 * 2**32 + 679, 2**50, 3**100,
        5**123 + 7**43, 13**57 + 12, 2**1000,  2**2000 + 3**1000
    ]
    for n in miscellaneous_integers_with_17_or_more_bits:
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
        for n in n_with_plaintext_chunklen(n_byte):
            data.append(dict(d, n=n))
    return data

def generate_unpadded_plain_integer_data():
    data = []
    for i in range(0x00, 0xff):
        data.append(dict(n=1<<16, ints=[i]))
        data.append(dict(n=1<<17-1, ints=[0xff, i]))
        data.append(dict(n=3**16, ints=[i, 0xff]))
    data.append(dict(n=1<<24, ints=[0xfe0000, 0xff]))
    data.append(dict(n=1<<25, ints=[0xff000,  0xf00000]))
    data.append(dict(n=(1<<28 + 1), ints=[0x1f47a3c]))
    return data

def generate_too_big_plain_integer_data():
    return [
        dict(n=1<<16, ints=[0xff0000]),
        dict(n=1<<16, ints=[0xff003a]),
        dict(n=1<<17, ints=[0xff16a8]),
        dict(n=1<<17, ints=[0xff358e]),
        dict(n=(1<<24) - 1, ints=[0xffffff]),
        dict(n=1<<24, ints=[0xff000000]),
    ]

def generate_unpadded_cipher_text_data():
    data = []
    for n_byte in (3, 4, 5, 24, 1000):
        for n in n_with_bytes(n_byte):
            for i in set([1, 2, n_byte / 2, n_byte - 2, n_byte - 1]):
                for j in (0, 1, 2, 4, 23):
                    data.append(dict(n=n, bytes='a'*i + 'b'*n_byte*j))
    return data

def generate_too_big_cipher_integer_data():
    return [
        dict(n=1<<16, ints=[1<<24]),
        dict(n=1<<19, ints=[3**17]),
        dict(n=(1<<24) - 1, ints=[1<<24]),
        dict(n=1<<24, ints=[(1<<32) + 5]),
        dict(n=1<<24, ints=[0x12ab08ff2367c]),
        dict(n=(1<<1000) - 1, ints=[1<<1000]),
    ]

@without_duplicates
def generate_too_small_n():
    list_of_small_n = []
    for d in length_data:
        if d['n_len'] is None:
            list_of_small_n.append(d['n'])
    for i in 1, 2:
        list_of_small_n.extend(n_with_bytes(i))
    return list_of_small_n

plain_conversion_data = generate_plain_conversion_data()
unpadded_plain_integer_data = generate_unpadded_plain_integer_data()
too_big_plain_integer_data = generate_too_big_plain_integer_data()
cipher_conversion_data = generate_cipher_conversion_data()
unpadded_cipher_text_data = generate_unpadded_cipher_text_data()
too_big_cipher_integer_data = generate_too_big_cipher_integer_data()
too_small_n = generate_too_small_n()

class ByteSeqConverter(ByteSequenceEncrypter):
    def __init__(self, x):
        self._setup_byte_lengths(x)


# -------------------- #
#  Go with the tests.  #
# -------------------- #


@with_params([dict(n=d['n'], chunk_length=d['p_len'])
                for d in length_data if d['p_len'] is not None])
def test_plain_chunk_byte_length(n, chunk_length):
    assert chunk_length == ByteSeqConverter(n).plain_chunk_byte_length

@with_params([dict(n=d['n'], n_length=d['n_len'])
                for d in length_data if d['n_len'] is not None])
def test_n_byte_length(n, n_length):
    assert n_length == ByteSeqConverter(n).n_byte_length


@with_params(too_small_n, 'n')
def test_plain_chunk_length_key_too_small(n):
    pytest.raises(CryptoValueError, "ByteSeqConverter(n)")


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


@with_params(cipher_conversion_data)
def test_c2i(n, bytes, ints):
    assert list(ByteSeqConverter(n).c2i(bytes)) == ints

@with_params(cipher_conversion_data)
def test_c2i_with_generator(n, bytes, ints):
    assert list(ByteSeqConverter(n).c2i(seq2gen(bytes))) == ints

@with_params(cipher_conversion_data)
def test_i2c(n, bytes, ints):
    assert ''.join((ByteSeqConverter(n).i2c(ints))) == bytes

@with_params(cipher_conversion_data)
def test_i2c_with_generator(n, bytes, ints):
    assert ''.join((ByteSeqConverter(n).i2c(seq2gen(ints)))) == bytes


@with_params(unpadded_plain_integer_data)
def test_i2p_unpadded(n, ints):
    converter = ByteSeqConverter(n)
    pytest.raises(CryptoValueError,
                  "for _ in converter.i2p(ints): pass")

@with_params(unpadded_plain_integer_data)
def test_i2p_unpadded_with_generator(n, ints):
    converter = ByteSeqConverter(n)
    pytest.raises(CryptoValueError,
                  "tuple(converter.i2p(seq2gen(ints)))")


@with_params(too_big_plain_integer_data)
def test_i2p_too_big(n, ints):
    converter = ByteSeqConverter(n)
    pytest.raises(CryptoValueError,
                  "for _ in converter.i2p(ints): pass")

@with_params(too_big_plain_integer_data)
def test_i2p_too_big_with_generator(n, ints):
    converter = ByteSeqConverter(n)
    pytest.raises(CryptoValueError,
                  "tuple(converter.i2p(seq2gen(ints)))")


@with_params(unpadded_cipher_text_data)
def test_c2i_unpadded(n, bytes):
    converter = ByteSeqConverter(n)
    pytest.raises(CryptoValueError,
                  "for _ in converter.c2i(bytes): pass")

@with_params(unpadded_cipher_text_data)
def test_c2i_unpadded_with_generator(n, bytes):
    converter = ByteSeqConverter(n)
    pytest.raises(CryptoValueError,
                  "tuple(converter.c2i(seq2gen(bytes)))")


@with_params(too_big_cipher_integer_data)
def test_i2c_too_big(n, ints):
    converter = ByteSeqConverter(n)
    pytest.raises(CryptoValueError,
                  "for _ in converter.i2c(ints): pass")


@with_params(too_big_cipher_integer_data)
def test_i2c_too_big_with_generator(n, ints):
    converter = ByteSeqConverter(n)
    pytest.raises(CryptoValueError,
                  "tuple(converter.i2c(seq2gen(ints)))")


@with_params([2 ,3, 4, 5, 100, 997], 'n_byte')
@with_params([1, 2 ,3, 10, 97, 128], 'n_iter')
@with_params(['p2i', 'i2p'], 'convtype')
# FIXME: using a timeout would be better than risking to let the
# test hang in case of failure...
def test_p2i_or_i2p_with_infinite_generator(n_byte, n_iter, convtype):
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

# Check that we can convert also "big" byte sequences (~ 200M) in a
# reasonable time.
# FIXME: having a timeout here would be better than risking to have
# the testsuite almost hang ...
@with_params([1 << 16, 1 << 1511], 'n')
def test_p2i_large(n):
    def gen_bytes():
        for i in range(0, 20):
            fp = open("random.bytes")
            while True:
                byte = fp.read(1)
                if byte:
                    yield byte
                else:
                    fp.close()
                    break
    for _ in ByteSeqConverter(n).p2i(gen_bytes()): pass


# vim: et sw=4 ts=4 ft=python
