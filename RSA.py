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
    Not meant to be used directly.

    You are advised to use the class-factory subroutine 'integers_mod()',
    which build a proper 'IntegerMod' subclass for you:
       >>> IntegerMod7 = integers_mod(7)
       >>> _1mod7 = IntegerMod7(1)
       >>> _2mod7 = IntegerMod7(2)
       >>> _3mod7 = IntegerMod7(3)
       >>> print (_1mod7 + _2mod7 * _3mod7)
       0 (mod 7)

    It's also possible to specify a custom name for the returned class:
       >>> IntegerMod5 = integers_mod(5, 'custom_name')
       >>> print IntegerMod5.__name__
       custom_name
       >>> _1mod5 = IntegerMod5(1)
       >>> _2mod5 = IntegerMod5(2)
       >>> _3mod5 = IntegerMod5(3)
       >>> print (_1mod5 + _2mod5 * _3mod5)
       2 (mod 5)

    You might also use 'IntegerMod' by subclassing it first, as in:
       >>> class IntegerMod6(IntegerMod):
       ...    modulo = 6
       >>> _1mod7 = IntegerMod7(1)
       >>> _2mod7 = IntegerMod7(2)
       >>> _3mod7 = IntegerMod7(3)
       >>> print (_1mod6 + _2mod7 + _3mod6)
       0 (mod 6)

    but this use is discouraged.
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
            raise ValueError("%d is not prime with %d" %
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

    def __pow__(self, other):
        raise NotImplementedError #TODO


def integers_mod(n, class_name=None):
    """Return a class representing integers (modulo n), for the specified
    modulo n.

    If n is not an instance of 'int' or 'long', raise a IMTypeError
    exception; if n is <= 0, raise an IMValueError exception.

    The optional argument 'class_name' is used to se the name of the
    returned class; if it is not given or 'None', a proper name will
    be provided automatically (e.g. "IntegerMod11" if n is 11, etc).

    Some examples:
        >>> # erroneous usage #1
        >>> IntegerMod7 = integers_mod("foo")
        Traceback (most recent call last):
            ...
        IMTypeError: parameter n is not an integer
        >>> # erroneous usage #2
        >>> IntegerMod7 = integers_mod(-7)
        Traceback (most recent call last):
            ...
        IMValueError: parameter n is negative or zero
        >>> # let's verify that 2 * 6 = 12 = 1 (mod 11)
        >>> IntegerMod11 = integers_mod(11)
        >>> _2mod11 = IntegerMod11(2)
        >>> _6mod11 = IntegerMod11(6)
        >>> print (_2mod11 * _6mod11)
        1 (mod 11)
        >>> # see that we can override the class name, without other
        >>> # side-effects
        >>> IntMod13 = integers_mod(13, class_name='IntegerModuloThirteen')
        >>> print IntMod13.__name__
        IntegerModuloThirteen
        >>> _5mod13 = IntMod13(2)
        >>> _6mod13 = IntMod13(6)
        >>> print (_5mod13 * _6mod13)
        >>> # one-line verification of Fermat's theorem with p=23, a=11
        >>> print ((integers_mod(23)(11))**(23-1))
        1 (mod 23)
    """
    if not isinstance(n, (int, long)):
        raise IMTypeError("parameter n (%s) is not an integer" % repr(n))
    if not n > 0:
        raise IMValueError("parameter n (%s) is negative or zero" % repr(n))
    if class_name is None:
        class_name = "IntegerMod%u" % n
    class klass(IntegerMod):
        modulo = n
    klass.__name__ = class_name
    return klass

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
