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

## ------------------------------------------------------------------ ##
##  Positional Representation of Integer Numbers in Different Bases.  ##
## ------------------------------------------------------------------ ##

def pos_to_int(seq, base):
    result, base_power = 0, 1
    for digit in seq:
        result += base_power * digit
        base_power *= base
    return result

def int_to_pos(n, base):
    seq = []
    while 1:
        seq.append(n % base)
        n = n / base
        if n == 0:
            break
    return seq

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
        return "%r(%u)" % (self.__class__, self.residue)

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


class IntegerModPQ(IntegerMod):
    """A class representing integers (modulo pq), where p and q are two
    different prime numbers.  It offers an optimized implementation of
    exponentation, using the Chinese Reminder Theorem.
    This calss could probably be generalized to all integers whose
    factorization into primes is known; but the particular case we
    implementat is enough for our needs (i.e., implementing the RSA
    encryption/decryption)."""

    """The two primes whose product gives the modulo."""
    p = None
    q = None

    @classmethod
    def _cls_init(cls):
        if cls.p is None or cls.q is None:
            # Sanity check: `p' and `q' should be overridden by subclasses.
            raise IMRuntimeError("p or q not overridden (is still None)")
        # So that we can assume p > q.
        cls.p, cls.q = max(cls.p, cls.q), min(cls.p, cls.q)
        cls.modulo = cls.p * cls.q
        class int_mod_p(IntegerMod): modulo = cls.p
        class int_mod_q(IntegerMod): modulo = cls.q
        cls.int_mod_p = int_mod_p
        cls.int_mod_q = int_mod_q
        # p^(-1) (mod q)
        cls.p_reciprocal_mod_q = modular_reciprocal(cls.p, cls.q)
        cls._cls_init = classmethod(lambda cls : None)

    def __init__(self, whole):
        self.__class__._cls_init()
        super(IntegerModPQ, self).__init__(whole)
        self.mod_p = self.int_mod_p(whole)
        self.mod_q = self.int_mod_q(whole)

    def __pow__(self, exponent):
        if not isinstance(exponent, (int, long)):
            raise IMTypeError("exponent %r is not an integer", exponent)
        a = (self.mod_p ** (exponent % (self.p - 1))).residue
        b = (self.mod_q ** (exponent % (self.q - 1))).residue
        result = a + self.p * (b - a) * self.p_reciprocal_mod_q
        return self.__class__(result)


def modular_reciprocal(a, m):
    """Calculate the inverse of a (mod m), i.e. 0 < b < m such that
    ab = 1 (mod m).  This will raise an exception if a and b are not
    coprime"""
    class cls(IntegerMod):
        modulo = m
    cls.__name__ = "IntegerMod%u" % m  # for better error messages
    return (cls(a)**(-1)).residue


#--------------------------------------------------------------------------


## -------------------------------- ##
##  RSA encryption and decryption.  ##
## -------------------------------- ##


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
    def __init__(self, p, q, e):
        # We just trust p and q to be prime and of similar size.
        self.p = p
        self.q = q
        self.n = p * q
        phi_n = (p - 1) * (q - 1)
        # TODO: check that (e, phi) = 1 and 0 < e < phi
        self.e = e
        self.d = modular_reciprocal(e, phi_n)
    def public(self):
        return self.public_key_class(self.n, self.e)
    def __eq__(self, other):
        return (self.p == other.p and self.q == other.q
                and self.d == other.d)
    def __ne__(self, other):
        return (not self == other)


