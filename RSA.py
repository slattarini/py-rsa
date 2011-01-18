# -*- python -*-
# -*- coding: iso-8859-1 -*-

#--------------------------------------------------------------------------

## --------------------------------- ##
##  Metadata & Global Documentation  ##
## --------------------------------- ##

"""An "educational" implementation of the RSA encryption and digital sign
algorithm"""

# All classes declared in this file are to be new-style classes.
__metaclass__ = type

#--------------------------------------------------------------------------

## ---------------- ##
##  Global Imports  ##
## ---------------- ##

import functools

#--------------------------------------------------------------------------

## ------------------- ##
##  Custom Exceptions  ##
## ------------------- ##

class IMException(Exception):
    """Base class for exceptions that can be raised by classes and
    subroutines dealing with integers (mod n)"""
    pass

class IMRuntimeError(IMException, RuntimeError):
    """RuntimeError exception that can be raised by classes and
    subroutines dealing with integers (mod n)"""
    pass

class IMTypeError(IMException, TypeError):
    """TypeError exception that can be raised by classes and subroutines
    dealing with integers (mod n)"""
    pass

class IMValueError(IMException, ValueError):
    """ValueError exception that can be raised by classes and subroutines
    dealing with integers (mod n)"""
    pass

class CryptoException(Exception):
    """Base class for exceptions that can be raised by classes and
    subroutines dealing with RSA encryption (keys, encrypters and
    decrypters)"""
    pass

class CryptoRuntimeError(CryptoException, RuntimeError):
    """RuntimeError exception that can be raised by classes and subroutines
    dealing with RSA encryption (keys, encrypters and decrypters)"""
    pass

class CryptoTypeError(CryptoException, TypeError):
    """TypeError exception that can be raised by classes and subroutines
    dealing with RSA encryption (keys, encrypters and decrypters)"""
    pass

class CryptoValueError(CryptoException, ValueError):
    """ValueError exception that can be raised by classes and subroutines
    dealing with RSA encryption (keys, encrypters and decrypters)"""
    pass

#--------------------------------------------------------------------------

## ---------------------------------------------- ##
##  Internal Classes, Subroutines and Decorators  ##
## ---------------------------------------------- ##

def _operation_modulo_integer(func):
    def wrapper(self, other):
        if isinstance(other, (int, long)):
            other = self.__class__(other)
        elif not isinstance(other, self.__class__):
            raise IMTypeError("%r is not a %s", other, self.__class__)
        return self.__class__(func(self, other))
    return functools.update_wrapper(wrapper, func)

#--------------------------------------------------------------------------

## ---------------------------------------------- ##
##  Great Common Divisor and Eucliean Algorithms  ##
## ---------------------------------------------- ##

def extended_gcd(a, b):
    """Implement the Euclidean algorithm for the determination of the
    great common divisor between a and b.  Returns (d, x, y), where
    d = g.c.d.(a, b) and x, y are such that:
      * ax + by = d
      * -max(1, (1/2)(b/d) <= x <= max(1, (1/2)(b/d))
      * -max(1, (1/2)(a/d) <= y <= max(1, (1/2)(a/d))
    """
    # This special cases selected for compatibility with GAP (see the
    # `Gcdex' function).
    if b == 0:
        if a == 0:
            return (0, 0, 0)
        else:
            return (a, 1, 0)
    r0, r1 = a, b
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    while r1 != 0:
        q = r0 / r1
        r0, r1 = r1, r0 % r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return (r0, x0, y0)

def gcd(a, b):
    """Calculate and return the greatest common divisor between a and b,
    using the Euclidean algorithm."""
    r0 = max(a, b)
    r1 = min(a, b)
    while r1 != 0:
        r0, r1 = r1, r0 % r1
    return r0

#--------------------------------------------------------------------------

## ------------------- ##
##  Integers Modulo N  ##
## ------------------- ##

