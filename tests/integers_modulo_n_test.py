#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for the RSA.py's implementation of integers (mod n)"""
import py.test
import tests.pyrsa_testlib as TL
import RSA

# obtained with GAP, but could also be looked upon a simple table
small_primes  = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 97, ]
medium_primes = [ 131, 151, 157, 181, 241, 269, 271, 307, ]
large_primes  = [ 373, 397, 401, 433, 499, 523, 541, 571, 641, 659,
                  661, 701, 773, 811, 821, 853, 929, 953, 967, 997, ]
primes = small_primes + medium_primes + large_primes

composite_nosquarefree_modulos = [4, 8, 9, 12, 16, 18, 20, 25, 90, 96, 100]
composite_squarefree_modulos = [6, 10, 14, 15, 21, 22, 46, 77, 95]

# given by their factorization into primes

composite_modulos = [
    (17, 131, 997,),
    (131, 157, 181, 269, 307, 373, 397,),
]

composite_big_modulo = [
    (2, 5), (3, 1), (5, 3), (7, 6), (11, 1), (13, 1), (17, 1), (19, 1),
]
composite_powerfull_big_modulo = [
    (2, 5), (3, 2), (5, 3), (7, 6), (11, 2), (13, 3),
]
composite_squarefree_big_modulo = [
    (3, 1), (5, 1), (7, 1), (13, 1), (19, 1), (23, 1), (269, 1),
]

misc_modulos = [2, 3, 4, 5, 20, 77, 100, 120, 335, 2047, 2**100, 3*1000]

init_known_values = [
    dict(whole=0,   modulo=1, residue=0),
    dict(whole=1,   modulo=1, residue=0),
    dict(whole=0,   modulo=2, residue=0),
    dict(whole=1,   modulo=2, residue=1),
    dict(whole=8,   modulo=5, residue=3),
    dict(whole=77,  modulo=13, residue=12),
    dict(whole=76,  modulo=11, residue=10),
    dict(whole=126, modulo=25, residue=1),
    dict(whole=150, modulo=25, residue=0),
    dict(whole=76,  modulo=22, residue=10),
    # the follwing have been found with GAP
    dict(whole=(71**6 * 73**11 * 97**5 * 673),
         modulo=(29 * 67**2 * 101**3),
         residue=16636952179),
    dict(whole=(3**500 * 5**50),
         modulo=11**27,
         residue=703780454821668921429157503L)
]

addition_data = [
    dict(modulo=2,   addend1=1,   addend2=1,   result=0),
    dict(modulo=3,   addend1=1,   addend2=2,   result=0),
    dict(modulo=49,  addend1=1,   addend2=-16, result=34),
    dict(modulo=97,  addend1=50,  addend2=50,  result=3),
    dict(modulo=100, addend1=99,  addend2=23,  result=22),
    dict(modulo=100, addend1=8,   addend2=-44, result=64),
    # try with big values
    dict(modulo  = 2**500 + 47**100,
         addend1 = 2**500 - 23,
         addend2 = 47**100 + 45,
         result  = 22
    ),
    # try with huge values
    dict(modulo  = 31**500 + 55**300,
         addend1 = 31**500 - 10**54,
         addend2 = 55**300 + 11**52,
         result  = 420429319844313329730664601483335671261683881745483121
    ),
]

multiplication_data = [
    dict(modulo=2,   factor1=1,   factor2=1,    result=1),
    dict(modulo=3,   factor1=1,   factor2=2,    result=2),
    dict(modulo=3,   factor1=2,   factor2=2,    result=1),
    dict(modulo=15,  factor1=10,  factor2=3,    result=0),
    dict(modulo=49,  factor1=7,   factor2=7,    result=0),
    dict(modulo=97,  factor1=96,  factor2=96,   result=1),
    dict(modulo=97,  factor1=-98, factor2=193,  result=1),
    dict(modulo=100, factor1=11,  factor2=21,   result=31),
    dict(modulo=100, factor1=23,  factor2=55,   result=65),
    dict(modulo=100, factor1=223, factor2=1055, result=65),
    dict(modulo=73,  factor1=71,  factor2=68,   result=10),
    dict(modulo=73,  factor1=-1,  factor2=68,   result=5),
    dict(modulo=6275631, factor1=732523416, factor2=1553146,
         result=4756614),
    # try with big values
    dict(modulo  = 2**50 * 47**100,
         factor1 = 2**50 + 1,
         factor2 = 47**100 - 1,
         result  = 47**100 - 2**50 - 1,
    ),
    # try with huge values
    dict(modulo  = 71**513 * 47**911,
         factor1 = 47 * (71**512 + 1),
         factor2 = 71 * (47**910 + 1),
         result  = 47 * 71**513 + 71 * 47**911 + 47 * 71,
    ),
]

