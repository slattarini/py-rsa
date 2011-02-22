#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for our implementation of RSA applied to generic sequences
of bytes."""

from RSA import BinaryEncrypter, PublicKey, PrivateKey
from tests.keys import keys as keys_dict
from tests.lib import with_params, without_duplicates, pytest_generate_tests

keys_list = [ keys_dict[tag] for tag in keys_dict ]

def define_texts():
    texts = set()
    texts.add('')
    chars = [chr(x) for x in range(0, 256)]
    texts.update(chars)
    texts.update(['abcde', '123', 'x\012\015', ':\000\000', '\000\000@'])
    # Line feed, carriage return, and null bytes
    texts.update(['x\n\n', '\n\n\n', 'x\r\r', '\r\r\r'])
    texts.update(['\n\r\n', '\r\n\r', '\000\000\n\000', '\n\r\n\r'])
    # Try that we can handle DEL and BACKSPACE characters.
    texts.update(['x\by', 'x\b\by', 'uv\b\bxy'])
    texts.update(['x\177y', 'x\177\177y', 'uv\177\177xy'])
    return texts
    for c1 in chars:
        for c2 in chars:
            texts.add("%s%s" % (c1, c2))
    texts.extend([c*50 for c in chars])
    texts.extend([c*23451 for c in ['\0', 'a', '\177', 'ab\177xy01@:\007']])
    # Plaintexts generated from `/dev/urandom'.
    rand1 = """\
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
y\332\n\000\073\
"""
    rand2 = """\
\021|\026\3244PTq\361dX6\277\372\015crmD\263\277\247!\325\343hy(;\375Z9D\
\032\317\334\002\024\301\244\341\246R\344\024\374\212\212:\237B\261\327e,s\
j${\\\235\337\250j\204\n\243en\241n\264,\210\321P<Q\2072\251"\000\262\260\
\341\201       \234\311\330\234H\334\231\277>?T_\036.\263\242%\302\335\016\
\217?\315\302\311\027\3613\002\220\331\366]e-vS\020\2373(\374\257/Y\342<4\
\020\377\233S\243\016\221\243wb_b8\236\326\2445\361\362B\221\334\206\227\
\211\344\311n\272\261&f   \007YP\177\3067\027\022H\2668\023\321)\343\013\
\265\337#\274\207S\372)\212\201Nf\201\315\177\371\241\331\215\353\3258\263\
\016O\371zC\307KH\372A~]Ykv\031\366\2718\316L\376\257\207\214@*\025@\317\
\213\361\305\266\255j8\306q\273O3\302\031\231FO%{\234\330g\311}\365w\027\
\225\253\226?\223\267w\321}\220\356\014\243\213\265d~\366\204\345\273v\
\255\013\264\002$^\262\270r\217z\252q\377\365\336M\321\301e\310*\365i\001\
\241U2\320\204c[!\364\000\\\322\251\026\353\347Q\234\356)\274[^M\177\340\
\253\0038\025\014\245<<\020\021\031\311\026\376\361\345\032\324\236\001\
\274\221\370M-\267\215e\356*\037\224\331,\374\306\243nz\335Q\226>\332\007\
N\231g\344\320w\367knZ\237\375\225\360\250\343\251\353\234\015L\303H\010\
\304\014\\g\0105\225\346\231\357\324\240B\207-\000\263\376\376\251\261\264\
Ja\277\335.Xe\026\2317k!\235\332\204\345\313\245\327_569\020 \374k\262\241\
\014\002\035V\314\337\260!\237@[y\036]\023\331\275\236\006\237\237lHz\016\
\325(Z`\232vy<Q\375\250\\\212\227\015\326!\241\301\202\247\247\024F\221\
\272Qb\244\310\325\010\037=\023\003\242Z}\215Z\031\275V"Sr\372E\234\212\
\024\203\272\320\307\306\375[\316\325N'\326\363|\233\361'@\
"""
    texts.update([rand1, rand2])
    texts.update([x + '\000' for x in (rand1, rand2)])
    texts.update(['\000' + x for x in (rand1, rand2)])
    return texts

plaintexts = define_texts()

# -------------------- #
#  Go with the tests.  #
# -------------------- #

@with_params(plaintexts, 'plaintext')
@with_params([k for k in keys_list if k['n'].bit_length() > 16])
def test_pubkey_encrypt_privkey_decrypt(n, p, q, e, d, plaintext):
    encrypter = BinaryEncrypter(PublicKey(n, e))
    decrypter = BinaryEncrypter(PrivateKey(p, q, e))
    ciphertext = ''.join(encrypter.encrypt(plaintext))
    assert plaintext == ''.join(decrypter.decrypt(ciphertext))

@with_params(plaintexts, 'plaintext')
@with_params([k for k in keys_list if k['n'].bit_length() > 16])
def test_privkey_encrypt_privkey_decrypt(n, p, q, e, d, plaintext):
    encrypter = BinaryEncrypter(PrivateKey(p, q, e))
    ciphertext = ''.join(encrypter.encrypt(plaintext))
    assert plaintext == ''.join(encrypter.decrypt(ciphertext))

# Check that we can enncrypt/decrypt also "biggish" byte sequences
# (~ 50M) in a reasonable time.
# FIXME: having a timeout here would be better than risking to have
# the testsuite almost hang ...
@with_params([keys_dict['M2281_M2203'], keys_dict['styere_e19']])
def test_encrypt_decrypt_large(n, p, q, e, d):
    def gen_bytes():
        for i in range(0, 5):
            fp = open("random.bytes")
            while True:
                byte = fp.read(1)
                if byte:
                    yield byte
                else:
                    fp.close()
                    break
    encrypter = BinaryEncrypter(PrivateKey(p, q, e))
    for chunk in encrypter.encrypt(gen_bytes()): pass

# vim: et sw=4 ts=4 ft=python
