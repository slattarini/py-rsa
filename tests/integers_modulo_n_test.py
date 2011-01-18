#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for the RSA.py's implementation of integers (mod n)"""
import pytest
import RSA
from tests.pyrsa_testlib import with_params, without_duplicates, \
                                integers_mod, pytest_generate_tests


###  DATA


# obtained with GAP, but could also be looked upon a simple table
small_primes  = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 97, ]
medium_primes = [ 131, 151, 157, 181, 241, 269, 271, 307, ]
large_primes  = [ 373, 397, 401, 433, 499, 523, 541, 571, 641, 659,
                  661, 701, 773, 811, 821, 853, 929, 953, 967, 997, ]
primes = small_primes + medium_primes + large_primes


@without_duplicates
def define_init_known_values():
    data = []
    for d in [
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
    ]:
        d0, d1 = d.copy(), d.copy()
        d1["whole"] = - d1["whole"]
        if d1["residue"] != 0:
            d1["residue"] = d1["modulo"] - d1["residue"]
        data.extend([d0, d1])
    return data

@without_duplicates
def define_stringify_data():
    return [
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
        dict(whole=24723672576589724589756828724L, modulo=825461974345357L,
             string="152921409798503 (mod 825461974345357)"),
    ]

@without_duplicates
def define_addition_data():
    data = []
    for d in [
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
             result  = 22),
        # try with huge values
        dict(modulo  = 31**500 + 55**300,
             addend1 = 31**500 - 10**54,
             addend2 = 55**300 + 11**52,
             # this is simply (11**52 - 10**54), calculated with GAP.
             result  = 420429319844313329730664601483335671261683881745483121,
        ),
    ]:
        d0, d1 = d.copy(), d.copy()
        # swap the two addends
        d1["addend1"], d1["addend2"] = d1["addend2"], d1["addend1"]
        data.extend([d0, d1])
    return data

@without_duplicates
def define_subtraction_data():
    data = []
    for d in addition_data:
        data.append(dict(modulo=d["modulo"],
                         result=d["result"],
                         minuend=d["addend1"],
                         subtrahend=-d["addend2"]))
        if d["result"] == 0:
            result = 0
        else:
            result = d["modulo"] - d["result"]
        data.append(dict(modulo=d["modulo"],
                         result=result,
                         minuend=-d["addend1"],
                         subtrahend=d["addend2"]))
    return data