additive_inversion_data = [
    dict(modulo=2,   residue=0,   inverse=0),
    dict(modulo=2,   residue=1,   inverse=1),
    dict(modulo=3,   residue=0,   inverse=0),
    dict(modulo=3,   residue=1,   inverse=2),
    dict(modulo=55,  residue=49,  inverse=6),
    dict(modulo=97,  residue=24,  inverse=73),
    dict(modulo=121, residue=11, inverse=110),
    dict(modulo=14513461357231752457,
         residue=9734356935945946979,
         inverse=4779104421285805478),
]

multiplicative_inversion_data = [
    dict(modulo=2,  residue=1,   reciprocal=1),
    dict(modulo=3,  residue=2,   reciprocal=2),
    dict(modulo=5,  residue=2,   reciprocal=3),
    dict(modulo=8,  residue=3,   reciprocal=3),
    dict(modulo=8,  residue=3,   reciprocal=3),
    dict(modulo=50, residue=7,   reciprocal=43),
    dict(modulo=50, residue=-17, reciprocal=47),
    dict(modulo=50, residue=3,   reciprocal=17),
    dict(modulo=55, residue=7,   reciprocal=8),
    dict(modulo=97, residue=48,  reciprocal=95),
    dict(modulo=97, residue=12,  reciprocal=89),
    dict(modulo=97, residue=-1,  reciprocal=96),
    dict(modulo=97, residue=-6,  reciprocal=16),
    # try with big values (result found with GAP)
    dict(modulo     = 31**41,
         residue    = 23**23 + 1,
         reciprocal = 12314522799775017007991696109927229269151916254315470214920129
    ),
]

division_data = [
    dict(modulo=2,   dividend=0,  divisor=1,  result=0),
    dict(modulo=2,   dividend=1,  divisor=1,  result=1),
    dict(modulo=3,   dividend=0,  divisor=1,  result=0),
    dict(modulo=3,   dividend=1,  divisor=1,  result=1),
    dict(modulo=3,   dividend=2,  divisor=1,  result=2),
    dict(modulo=3,   dividend=1,  divisor=2,  result=2),
]

exponentiation_data = [

    dict(modulo=2,   base=0,  exponent=1,   result=0),
    dict(modulo=2,   base=0,  exponent=4,   result=0),
    dict(modulo=2,   base=1,  exponent=0,   result=1),
    dict(modulo=2,   base=1,  exponent=1,   result=1),

    dict(modulo=3,   base=2,  exponent=0,   result=1),
    dict(modulo=3,   base=2,  exponent=1,   result=2),
    dict(modulo=3,   base=2,  exponent=2,   result=1),

    dict(modulo=5,   base=2,  exponent=0,   result=1),
    dict(modulo=5,   base=2,  exponent=1,   result=2),
    dict(modulo=5,   base=2,  exponent=2,   result=4),
    dict(modulo=5,   base=2,  exponent=3,   result=3),
    dict(modulo=5,   base=2,  exponent=4,   result=1),
    dict(modulo=5,   base=3,  exponent=0,   result=1),
    dict(modulo=5,   base=3,  exponent=1,   result=3),
    dict(modulo=5,   base=3,  exponent=2,   result=4),
    dict(modulo=5,   base=3,  exponent=3,   result=2),
    dict(modulo=5,   base=3,  exponent=4,   result=1),

    dict(modulo=10,  base=2,  exponent=2,   result=4),
    dict(modulo=10,  base=3,  exponent=3,   result=7),
    dict(modulo=100, base=5,  exponent=3,   result=25),
    dict(modulo=100, base=20, exponent=2,   result=0),
    dict(modulo=35,  base=6,  exponent=2,   result=1),
    dict(modulo=35,  base=6,  exponent=16,  result=1),
    dict(modulo=3,   base=2,  exponent=100, result=1),
    dict(modulo=5,   base=7,  exponent=44,  result=1),

    dict(modulo=797159,    base=3,  exponent=13,  result=5),
    dict(modulo=7**30-1,   base=7,  exponent=32,  result=49),
    dict(modulo=7**30+1,   base=7,  exponent=31,  result=7**30-6),
    dict(modulo=97**300-1, base=97, exponent=322, result=97**22),

    # tests for QoI w.r.t. speed
    dict(modulo=5**20,   base=7**10,  exponent=4*(5**19),    result=1),
    dict(modulo=5**100,  base=3**100, exponent=4*(5**99),    result=1),
    dict(modulo=47**60,  base=45*20,  exponent=46*(47**59),  result=1),
    dict(modulo=97**200, base=53*120, exponent=96*(97**199), result=1),

    # stress tests for QoI w.r.t. speed
    dict(modulo=11**2001,  base=2, exponent=10*(11**2000), result=1),
    dict(modulo=2047**365, base=1111*273, exponent=11*88*(2047**364),
         result=1),

]