class BasicEncrypter:
    """Base class for encrypting/decrypting using RSA.

    Can only encrypt if given a public key, can also decrypt if given a
    private key.

    This class works only on integers < pq, and uses a minimalistic and
    naive implementation, which is also not semantically secure (no padding,
    etc.).  But this implemetnation is designed to be easily extended by
    subclasses, which can then offer various enhancements.

    Some examples of usage:
      >>> plain = 2**1000 + 25 # The number to encrypt.
      >>> # p and q are Mersenne primes; source: Wikipedia.
      >>> key = PrivateKey(p=2**2281-1, q=2**2203-1, e=65537)
      >>> # An encrypter knowing just the public key will only be able to
      >>> # encrypt; one knowing the private key should be able to both
      >>> # encrypt and decrypt.
      >>> E = BasicEncrypter(key.public())
      >>> D = BasicEncrypter(key)
      >>> D.decrypt(E.encrypt(plain)) == plain
      True
      >>> # A decrypter (i.e. an encypter in posses of a private key)
      >>> # should also be able to encrypt.
      >>> D.decrypt(D.encrypt(plain)) == plain
      True
      >>> # As already said, an encrypter requires a private key in order
      >>> # to be able to decrypt.
      >>> cipher = E.encrypt(plain)
      >>> E.decrypt(cipher) == plain
      Traceback (most recent call last):
       ...
      CryptoRuntimeError: can't decrypt without a private key
    """

    def __init__(self, key):
        """ The key might be a public RSA key or a private RSA key."""
        # But we can decrypt only if it is a private key, in which case we
        # can also used on optimized implementation to improve encryption
        # and decryption performances.
        self.key = key
        try:
            key.p, key.q
        except AttributeError:
            # is a public key
            class mod_n(IntegerMod):
                modulo = key.n
        else:
            # is a private key
            class mod_n(IntegerModPQ):
                p, q = key.p, key.q
        self.mod_n = mod_n

    #
    # Transform the encrypted/decrypted messages into/from a sequence
    # of non-negative integers.
    #
    # Subclasses can override these functions in order to be able to
    # encrypt/decrypt objects of generic types (e.g. strings and sequences
    # of bytes), provided that there's a simple way to univocally convert
    # between such objects and sequences of unsigned integers.
    #
    # Note that we deliberately allow the objects representing the plain
    # messages and the objects representing the encrypted messages to be
    # of different types.  This might be truly useful in practice.
    #
    def o2i(self, text):
        """From plaintext and/or ciphertext to sequence of integers."""
        return (text,)
    def i2o(self, seq):
        """From sequence of integers to plaintext and/or ciphertext."""
        return seq[0]
    def p2i(self, plaintext):
        """From plaintext to sequence of integers.
        By default, equivalent to 'o2i'"""
        return self.o2i(plaintext)
    def i2p(self, integer):
        """From sequence integers to plaintext.
        By default, equivalent to 'i2o'"""
        return self.i2o(integer)
    def c2i(self, ciphertext):
        """From ciphertext to sequence of integers.
        By default, equivalent to 'o2i'"""
        return self.o2i(ciphertext)
    def i2c(self, integer):
        """From sequence of integers to ciphertext.
        By default, equivalent to 'i2o'"""
        return self.i2o(integer)

    # Implement the padding scheme used by the class.
    # Meant to be overridden by subclasses.
    def pad(self, plaintext):
        return plaintext
    def unpad(self, plaintext):
        return plaintext

    def _modexp(self, integer, exponent):
        if not 0 <= integer < self.key.n:
            # FIXME: better error class?
            raise CryptoRuntimeError("integer %d out of range" % integer)
        return (self.mod_n(integer)**exponent).residue

    def _encrypt(self, integer):
        return self._modexp(integer, self.key.e)

    def _decrypt(self, integer):
        try:
            d = self.key.d
        except AttributeError:
            raise CryptoRuntimeError("can't decrypt without a private key")
        else:
            return self._modexp(integer, d)

    def encrypt(self, plaintext):
        return self.i2c(map(self._encrypt, self.p2i(plaintext)))
    def decrypt(self, ciphertext):
        return self.i2p(map(self._decrypt, self.c2i(ciphertext)))


class IntegerEncrypter(BasicEncrypter):
    """Encrypt/Decrypt generic integers.  This class is meant to work also
    with integers >= pq.

    Example:
      >>> key = PrivateKey(p=2**1279-1, q=2**3217-1, e=8191)
      >>> plain = 7**4000 + 27
      >>> E = IntegerEncrypter(key.public())
      >>> D = IntegerEncrypter(key)
      >>> D.decrypt(E.encrypt(plain)) == plain
      True
      >>> D.decrypt(D.encrypt(plain)) == plain
      True
    """
    def o2i(self, big_integer):
        return int_to_pos(big_integer, self.key.n)
    def i2o(self, sequence):
        return pos_to_int(sequence, self.key.n)


class ByteSequenceEncrypter(BasicEncrypter):
    """Encrypt a generic byte sequence with RSA."""

    # Plaintext conversion  [byte sequence] <--> [list of integer]
    #--------------------------------------------------------------
    # We'll first convert the byte sequence into a bits sequence.
    # This bits sequence will be broken in chunks of proper size;
    # each of these chunks will be padded with a final bit = 1, and
    # trivially converted into an integer, by considering its list
    # of bits as a representation of said integer in base 2 (big
    # endian format).
    # The padding is necessary to avoid ambiguity in case the chunk
    # ends with one or more 0 bits; otherwise, distinct bit sequences
    # like '111', '1110' and '1110000' whould all be converted into
    # the same integer (in this case, '7').
    # Since the integers to be encrypted must be less than n, the bits
    # sequence must be broken in chunks whose integer representation
    # is < n.  An easy way to do so is to ensure that each chunk has
    # at most (n_bitlen - 1) bits, where n_bitlen is the number of
    # bits in n.  Since we need room also to append the final padding
    # bit = 1, the unpadded chunks will have to be (n_bitlen - 2) bits
    # long actually.

    # Ciphertext conversion  [byte sequence] <--> [list of integer]
    #---------------------------------------------------------------
    # Each integer must be converted into a chunk of bytes of fixed
    # length, so that the receiving end can unambiguously decompose
    # the arriving sequence of bytes, to recover the original list of
    # integers.
    # This is quite easy to do: we just convert the integers in base
    # 2**8 = 256 (in big-endian format), and if necessary pad the
    # resulting byte sequence with null bytes.
    # Also, the length of the chunks is easy to determine: since the
    # integers are all to be < n, the length *in bytes* of n will
    # suffice (this lenght is simply one-eight of the length in bits
    # of n, rounded *up*).

    BASE = 1 << 8

    def i2c(self, integer):
        return ''.join([chr(i) for i in int_to_pos(integer, self.BASE)])
    def c2i(self, bytes):
        return pos_to_int([ord(b) for b in bytes], self.BASE)

    def p2i(self, bytes):
        # Apend `1' so that we can distinguish between e.g. sequences
        # ending with '\000' and '\000\000'.
        return pos_to_int([ord(b) for b in bytes] + [1], self.BASE)
    def i2p(self, integer):
        return ''.join([chr(i) for i in
                        int_to_pos(integer, self.BASE)[:-1]])


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
