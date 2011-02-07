#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for our "naive" implementation of RSA keys."""
from RSA import PublicKey, PrivateKey
from tests.keys import keys
from tests.lib import with_params, pytest_generate_tests

private_keys = [ v for (_, v) in keys.iteritems() ]
public_keys = [ dict(n = k['n'], e = k['e']) for k in private_keys ]

@with_params(public_keys)
def test_create_public_key(n, e):
    key = PublicKey(n, e)
    assert (key.n == n and key.e == e)

@with_params(private_keys)
def test_create_private_key(n, p, q, e, d):
    key = PrivateKey(p, q, e)
    assert (key.p == p and key.q == q and key.n == n
            and key.e == e and key.d == d)

@with_params(private_keys)
def test_public_key_from_private_key(n, p, q, e, d):
   private_key = PrivateKey(p, q, e)
   public_key = PublicKey(n, e)
   assert private_key.public() == public_key

@with_params(public_keys)
def test_public_keys_equality(n, e):
   key1 = PublicKey(n, e)
   key2 = PublicKey(n + 0L, e + 0L)
   assert key1 == key2 and not (key1 != key2)

@with_params(private_keys)
def test_private_keys_equality(n, p, q, e, d):
   key1 = PrivateKey(p, q, e + 0L)
   key2 = PrivateKey(p + 0L, q + 0L, e)
   assert key1 == key2 and not (key1 != key2)

# vim: et sw=4 ts=4 ft=python