stringify_data = [
    dict(whole=0,   modulo=1,  string="0 (mod 1)" ),
    dict(whole=1,   modulo=1,  string="0 (mod 1)" ),
    dict(whole=0,   modulo=2,  string="0 (mod 2)" ),
    dict(whole=1,   modulo=2,  string="1 (mod 2)" ),
    dict(whole=11,  modulo=2,  string="1 (mod 2)" ),
    dict(whole=4,   modulo=10, string="4 (mod 10)"),
    dict(whole=122, modulo=10, string="2 (mod 10)"),
    dict(whole=5,   modulo=11, string="5 (mod 11)"),
    dict(whole=72,  modulo=11, string="6 (mod 11)"),
    dict(whole=21729679117, modulo=11, string="3 (mod 11)"),
    dict(whole=157895784639783246708365073, modulo=13,
         string="9 (mod 13)"),
    dict(whole=24723672576589724589756828724, modulo=825461974345357,
         string="152921409798503 (mod 825461974345357)"),
]

# py.test special hook function to generate test input.
def pytest_generate_tests(metafunc):
    funcargs = metafunc.funcargnames
    if not funcargs:
        pass # test function without arguments
    elif set(["prime_modulo"]) == set(funcargs):
        for p in primes:
            metafunc.addcall(funcargs={'prime_modulo': p})
    elif set(["whole", "modulo", "residue"]) == set(funcargs):
        for d in init_known_values:
            metafunc.addcall(funcargs=d)
    elif set(["modulo", "residue", "inverse"]) == set(funcargs):
        for d in additive_inversion_data:
            metafunc.addcall(funcargs=d)
            if d["inverse"] != d["residue"]:
                d1 = dict(modulo=d["modulo"],
                          residue=d["inverse"],
                          inverse=d["residue"])
                metafunc.addcall(funcargs=d1)
    elif set(["modulo", "addend1", "addend2", "result"]) == set(funcargs):
        for d in addition_data:
            metafunc.addcall(funcargs=d)
            if d["addend1"] != d["addend2"]:
                d1 = d.copy()
                d1["addend1"], d1["addend2"] = d1["addend2"], d1["addend1"]
                metafunc.addcall(funcargs=d1)
    elif set(["modulo", "minuend", "subtrahend", "result"]) == set(funcargs):
        for d in addition_data:
            d1 = dict(modulo=d["modulo"],
                      result=d["result"],
                      minuend=d["addend1"],
                      subtrahend=-d["addend2"])
            metafunc.addcall(funcargs=d1)
    elif set(["modulo", "factor1", "factor2", "result"]) == set(funcargs):
        for d in multiplication_data:
            d0, d1, d2, d3 = d.copy(), d.copy(), d.copy(), d.copy()
            d1["factor1"] *= -1
            if d1["result"] != 0:
                d1["result"] = d1["modulo"] - d1["result"]
            d2["factor2"] *= -1
            if d2["result"] != 0:
                d2["result"] = d2["modulo"] - d2["result"]
            d3["factor1"] *= -1
            d3["factor2"] *= -1
            for x in (d0, d1, d2, d3):
                metafunc.addcall(funcargs=x)
                x1 = x.copy()
                x1["factor1"], x1["factor2"] = x1["factor2"], x1["factor1"]
                metafunc.addcall(funcargs=x1)
    elif set(["modulo", "dividend", "divisor", "result"]) == set(funcargs):
        for d in division_data:
            metafunc.addcall(funcargs=d)
    elif set(["modulo", "residue", "reciprocal"]) == set(funcargs):
        for d in multiplicative_inversion_data:
            d0, d1, d2 = d.copy(), d.copy(), d.copy()
            d1["residue"] *= -1
            d1["reciprocal"] = d1["modulo"] - d1["reciprocal"]
            d2["residue"] = d2["modulo"] - d2["residue"]
            d2["reciprocal"] = d2["modulo"] - d2["reciprocal"]
            for x in (d0, d1, d2):
                metafunc.addcall(funcargs=x)
    elif set (["modulo", "base", "exponent", "result"]) == set(funcargs):
        for d in exponentiation_data:
            metafunc.addcall(funcargs=d)
            d1 = d.copy()
            if d['exponent'] % 2 == 1:
                if d['result'] != 0:
                    d1['result'] = d['modulo'] - d['result']
            d1['base'] = d['modulo'] - d['base']
            metafunc.addcall(funcargs=d1)
    elif set(["whole", "modulo", "string"]) == set(funcargs):
        for d in stringify_data:
            metafunc.addcall(funcargs=d)
    else: # sanity check
        raise RuntimeError("bad funcargsnames list: %r" % funcargs)


