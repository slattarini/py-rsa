#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for our "naive" implementation of RSA keys."""
import pytest
import RSA
from tests.pyrsa_testlib import with_params, integers_mod

def test_create_public_key():
    key = RSA.PublicKey(n=35, e=3)
    assert (key.n == 35 and key.e == 3)

# From the example on Wikipedia entry on RSA.
def test_create_private_key_1():
    key = RSA.PrivateKey(p=61, q=53, e=17)
    assert (key.p == 61 and key.q == 53 and key.n == 3233
            and key.e == 17 and key.d == 2753)

def test_create_private_key_2():
    M1, M2 = 2**521 - 1, 2**607 - 1 # these are mersenne primes
    key = RSA.PrivateKey(p=M1, q=M2, e=(M1-1)*(M2-1)-1)
    assert (key.p == M1 and key.q == M2 
            and key.n == 2**1128 - 2**521 - 2**607 + 1
            and key.e == 2**1128 - 2**522 - 2**608 + 3
            and key.d == key.e)
    
def test_public_key_from_private_key():
   private_key = RSA.PrivateKey(p=61, q=53, e=17)
   public_key = RSA.PublicKey(n=61*53, e=17)
   assert private_key.public() == public_key

def test_private_keys_equality():
   key1 = RSA.PrivateKey(p=61, q=53, e=17L)
   key2 = RSA.PrivateKey(p=61L, q=53, e=17)
   assert key1 == key2 and not (key1 != key2)

def test_public_keys_equality():
   key1 = RSA.PublicKey(n=55, e=29L)
   key2 = RSA.PublicKey(n=55L, e=29L)
   assert key1 == key2 and not (key1 != key2)

# vim: et sw=4 ts=4 ft=python
