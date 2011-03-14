#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of RSA.py testsuite.

"""Tests for our implementation of RSA applied to integers."""

from RSA import PublicKey, PrivateKey, BasicEncrypter

# Without the Chinese Remainder theorem optimization, this would take
# a ridicolously long time: on the test machine, it took ~ half an
# hour.  With the optimization enabled, it completes in ~ 200 seconds.
# FIXME: having a timeout here would be better than risking to have the
# testsuite almost hang ...
def test_decrypt_speed():
    p = 2**11213 - 1
    q = 2**9941 - 1
    e = 2**3217 - 1
    encrypter = BasicEncrypter(PrivateKey(p, q, e))
    encrypter.decrypt((p - 10) * (q - 23) // 2)

# vim: et sw=4 ts=4 ft=python
