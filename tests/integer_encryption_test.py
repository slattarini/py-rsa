#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for our implementation of RSA applied to integers."""
import pytest
import RSA
#from tests.pyrsa_testlib import with_params, without_duplicates, \
#                                integers_mod, pytest_generate_tests

# Example stolen from wikipedia entry on RSA.
def test_wikipedia_sample():
   key = RSA.PrivateKey(p=61, q=53, e=17)
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

# vim: et sw=4 ts=4 ft=python