class IntegerMod(object):
    """A class representing integers (modulo n), for an unspecified modulo.
    Not meant to be used directly; you should use it by subclassing.

    A basic example:
      >>> class IntegerMod15(IntegerMod):
      ...    modulo = 15
      >>> # They print nicely, and can be initialized from any integer.
      >>> print IntegerMod15(11)
      11 (mod 15)
      >>> print IntegerMod15(17)
      2 (mod 15)
      >>> print IntegerMod15(-1)
      14 (mod 15)
      >>> print IntegerMod15(150000000000000000000000000000000L + 1)
      1 (mod 15)
      >>> # A nice trick to have all integers (modulo 15) at hand.
      >>> mod15 = []
      >>> for i in range(0,15):
      ...   mod15.append(IntegerMod15(i))
      >>> # Four operations are supported, with natural association
      >>> # and precedence rules.
      >>> print (mod15[1] + mod15[3] + mod15[11])
      0 (mod 15)
      >>> print (mod15[1] - mod15[3])
      13 (mod 15)
      >>> print (mod15[1] - mod15[3] + mod15[5])
      3 (mod 15)
      >>> print (mod15[11] * mod15[5] - mod15[4])
      6 (mod 15)
      >>> print (mod15[11] / mod15[4])
      14 (mod 15)
      >>> # Inversion is supported too.
      >>> print (-mod15[7])
      8 (mod 15)
      >>> print (mod15[7] + (- mod15[10]))
      12 (mod 15)
      >>> # Exponentiation works too.
      >>> print (mod15[2]**4)
      1 (mod 15)
      >>> print (mod15[7]**2)
      4 (mod 15)
      >>> print (mod15[13]**(-3))
      13 (mod 15)
      >>> # Integers modulo something can also be combined with
      >>> # regular integers!
      >>> print (1 / mod15[2])
      8 (mod 15)
      >>> print (5 * mod15[3])
      0 (mod 15)
      >>> print ((2 + 15 * 10**100) * mod15[2])
      4 (mod 15)
      >>> print (mod15[11] / mod15[8] * 3 + 1)
      7 (mod 15)
      >>> # Proper exceptions should be raised for impossible operations
      >>> mod15[10]**(-1)
      Traceback (most recent call last):
       ...
      IMValueError: 15 is not prime with 10
      >>> 1 / mod15[9]
      Traceback (most recent call last):
       ...
      IMValueError: 15 is not prime with 9
      >>> # To calculate a/b (mod m), we require that gcd(b, m) = 1,
      >>> # since otherwise the operation is impossible (has no solutions)
      >>> # or indefinite (has multiple possible results).
      >>> mod15[12] / mod15[3]
      Traceback (most recent call last):
       ...
      IMValueError: 15 is not prime with 3
    """

    """The modulo the integers are reduced with.  Must be overridden
    by subclasses."""
    modulo = None

    def __init__(self, whole):
        if self.modulo is None:
            # Sanity check: `modulo' should be overridden by subclasses.
            raise IMRuntimeError("modulo not overridden (is still None)")
        if isinstance(whole, self.__class__):
            whole = whole.residue
        self.residue = whole % self.modulo

    def __repr__(self):
        # FIXME: not always correct
        return "%s(%u)" % (self.__class__.__name__, self.residue)

    def __str__(self):
        return "%u (mod %u)" % (self.residue, self.modulo)

    def __eq__(self, other):
        """Two integers (mod m) are equal iff their modulo, residue
        and class are equal."""
        return (type(self) == type(other)
                and self.modulo == other.modulo
                and self.residue == other.residue)

    def __ne__(self, other):
        return (not self == other)

    def __neg__(self):
        return (-1) * self

    @_operation_modulo_integer
    def __add__(self, other):
        return self.residue + other.residue

    def __radd__(self, other):
        return self + other

    @_operation_modulo_integer
    def __sub__(self, other):
        return self.residue - other.residue

    def __rsub__(self, other):
        return (-1) * (self - other)

    @_operation_modulo_integer
    def __mul__(self, other):
        return self.residue * other.residue

    def __rmul__(self, other):
        return self * other

    # When calculating a/b (mod m), we require that gcd(b, m) = 1,
    # since otherwise the operation is impossible (has no solutions)
    # or indefinite (has multiple possible results).

    @_operation_modulo_integer
    def __div__(self, other):
        return self * other**(-1)

    @_operation_modulo_integer
    def __rdiv__(self, other):
        return self**(-1) * other

    def __pow__(self, exponent):
        if not isinstance(exponent, (int, long)):
            raise IMTypeError("exponent %r is not an integer", exponent)
        elif exponent < 0:
            exponent *= -1
            base = self._get_reciprocal()
        else:
            base = self
            if self.residue == 0:
                # FIXME: what about e.g. 0**0? not easy to detect in the general
                # case, since we can't easily know the value of phi(modulo),
                # and thus we can't know if exponent % phi(modulo) == 0.
                # Just return 0 for the moment.
                return self.__class__(0)
        partial1 = partial2 = self.__class__(1)
        while exponent > 0:
            if exponent % 2 == 1:
                partial1 *= base
                exponent -= 1
            else:
                exponent /= 2
                partial2 = base = base * base
                if exponent == 1:
                    break
        return partial1 * partial2

    def _get_reciprocal(self):
        d, x, y = extended_gcd(self.modulo, self.residue)
        if d != 1:
            raise IMValueError("%d is not prime with %d" %
                               (self.modulo, self.residue))
        # Now we have self.modulo * x + self.residue * y = 1, so
        # self.residue * y = 1 (mod self.modulo), so...
        return self.__class__(y)

