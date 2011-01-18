#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for our implementation of RSA applied to integers."""
import pytest
import RSA
#from tests.pyrsa_testlib import with_params, without_duplicates, \
#                                integers_mod, pytest_generate_tests

# Example stolen from wikipedia entry on RSA.
def test_wikipedia():
    key = RSA.PrivateKey(p=61, q=53, e=17)
    assert key.n == 3233
    assert key.d == 2753
    encrypter_priv = RSA.IntegerEncrypter(key)
    encrypter_pub = RSA.IntegerEncrypter(key.public())
    decrypter = RSA.IntegerDecrypter(key)
    plain = 65
    cypher = 2790
    assert (encrypter_priv.encrypt(plain) == cypher
            and encrypter_pub.encrypt(plain) == cypher
            and decrypter.decrypt(cypher) == plain)

# The list of known values has been obtained thanks to:
#  http://www.hanewin.net/encrypt/rsa/rsa-test.htm
#  http://people.eku.edu/styere/Encrypt/RSAdemo.html

def test_people_eku_edu():
    p = 459983137786273
    q = 167458717901777
    e = 17
    key = RSA.PrivateKey(p, q, e)
    assert key.n == 77028186510125710835232907121
    assert key.d == 45310697947132401996104246513
    encrypter_priv = RSA.IntegerEncrypter(key)
    encrypter_pub = RSA.IntegerEncrypter(key.public())
    decrypter = RSA.IntegerDecrypter(key)
    plain = 57128184570925880835232907122
    cypher = 6764407817379484644525719120
    assert (encrypter_priv.encrypt(plain) == cypher
            and encrypter_pub.encrypt(plain) == cypher
            and decrypter.decrypt(cypher) == plain)

# vim: et sw=4 ts=4 ft=python
