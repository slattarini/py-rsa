# -*- python -*-
# -*- coding: iso-8859-1 -*-

#--------------------------------------------------------------------------

## --------------------------------- ##
##  Metadata & Global Documentation  ##
## --------------------------------- ##

"""An "education" implementation of the RSA encryption/digital sign
algorithm"""

#--------------------------------------------------------------------------

## ------------------------ ##
##  List of exported stuff  ##
## ------------------------ ##

__all__ = [
    # custom exceptions
    'IMException',
    'IMTypeError',
    'IMValueError',
    # g.c.d and euclidean algorithm
    'extended_gcd',
    'gcd',
    # integers (mod n)
    'integers_mod',
    'IntegerMod',
]

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
    Not meant to be used directly; you should use it by subclassing:
       >>> class IntegerMod6(IntegerMod):
       ...    modulo = 6
       >>> _1mod6 = IntegerMod6(1)
       >>> _2mod6 = IntegerMod6(2)
       >>> _3mod6 = IntegerMod6(3)
       >>> print (_1mod6 + _2mod6 + _3mod6)
       0 (mod 6)
    """

    """The modulo the integers are reduced with.  Must be overridden
    by subclasses."""
    modulo = None

    def __init__(self, whole):
        if self.modulo is None:
            # Sanity check: `modulo' should be overridden by subclasses.
            raise IMRuntimeError("modulo not overridden (is still None)")
        self.residue = whole % self.modulo

    def __repr__(self):
        # FIXME: not always correct
        return "%s(%u)" % (self.__class__.__name__, self.residue)

    def __str__(self):
        return "%u (mod %u)" % (self.residue, self.modulo)

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.modulo == other.modulo
                and self.residue == other.residue)

    # python docs suggest to define this method, explicitly also
    # when __eq__ is defined
    def __ne__(self, other):
        return (not (self == other))

    def __add__(self, other):
        # TODO: check that self and other belong to the same class
        return self.__class__(self.residue + other.residue)

    def __sub__(self, other):
        # TODO: check that self and other belong to the same class
        return self.__class__(self.residue - other.residue)

    def __mul__(self, other):
        if isinstance(other, (int, long)):
            other = self.__class__(other)
        # TODO: check that self and other belong to the same class
        return self.__class__(self.residue * other.residue)

    def __rmul__(self, other):
        return self * other

    def _get_reciprocal(self):
        d, x, y = extended_gcd(self.modulo, self.residue)
        if d != 1:
            raise IMValueError("%d is not prime with %d" %
                               (self.modulo, self.residue))
        # Now we have self.modulo * x + self.residue * y = 1, so
        # self.residue * y = 1 (mod self.modulo), so...
        return self.__class__(y)

    def __div__(self, other):
        if isinstance(other, (int, long)):
            other = self.__class__(other)
        # TODO: check that self and other belong to the same class
        # With this point, we'll need r = a / b (mod m), i.e. an integer
        # r such that b * r = a (mod m)
        m = self.modulo
        a = self.residue
        b = other.residue
        # With this, we'll have  d = b*x + m*y  and  d | b  &  d | m
        d, x, y = extended_gcd(b, m)
        # If d | a ...
        if a % d == 0:
            # ... then , t := a / d, we have :
            #   a = d * t = d * (b*x + m*y) = b * (d*x) (mod m)
            # so that a / b = d*x (mod m), and we're done.
            return self.__class__(d*x)
        # Else, if d does not divide a, the equation b * r = a (mod m) has
        # no solution; for if it had one, we'd have:
        #   a = b*r + m*s  for some integer s
        # which, being d | m and d | b, implies d | a, false.
        # FIXME: better exception?
        raise IMValueError('cannot divide "%s" for "%s"' % (self, other))

    def __pow__(self, exponent):
        if exponent < 0:
            exponent *= -1
            base = self._get_reciprocal()
        else:
            base = self
        result = self.__class__(1)
        while exponent > 0:
            exponent -= 1
            result *= base
        return result

#--------------------------------------------------------------------------


## ----------- ##
##  Main Code  ##
## ----------- ##

if __name__ == "__main__":
    # If running as a script, run all the doctests defined in this module.
     import sys
     sys.exit(doctest.testmod()[0] > 0)

#--------------------------------------------------------------------------

# vim: ft=python et sw=4 ts=4