### TESTS


def test_integermod_named_params():
    # Use of IntegerMod with named parameters.
    class IntegerMod2(RSA.IntegerMod):
        modulo = 2
    assert IntegerMod2(whole=1) == IntegerMod2(1)


def test_integermod_direct_instantiation_exception():
    # check that direct instantiation of IntegerMod fails properly
    py.test.raises(RSA.IMRuntimeError, "RSA.IntegerMod(1)")

def test_integermod_subclass_no_modulo_instantiation_exception():
    # check that instantiation of an IntegerMod subclass fails if
    # `modulo' class attribute is not overridden
    class integermod_subclass(RSA.IntegerMod): pass
    py.test.raises(RSA.IMRuntimeError, "integermod_subclass(1)")


# Test that 'whole % modulo == residue' (subclassing IntegerMod)
def test_make_int_modulo_int(whole, modulo, residue):
    class integermod_subclass(RSA.IntegerMod):
        pass
    integermod_subclass.modulo = modulo
    got = integermod_subclass(whole).residue
    assert residue == got, \
           "%u = %u != %u (mod %u)" % (whole, got, residue, modulo)


# Test that an IntegerMods can be converte to itself.
def test_int_modulo_int_to_itself(whole, modulo, residue):
    class integermod_subclass(RSA.IntegerMod):
        pass
    integermod_subclass.modulo = modulo
    integermod_instance1 = integermod_subclass(whole)
    integermod_instance2 = integermod_subclass(integermod_instance1)
    assert integermod_instance1 == integermod_instance2

# Test that an IntegerMod converte to itself return a copy, not
# a reference to self.
def test_int_modulo_int_to_itself_copy_not_ref():
    class integermod_subclass(RSA.IntegerMod):
        modulo = 5
    integermod_instance1 = integermod_subclass(1)
    integermod_instance2 = integermod_subclass(integermod_instance1)
    assert integermod_instance1 is not integermod_instance2


def test_stringify(whole, modulo, string):
    class integermod_subclass(RSA.IntegerMod):
        pass
    integermod_subclass.modulo = modulo
    assert str(integermod_subclass(whole)) == string


def test_integermod_different_subclasses_not_equal():
    class integermod_subclass_1(RSA.IntegerMod):
        modulo = 2
    class integermod_subclass_2(RSA.IntegerMod):
        modulo = 2
    instance_subclass_1 = integermod_subclass_1(1)
    instance_subclass_2 = integermod_subclass_2(1)
    # In case both __eq__ and __neq__ are defined
    assert ((instance_subclass_1 != instance_subclass_2)
            and not (instance_subclass_1 == instance_subclass_2))


def test_integermod_equality(whole, modulo, residue):
    cls = TL.integers_mod(modulo)
    assert (cls(whole) == cls(whole) and
            cls(whole) == cls(residue) and
            cls(residue) == cls(whole))

def test_integermod_equality_negated(whole, modulo, residue):
    cls = TL.integers_mod(modulo)
    if modulo != 1:
        assert (not (cls(whole+1) == cls(whole)) and
                not (cls(whole) == cls(residue+1)) and
                not (cls(whole+1) == cls(residue)))