#--------------------------------------------------------------------------

## ------------------ ##
##  RSA for numbers.  ##
## ------------------ ##

class PublicKey:
    """The most basic usable RSA Public Key. Just a data container."""
    def __init__(self, n, e):
        self.n = n
        self.e = e
    def __eq__(self, other):
        return (self.n == other.n and self.e == other.e)
    def __ne__(self, other):
        return (not self == other)

class PrivateKey:
    """The most basic private RSA Key. Basically just a data container."""
    public_key_class = PublicKey
    modular_integer_class = IntegerMod
    def __init__(self, p, q, e):
        # We just trust p and q to be prime and of similar size.
        self.p = p
        self.q = q
        self.n = p * q
        phi_n = (p - 1) * (q - 1)
        # TODO: check that (e, phi) = 1 and 0 < e < phi
        class mod_phi_n(self.modular_integer_class):
            modulo = phi_n
        self.e = e
        self.d = (mod_phi_n(e)**(-1)).residue
    def public(self):
        return self.public_key_class(self.n, self.e)
    def __eq__(self, other):
        return (self.p == other.p and self.q == other.q
                and self.d == other.d)
    def __ne__(self, other):
        return (not self == other)

class IntegerEncrypter:
    """Encrypt a given integer using RSA.
      >>> # p and q are Mersenne primes; see Wikipedia.
      >>> key = PrivateKey(p=2**2281-1, q=2**2203-1, e=65537)
      >>> D = IntegerDecrypter(key)
      >>> # An encrypter should work with just a public key.
      >>> E = IntegerEncrypter(key.public())
      >>> # The number to encrypt.
      >>> plain = 2**1000 + 25
      >>> cypher = E.encrypt(plain)
      >>> D.decrypt(cypher) == plain
      True
      >>> # An encrypter should work also with a private key (which
      >>> # "contains" the public key anyway).
      >>> E2 = IntegerEncrypter(key.public())
      >>> E2.encrypt(plain) == cypher
      True
      >>> # Let's try with another input.
      >>> plain = 2**1010 + 27
      >>> D.decrypt(E.encrypt(plain)) == plain
      True
      >>> D.decrypt(E2.encrypt(plain)) == plain
      True
    """
    modular_integer_class = IntegerMod
    def __init__(self, key):
        # "key" might be a public RSA key or a private RSA key.
        self.key = key
        class mod_n(self.modular_integer_class):
            modulo = key.n
        self.mod_n = mod_n
    def _modular_exponentiation(self, x, m):
        # TODO: assert 0 <= m < n
        return (self.mod_n(x)**m).residue
    def encrypt(self, i):
        return self._modular_exponentiation(i, self.key.e)

class IntegerDecrypter(IntegerEncrypter):
    """Decrypt and/or decrypt a given integer using RSA.
      >>> # p and q are Mersenne primes; see Wikipedia.
      >>> key = PrivateKey(p=2**4253-1, q=2**4423-1, e=8191)
      >>> # While an encrypter should work also with just a public key,
      >>> # a decrypter should require a private key.
      >>> D = IntegerDecrypter(key.public())
      Traceback (most recent call last):
       ...
      CryptoTypeError: key doesn't seem a private key
      >>> D = IntegerDecrypter(key)
      >>> plain = 3**3237 + 2**512 - 7
      >>> # A decrypter can encrypt as well as decrypt!
      >>> cypher = D.encrypt(plain)
      >>> D.decrypt(cypher) == plain
      True
    """
    def __init__(self, key):
        try:
            key.d
        except AttributeError:
            raise CryptoTypeError("key doesn't seem a private key")
        else:
            super(IntegerDecrypter, self).__init__(key)
    def decrypt(self, i):
        return self._modular_exponentiation(i, self.key.d)

#--------------------------------------------------------------------------


## ----------- ##
##  Main Code  ##
## ----------- ##

if __name__ == "__main__":
    # If running as a script, run all the doctests defined in this module.
     import sys, doctest
     sys.exit(doctest.testmod()[0] > 0)

#--------------------------------------------------------------------------

# vim: ft=python et sw=4 ts=4