@without_duplicates
def define_multiplication_data():
    data = []
    for d in [
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
        # try with "medium" value
        dict(modulo=6275631,
             factor1=732523416,
             factor2=1553146,
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
    ]:
        # Given a*b, we want to try also a*(-b), (-a)*b, (-a)*(-b).
        d0, d1, d2, d3 = d.copy(), d.copy(), d.copy(), d.copy()
        # ---
        d1["factor1"] *= -1
        if d1["result"] != 0:
            d1["result"] = d1["modulo"] - d1["result"]
        # ---
        d2["factor2"] *= -1
        if d2["result"] != 0:
            d2["result"] = d2["modulo"] - d2["result"]
        # ---
        d3["factor1"] *= -1
        d3["factor2"] *= -1
        # ---
        data.extend([d0, d1, d2, d3])
        # Given a*b, we want to try also b*a.
        for x in (d0, d1, d2, d3):
            x = x.copy()
            x["factor1"], x["factor2"] = x["factor2"], x["factor1"]
            data.append(x)
    return data

@without_duplicates
def define_additive_inversion_data():
    data = []
    for d in [
        dict(modulo=2,   residue=0,   inverse=0),
        dict(modulo=2,   residue=1,   inverse=1),
        dict(modulo=3,   residue=0,   inverse=0),
        dict(modulo=3,   residue=1,   inverse=2),
        dict(modulo=55,  residue=49,  inverse=6),
        dict(modulo=97,  residue=24,  inverse=73),
        dict(modulo=121, residue=11,  inverse=110),
        dict(modulo=14513461357231752457,
             residue=9734356935945946979,
             inverse=4779104421285805478),
    ]:
        d0, d1 = d.copy(), d.copy()
        # If -a = b, then -b = a; so check this too.
        d1["inverse"], d1["residue"] = d1["residue"], d1["inverse"]
        data.extend([d0, d1])
    return data

@without_duplicates
def define_multiplicative_inversion_data():
    data = []
    for d in [
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
    ]:
        d0, d1, d2 = d.copy(), d.copy(), d.copy()
        # Given a^-1, we want to try also (-a)^-1, in two different
        # "flavors".
        # ---
        d1["residue"] *= -1
        d1["reciprocal"] = d1["modulo"] - d1["reciprocal"]
        # ---
        d2["residue"] = d2["modulo"] - d2["residue"]
        d2["reciprocal"] = d2["modulo"] - d2["reciprocal"]
        # ---
        data.extend([d0, d1, d2])
    return data

@without_duplicates
def define_division_data():
    data = []
    for d in [
        dict(modulo=2,   dividend=0,  divisor=1,  result=0),
        dict(modulo=2,   dividend=1,  divisor=1,  result=1),
        dict(modulo=3,   dividend=0,  divisor=1,  result=0),
        dict(modulo=3,   dividend=1,  divisor=1,  result=1),
        dict(modulo=3,   dividend=2,  divisor=1,  result=2),
        dict(modulo=3,   dividend=1,  divisor=2,  result=2),
        dict(modulo=55,  dividend=45, divisor=9,  result=5),
        dict(modulo=49,  dividend=44, divisor=39, result=25),
        dict(modulo=101, dividend=2,  divisor=51, result=4),
        # found with GAP
        dict(modulo   = 7264563962592586452347,
             dividend = 62354131224573468,
             divisor  = 1235413624573468,
             result   = 6792538694198912916609),
    ]:
        # Given a*b, we want to try also a*(-b), (-a)*b, (-a)*(-b).
        d0, d1, d2, d3 = d.copy(), d.copy(), d.copy(), d.copy()
        # ---
        d1["dividend"] *= -1
        if d1["result"] != 0:
            d1["result"] = d1["modulo"] - d1["result"]
        # ---
        d2["divisor"] *= -1
        if d2["result"] != 0:
            d2["result"] = d2["modulo"] - d2["result"]
        # ---
        d3["dividend"] *= -1
        d3["divisor"] *= -1
        # ---
        data.extend([d0, d1, d2, d3])
    return data

@without_duplicates
def define_exponentiation_data():
    data = []
    for d in [
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
        dict(modulo=5**20,   base=7**10,  exponent=4*(5**19),     result=1),
        dict(modulo=5**100,  base=3**100, exponent=4*(5**99),     result=1),
        dict(modulo=47**60,  base=45**20,  exponent=46*(47**59),  result=1),
        dict(modulo=97**200, base=53**120, exponent=96*(97**199), result=1),

        # stress tests for QoI w.r.t. speed
        dict(modulo=11**2001,  base=2, exponent=10*(11**2000), result=1),
        dict(modulo=2047**365, base=1111*273, exponent=11*88*(2047**364),
            result=1),
    ]:
        # Given a^n, we want to try also (-a)^n, in two different
        # "flavors".
        d0, d1, d2 = d.copy(), d.copy(), d.copy()
        d1['base'] = - d0['base']
        d2['base'] = d0['modulo'] - d0['base']
        if d0['exponent'] % 2 == 1 and d0['result'] != 0:
            d2['result'] = d1['result'] = d0['modulo'] - d0['result']
        data.extend([d0, d1, d2])
    return data

@without_duplicates
def define_noncoprime_modulo_and_residue_data():
    data = []
    for d in [
        dict(modulo=2,  residue=0),
        dict(modulo=5,  residue=0),
        dict(modulo=6,  residue=3),
        dict(modulo=12, residue=2),
        dict(modulo=12, residue=3),
        dict(modulo=12, residue=4),
        dict(modulo=12, residue=6),
        dict(modulo=12, residue=9),
        dict(modulo=55, residue=0),
        dict(modulo=55, residue=5),
        dict(modulo=55, residue=11),
        dict(modulo=55, residue=44),
        dict(modulo=100000, residue=222),
        dict(modulo=(3 ** 5 * 17**2 * 23**3), residue=(3 * 11)),
        dict(modulo=(3 ** 5 * 17**2 * 23**3), residue=(2**8 * 17**3)),
        # try also with big modules
        dict(modulo=2**10000,          residue=2**4000),
        dict(modulo=3**10000*47**1000, residue=3**12000*37**1000),
    ]:
        # g.c.d. (a, n) = 1 iff g.c.d. (-a, n) = 1
        # "flavors".
        d0, d1 = d.copy(), d.copy()
        d1['residue'] *= -1
        data.extend([d0, d1])
    return data


init_known_values = define_init_known_values()
stringify_data = define_stringify_data()
addition_data = define_addition_data()
subtraction_data = define_subtraction_data()
multiplication_data = define_multiplication_data()
division_data = define_division_data()
additive_inversion_data = define_additive_inversion_data()
multiplicative_inversion_data = define_multiplicative_inversion_data()
exponentiation_data = define_exponentiation_data()
noncoprime_modulo_and_residue_data = define_noncoprime_modulo_and_residue_data()


### TESTS

def test_integermod_repr():
    class MyType(type):
        def __repr__(self):
            return self.__name__
    class MyClass(RSA.IntegerMod):
        __metaclass__ = MyType
        modulo = 5
    class MySubClass(MyClass):
        modulo = 11
    assert (repr(MyClass(23)) == "MyClass(3)"
            and repr(MySubClass(23)) == "MySubClass(1)")

@with_params([integers_mod], 'factory')
def test_integermod_named_params(factory):
    IntegerMod2 = factory(2)
    assert IntegerMod2(whole=1) == IntegerMod2(1)


def test_integermod_direct_instantiation_exception():
    pytest.raises(RSA.IMRuntimeError, "RSA.IntegerMod(1)")

def test_integermod_subclass_no_modulo_instantiation_exception():
    # check that instantiation of an IntegerMod subclass fails if
    # `modulo' class attribute is not overridden
    class integermod_subclass(RSA.IntegerMod): pass
    pytest.raises(RSA.IMRuntimeError, "integermod_subclass(1)")


# Test that 'whole % modulo == residue' (subclassing IntegerMod)
@with_params([integers_mod], 'factory')
@with_params(init_known_values)
def test_make_int_modulo_int(whole, modulo, residue, factory):
    got = factory(modulo)(whole).residue
    assert residue == got, \
           "%u = %u != %u (mod %u)" % (whole, got, residue, modulo)


# Test that an IntegerMods can be converted to itself.
@with_params([integers_mod], 'factory')
@with_params(init_known_values)
def test_int_modulo_int_to_itself(whole, modulo, residue, factory):
    integermod_subclass = factory(modulo)
    integermod_instance1 = integermod_subclass(whole)
    integermod_instance2 = integermod_subclass(integermod_instance1)
    assert integermod_instance1 == integermod_instance2

# Test that an IntegerMod converte to itself return a copy, not
# a reference to self.
@with_params([integers_mod], 'factory')
def test_int_modulo_int_to_itself_copy_not_ref(factory):
    integermod_subclass = factory(5)
    integermod_instance1 = integermod_subclass(1)
    integermod_instance2 = integermod_subclass(integermod_instance1)
    assert integermod_instance1 is not integermod_instance2

@with_params([integers_mod], 'factory')
def test_integermod_different_subclasses_not_equal(factory):
    integermod_subclass_1 = factory(2)
    integermod_subclass_2 = factory(2)
    instance_subclass_1 = integermod_subclass_1(1)
    instance_subclass_2 = integermod_subclass_2(1)
    # In case both __eq__ and __neq__ are defined
    assert ((instance_subclass_1 != instance_subclass_2)
            and not (instance_subclass_1 == instance_subclass_2))


@with_params([integers_mod], 'factory')
@with_params(stringify_data)
def test_stringify(whole, modulo, string, factory):
    integermod_subclass = factory(modulo)
    assert str(integermod_subclass(whole)) == string


@with_params([integers_mod], 'factory')
@with_params(init_known_values)
def test_integermod_equality(whole, modulo, residue, factory):
    cls = factory(modulo)
    assert (cls(whole) == cls(whole) and
            cls(whole) == cls(residue) and
            cls(residue) == cls(whole))

@with_params([integers_mod], 'factory')
@with_params(init_known_values)
def test_integermod_equality_negated(whole, modulo, residue, factory):
    cls = factory(modulo)
    if modulo != 1:
        assert (not (cls(whole+1) == cls(whole)) and
                not (cls(whole) == cls(residue+1)) and
                not (cls(whole+1) == cls(residue)))

@with_params([integers_mod], 'factory')
@with_params(init_known_values)
def test_integermod_inequality_negated(whole, modulo, residue, factory):
    cls = factory(modulo)
    assert (not (cls(whole) != cls(whole)) and
            not (cls(whole) != cls(residue)) and
            not (cls(residue) != cls(whole)))

@with_params([integers_mod], 'factory')
@with_params(init_known_values)
def test_integermod_inequality(whole, modulo, residue, factory):
    cls = factory(modulo)
    if modulo != 1:
        assert (cls(whole+1) != cls(whole) and
                cls(whole) != cls(residue+1) and
                cls(whole+1) != cls(residue))


@with_params([integers_mod], 'factory')
@with_params(addition_data)
def test_integermod_add(modulo, addend1, addend2, result, factory):
    cls = factory(modulo)
    assert (cls(addend1) + cls(addend2)).residue == result

@with_params([integers_mod], 'factory')
@with_params(addition_data)
def test_integermod_ladd(modulo, addend1, addend2, result, factory):
    cls = factory(modulo)
    assert (cls(addend1) + addend2).residue == result

@with_params([integers_mod], 'factory')
@with_params(addition_data)
def test_integermod_radd(modulo, addend1, addend2, result, factory):
    cls = factory(modulo)
    assert (addend1 + cls(addend2)).residue == result


@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_sub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    assert (cls(minuend) - cls(subtrahend)).residue == result

@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_lsub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    assert (cls(minuend) - subtrahend).residue == result

@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_rsub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    assert (minuend - cls(subtrahend)).residue == result


@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_mul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    assert (cls(factor2) * cls(factor1)).residue == result

@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_lmul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    assert (cls(factor1) * factor2).residue == result

@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_rmul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    assert (factor1 * cls(factor2)).residue == result


@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_div(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    assert (cls(dividend) / cls(divisor)).residue == result

@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_ldiv(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    assert (cls(dividend) / divisor).residue == result

@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_rdiv(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    assert (dividend / cls(divisor)).residue == result


@with_params([integers_mod], 'factory')
@with_params(additive_inversion_data)
def test_integermod_inverse(modulo, residue, inverse, factory):
    cls = factory(modulo)
    assert (- cls(residue)).residue == inverse


@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_pow(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    assert (cls(residue)**(-1)).residue == reciprocal

@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_rdiv(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    assert ((cls(1)/residue).residue == reciprocal, factory)

@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_ldiv(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    assert ((1/cls(residue)).residue == reciprocal)


@with_params([integers_mod], 'factory')
@with_params(noncoprime_modulo_and_residue_data)
def test_integermod_invalid_reciprocal_pow(modulo, residue, factory):
    cls = factory(modulo)
    pytest.raises(RSA.IMValueError, "cls(%d)**(-1)" % residue)

@with_params([integers_mod], 'factory')
@with_params(noncoprime_modulo_and_residue_data)
def test_integermod_invalid_reciprocal_rdiv(modulo, residue, factory):
    cls = factory(modulo)
    pytest.raises(RSA.IMValueError, "cls(1)/%d" % residue)

@with_params([integers_mod], 'factory')
@with_params(noncoprime_modulo_and_residue_data)
def test_integermod_invalid_reciprocal_ldiv(modulo, residue, factory):
    cls = factory(modulo)
    pytest.raises(RSA.IMValueError, "1/cls(%d)" % residue)


@with_params([integers_mod], 'factory')
@with_params(exponentiation_data)
def test_integermod_exponentiation(modulo, base, exponent, result, factory):
    cls = factory(modulo)
    assert ((cls(base) ** exponent).residue == result)


@with_params([integers_mod], 'factory')
@with_params(primes, 'p')
def test_prime_integermod_reciprocal(p, factory):
    cls = factory(p)
    if p == 2:
        x = y = 1
    else:
        x = (p - 1) / 2
        y = p - 2
    assert (cls(x)**(-1)) == cls(y)


@with_params([integers_mod], 'factory')
@with_params(primes, 'p')
def test_fermat_little_theorem(p, factory):
    cls = factory(p)
    for d in (2, 3, 10):
        x = max(1, p/d)
        assert cls(x)**(p - 1) == cls(1)

@with_params([integers_mod], 'factory')
@with_params(primes, 'p')
def test_integermod_reciprocal_power_of_prime(p, factory):
    # It can be proved that if p is prime and:
    #  a^-1 = b (mod p^n)
    # then:
    #  a^-1 = 2 * b - a * b^2 (mod p^(n+1))
    modp100 = factory(p**120)
    modp101 = factory(p**121)
    if p == 5:
        a = 3**113
    else:
        a = 5**113
    b = (modp100(a)**(-1)).residue
    b_exp = modp101(2 * b - a * b**2)
    b_got = 1 / modp101(a)
    assert b_exp == b_got

# vim: et sw=4 ts=4 ft=python
