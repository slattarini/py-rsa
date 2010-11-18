#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""Simple test harness script for the testsuite of RSA.py"""

import sys
import py.test.cmdline
args = sys.argv[1:] + ['RSA.py', 'tests']

if __name__ == '__main__':
    py.test.cmdline.main(args)

# vim: et sw=4 ts=4 ft=python