def test_integermod_inequality_negated(whole, modulo, residue):
    cls = TL.integers_mod(modulo)
    assert (not (cls(whole) != cls(whole)) and
            not (cls(whole) != cls(residue)) and
            not (cls(residue) != cls(whole)))

def test_integermod_inequality(whole, modulo, residue):
    cls = TL.integers_mod(modulo)
    if modulo != 1:
        assert (cls(whole+1) != cls(whole) and
                cls(whole) != cls(residue+1) and
                cls(whole+1) != cls(residue))


def test_integermod_add(modulo, addend1, addend2, result):
    cls = TL.integers_mod(modulo)
    assert (cls(addend1) + cls(addend2)).residue == result

def test_integermod_ladd(modulo, addend1, addend2, result):
    cls = TL.integers_mod(modulo)
    assert (cls(addend1) + addend2).residue == result

def test_integermod_radd(modulo, addend1, addend2, result):
    cls = TL.integers_mod(modulo)
    assert (addend1 + cls(addend2)).residue == result


def test_integermod_sub(modulo, minuend, subtrahend, result):
    cls = TL.integers_mod(modulo)
    assert (cls(minuend) - cls(subtrahend)).residue == result

def test_integermod_lsub(modulo, minuend, subtrahend, result):
    cls = TL.integers_mod(modulo)
    assert (cls(minuend) - subtrahend).residue == result

def test_integermod_rsub(modulo, minuend, subtrahend, result):
    cls = TL.integers_mod(modulo)
    assert (minuend - cls(subtrahend)).residue == result


def test_integermod_mul(modulo, factor1, factor2, result):
    cls = TL.integers_mod(modulo)
    assert (cls(factor2) * cls(factor1)).residue == result

def test_integermod_lmul(modulo, factor1, factor2, result):
    cls = TL.integers_mod(modulo)
    assert (cls(factor1) * factor2).residue == result

def test_integermod_rmul(modulo, factor1, factor2, result):
    cls = TL.integers_mod(modulo)
    assert (factor1 * cls(factor2)).residue == result


def test_integermod_div(modulo, dividend, divisor, result):
    cls = TL.integers_mod(modulo)
    assert (cls(dividend) / cls(divisor)).residue == result

def test_integermod_ldiv(modulo, dividend, divisor, result):
    cls = TL.integers_mod(modulo)
    assert (cls(dividend) / divisor).residue == result

def test_integermod_rdiv(modulo, dividend, divisor, result):
    cls = TL.integers_mod(modulo)
    assert (dividend / cls(divisor)).residue == result


def test_integermod_inverse(modulo, residue, inverse):
    cls = TL.integers_mod(modulo)
    assert (- cls(residue)).residue == inverse


def test_integermod_reciprocal_pow(modulo, residue, reciprocal):
    cls = TL.integers_mod(modulo)
    assert (cls(residue)**(-1)).residue == reciprocal

def test_integermod_reciprocal_rdiv(modulo, residue, reciprocal):
    cls = TL.integers_mod(modulo)
    assert ((cls(1)/residue).residue == reciprocal)

def test_integermod_reciprocal_ldiv(modulo, residue, reciprocal):
    cls = TL.integers_mod(modulo)
    assert ((1/cls(residue)).residue == reciprocal)

def test_integermod_invalid_reciprocal():
    cls = TL.integers_mod(55)
    py.test.raises(RSA.IMValueError, "cls(0)**(-1)")
    py.test.raises(RSA.IMValueError, "cls(5)**(-1)")
    py.test.raises(RSA.IMValueError, "cls(11)**(-1)")
    py.test.raises(RSA.IMValueError, "cls(44)**(-1)")
    py.test.raises(RSA.IMValueError, "cls(55)**(-1)")

def test_prime_integermod_reciprocal(prime_modulo):
    cls = TL.integers_mod(prime_modulo)
    if prime_modulo == 2:
        x = y = 1
    else:
        x = (prime_modulo - 1) / 2
        y = prime_modulo - 2
    assert (cls(x)**(-1)) == cls(y)


def test_integermod_exponentiation(modulo, base, exponent, result):
    cls = TL.integers_mod(modulo)
    assert ((cls(base) ** exponent).residue == result)

def test_fermat_little_theorem(prime_modulo):
    cls = TL.integers_mod(prime_modulo)
    for d in (2, 3, 10):
        x = max(1, prime_modulo/d)
        assert cls(x)**(prime_modulo - 1) == cls(1)


# vim: et sw=4 ts=4 ft=python
