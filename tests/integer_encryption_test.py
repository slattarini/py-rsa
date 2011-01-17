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
   encrypter = RSA.IntegerEncrypter(key)
   decrypter_priv = RSA.IntegerDecrypter(key)
   decrypter_pub = RSA.IntegerDecrypter(key.public())
   plain = 65
   cypher = 2790
   assert (encrypter.encrypt(plain) == cypher
           and encrypter.decrypt(cypher) == plain
           and decrypter_priv.decrypt(cypher) == plain
           and decrypter_pub.decrypt(cypher) == plain)

###  DATA


# The list of known values has been obtained thanks to:
#  http://www.hanewin.net/encrypt/rsa/rsa-test.htm

# vim: et sw=4 ts=4 ft=python
