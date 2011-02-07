#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for our implementation of RSA applied to generic sequences
of bytes."""

import pytest
import RSA
from tests.pyrsa_testlib import with_params, without_duplicates, \
                                pytest_generate_tests

def define_texts():
    texts = set()
    texts.add('')
    chars = [chr(x) for x in range(0, 256)]
    texts.update(chars)
    texts.update(['abcde', '123', 'x\012\015', ':\000\000', '\000\000@'])
    # Try that we can handle DEL and BACKSPACE characters.
    texts.update(['x\by', 'x\b\by', 'uv\b\bxy'])
    texts.update(['x\177y', 'x\177\177y', 'uv\177\177xy'])
    return texts
    for c1 in chars:
        for c2 in chars:
            texts.add("%s%s" % (c1, c2))
    texts.extend([c*50 for c in chars])
    texts.extend([c*10000 for c in chars])
    # Plaintext generated from `/dev/urandom'.
    texts.update("""\
]\222\360?n\317\320q\257D\332\317~\315v\270\365\347Q1cZ\342}`\251\321\
\223\266Q\206\267J\225R\221H\010\370\207\206\020\223\274\244\002\365\302\
24\0163\277'\316h\312\313B\223i\261\324n\007\254\375\324Q\276\005\325\320\
R\267\252\232\211Q\365\362\367\234\351$\035c\300c\022\336]\343\3019\002 L\
\322\365\320Cn\232eN}E'\006\037\331\336Uo\027\220\270\271\317\007G\245a\
\337s\205\256\241R\233\205\340&- \037r%\023)\336\233]7\332\246 -\301\327lI\
xh\336\364=\325\352r`\330(\226E\003\366Ge\346\355B9\274>J\015\264\334\217[\
\347\336\307\024\003m^\273f\367\362z\375(\000\334\265j\314\212\022O\261\
\347\304NY?Sd\343\234r*\326\000\375m\023\267>\347!\247\313\206)\247\024^j\
\300\336)O$\304\364kN\363\317o\005\306\0305S\233\353t\346G\213+V\2034\007I\
_P\235-\235iR\220\327\317w\005Z\034o9\333j*\000\231\230ao\347\375F\2077\
\243\337~"Vw\355sI\251zkD\223u\002T\331r\254\3150\033@\353Df\256\273\0132\
\205\013\003l\275\007i\257\305\355\305\260$\264\362\313\337n\277\333 \031K\
\3108>\257s|\301;Q\364\025\2450AH\214j\233f-DQ\037\232b\260\255\326Aho{A_\
\320\266[\376r\236\220G\255\\\220\332\365\220\207\365,\216\315\017\265\331\
y     a}\007\326'\022\335L\007\037\002Ff\247\275-\300\241\216_\307\352\233\
V\364q\206\264\332\245k\370\373\304\013\025@\023\267\224+k=`-\221\374\266`\
y\332\n\000\073""")
    return texts

rsa_keys_data = [

    dict(
        n = 35,
        p = 5,
        q = 7,
        e = 11,
    ),

    dict(
        n = 3233,
        p = 61,
        q = 53,
        e = 17,
    ),

    dict(
        n = 31243,
        p = 157,
        q = 199,
        e = 5,
    ),

    dict(
        n = (2**2281 - 1) * (2**2203 - 1),
        p = 2**2281 - 1,
        q = 2**2203 - 1,
        e = 2**61 - 1,
    ),

] # rsa_keys_data

plaintexts = define_texts()

# -------------------- #
#  Go with the tests.  #
# -------------------- #

@with_params(plaintexts, 'plaintext')
@with_params(rsa_keys_data)
def test_pubkey_encrypt_privkey_decrypt(n, p, q, e, plaintext):
    encrypter = RSA.ByteSequenceEncrypter(RSA.PublicKey(n, e))
    decrypter = RSA.ByteSequenceEncrypter(RSA.PrivateKey(p, q, e))
    ciphertext = encrypter.encrypt(plaintext)
    assert type(ciphertext) == str
    assert decrypter.decrypt(ciphertext) == plaintext

@with_params(plaintexts, 'plaintext')
@with_params(rsa_keys_data)
def test_privkey_encrypt_privkey_decrypt(n, p, q, e, plaintext):
    encrypter = RSA.ByteSequenceEncrypter(RSA.PrivateKey(p, q, e))
    ciphertext = encrypter.encrypt(plaintext)
    assert type(ciphertext) == str
    assert plaintext == encrypter.decrypt(ciphertext)

# vim: et sw=4 ts=4 ft=python
