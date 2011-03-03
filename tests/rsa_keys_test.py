#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of RSA.py testsuite.

"""Tests for our "naive" implementation of RSA keys."""

import pytest
from RSA import PublicKey, PrivateKey, CryptoValueError
from tests.keys import keys
from tests.lib import with_params, pytest_generate_tests

def define_test_data():
    global private_keys, public_keys, invalid_private_keys
    private_keys = [ v for (_, v) in keys.iteritems() ]
    public_keys = [ dict(n = k['n'], e = k['e']) for k in private_keys ]
    invalid_private_keys = [
        dict(p=5, q=7, e=12),
        dict(p=5, q=7, e=29),
        dict(p=5, q=7, e=-1),
        dict(p=61, q=53, e=4457),
        dict(p=199, q=87, e=2),
        dict(p=199, q=87, e=-11),
        dict(p=199, q=87, e=26293),
        dict(p=199, q=87, e=-26393),
        dict(p=2**127-1, q=2**61-1, e=2**14-1),
        dict(p=2**127-1, q=2**61-1, e=2**187+1),
    ]
    for k in [k0.copy() for k0 in private_keys]:
        del k['d'], k['n']
        p, q = k['p'], k['q']
        phi_n = (p - 1) * (q - 1)
        invalid_private_keys.extend([
            dict(k, e = p - 1),
            dict(k, e = q - 1),
            dict(k, e = -1),
            dict(k, e = -p),
            dict(k, e = -q),
            dict(k, e = phi_n + 1),
            dict(k, e = phi_n**2 + 100 * phi_n+1),
        ])

define_test_data()

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

@with_params(invalid_private_keys)
def test_invalid_private_keys(p, q, e):
    pytest.raises(CryptoValueError, "PrivateKey(p, q, e)")

# vim: et sw=4 ts=4 ft=python
