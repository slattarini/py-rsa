#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for our implementation of RSA applied to integers."""
from RSA import PublicKey, PrivateKey, BasicEncrypter, IntegerEncrypter
from tests.lib import s2i, with_params, without_duplicates, \
                      pytest_generate_tests
from tests.keys import keys

# ---------------------------- #
#  Create data for the tests.  #
# ---------------------------- #

# Temporary definition, will be post-processed later.
rsa_test_data = [

    # Sanity checks on the implementation(s).
    dict(
        key = keys['small'],
        encrypter_type = IntegerEncrypter,
        _ = [
            dict(
                plain  = 0,
                cipher = 0,
            ),
            dict(
                plain  = 1,
                cipher = 1,
            ),
            dict(
                plain  = 2,
                cipher = 32,
            ),
            dict(
                plain  = 5,
                cipher = 161,
            ),
            dict(
                plain  = 3,
                cipher = 243,
            ),
            dict(
                plain  =   3 +  2 * 247,
                cipher = 243 + 32 * 247,
            ),
            dict(
                plain  = 2  + 1 * 247 +   3 * 247**2,
                cipher = 32 + 1 * 247 + 243 * 247**2,
            ),
            dict(
                plain  = 13 +   5 * 247,
                cipher = 52 + 161 * 247,
            ),
            dict(
                plain  = 13 +   5 * 247,
                cipher = 52 + 161 * 247,
            ),
        ]
    ),

    # http://en.wikipedia.org/wiki/RSA#A_worked_example
    dict(
        key = keys['wikipedia'],
        encrypter_type = IntegerEncrypter,
        _ = [
            dict(
                plain = 65,
                cipher = 2790,
            ),
            dict(
                plain = 65 + 3233 + 65 * 3233**2,
                cipher = 2790 + 3233 + 2790 * 3233**2,
            ),
        ]
    ),

    # http://critto.liceofoscarini.it/critto/rsa/rsa_demo.phtml
    dict(
        key = keys['foscarini'],
        encrypter_type = IntegerEncrypter,
        _ = [
            dict(
                plain = 876,
                cipher = 20628,
            ),
            dict(
                # if plain = n + 1 ...
                plain = 31243,
                # ... we also expect that cipher = n + 1
                cipher = 31243,
            ),
            dict(
                plain  = (31243 * 876   + 30888 * 31243**7 + 157   * 31243**12),
                cipher = (31243 * 20628 + 3362  * 31243**7 + 20724 * 31243**12),
            ),
        ],
    ),

    # http://people.eku.edu/styere/Encrypt/RSAdemo.html
    dict(
        key = keys['styere_e17'],
        _ = [
            dict(
                plain = 0,
                cipher = 0,
            ),
            dict(
                plain = 2,
                cipher = 2**17, # because 2**17 < n
            ),
            dict(
                plain = 57128184570925880835232907122,
                cipher = 6764407817379484644525719120,
            ),
        ],
    ),

    # http://people.eku.edu/styere/Encrypt/RSAdemo.html
    dict(
        key = keys['styere_e19'],
        plain = s2i("""
            80921567314082977661194180175378694208028080487095042140
            99597921367850945315474143925943532423516957495472126238
            57652061972441899562100158646230426553421519267911017057
            92539724815673563824224453532477 """),
        cipher = s2i("""
            22137228139183158439669852364694862732482535535249847884
            49720954411001899921124803798801814042011086202993150254
            88274823131673309070513331643338514100983106623894620132
            88855973653488072253714991211499 """),
    ),

    # http://people.eku.edu/styere/Encrypt/RSAdemo.html
    dict(
        key = keys['styere_e23'],
        plain = s2i("""
            17236568092156731408297766119418017537869114208028080487
            09504214099597921367850945315474143925943532423516957495
            47212623857652061972441899562100158646230426553421519267
            91101705792539724815673563824224453532477555555555555555
            5588 """),
        cipher = s2i("""
            11249617172664411689713341259914189929078337526026500935
            12409469092809495376007898985547994042625180666716133109
            95539518373396124849705037687042903923722455371479737993
            13648904557753881822947487721378328739353698883280317580
            69913965098694112170747628063215395274847497730954321064
            35460126918014608277779654751194830369137001589355278527
            09123928225566443501117814878716331456545617304487076719
            40798934 """),
    ),

    # http://islab.oregonstate.edu/koc/ece575/02Project/Mor/
    dict(
        key = keys['oregonstate'],
        plain = s2i("""
            10011111101111000111101110000110011011011110110100000011
            10010011111000010011001011111011111101011010101100000111
            00000000010001101001101101011101010111000011111100001000
            11000010100101101101000110001101100111010111110100111100
            1000000010000110111101011011 """),
        cipher = s2i("""
            47367835209253383690467819493169886887363241045271912689
            00355152276480321075665546480570294956458929661801603950
            24876056438618301000575546096514331576813852538215249532
            73808652801320737566945327931249420476155674199927579554
            28425032803368870575661629088046064627442091904639948150
            9435413073426075477158765398 """),
    ),

    # http://islab.oregonstate.edu/koc/ece575/02Project/Mor/
    # Also check some corner cases.
    dict(
        key = keys['M2281_M2203'],
        encrypter_type = IntegerEncrypter,
        _ = [
            dict(
                plain = 1,
                cipher = 1,
            ),
            dict(
                # if plain = n + 1 ...
                plain = 2**4484 - 2**2281 - 2**2203 + 2,
                # ... we also expect that cipher = n + 1
                cipher= 2**4484 - 2**2281 - 2**2203 + 2,
            ),
            dict(
                # We should work correctly even if the message is not
                # coprime with n.
                plain = 2**2281 - 1,
                cipher = s2i("""
640061972037093167636558270100139108712369267897169070438891215707482244962
393307421036022966093171525790720912529525208236195591994399606764414667052
689699597644707387251579059824583202620366624568044047189018477774569237057
984312758300468647660060547039201938656675776829868870111548862963408700634
443762843535194017525863047464131469737571996543648853035295950268334373320
658101657032037374585564650676647903541268849934046871724964383676871027164
580939037756511161085906798072266989282710886895298330499675775133331041854
614699633235033862169196611036775505459393484389784535797018837826531517104
557019817271186955943673011402080468038732281704158574887592174157582382552
764025077596246395806065066356144886029698406052531346700276857150454156204
209493833592611276888027104925358078867028946530274102411281168141177020173
605372050120122515510144101888068611672259179745603938958760734685073657323
198650655769840690325153885201634266478132047556030315401289827833189030101
774143180468393071353273899920089978062483112024452001739059601426771737454
874680475996156242111493699523895107019786963547005804545235535165381345178
043394043270042857642881025267917608602596269142256184915821092621699050051
086044532654144866347347099452007408526905612788842555314231127906237465229
141597849471962808393653240794508699977270999861077998149018882121581684216
"""),
            ),
            dict(
                plain = 3**2000,
                cipher = s2i("""
233809301053491252688030600443670530842394086866430960416605728469810811696
508390132960387214408615701257439084340027749781724406984689209417293472019
451589843933378306480165645864951895113609011960106369048974775114147642802
130264712116801486685569327067201335629940087720970238528254365861134768622
625019693740671381645690866223309522423532714641432445793569630739992483408
549839487279912693187781651458009926142300626959206119949977103526056837098
292877997996647714045483172710437465562452148418493083466473472974976499414
197860960257242683231098232405437929111953671965237331880069844627496636645
312877617494480675629912138526026279186847647760470021217081311773422918185
541180221210037511965108977703120610133313896877803420683681495235881572188
532417692809395956458791646978084413996027835391671951675062145308353495429
027206728691825034752726484426528827489801042148286011444020204993808862425
363173235142958127996462264497564891846780380142781905119467970564345662126
072943587606217399625375390463178418233487040105054687814045193516588595223
007117152407905454390198455977934699590584247116131424895920491121462359579
252806685227660900388412508465521621753242395314849408901024863482759944125
025263347166077388947432501780663844879403271266975405379141297546816678258
472342336896979412551760711555160570273935158178609175610134979836216057998
"""),
            ),
        ],
    ),
] # rsa_test_data


def unravel_rsa_test_data(lst):
    unravelled_test_data = []
    for data_clump in [ x.copy() for x in lst ]:
        try:
            list_of_plain_encrypted_couples = data_clump['_']
        except KeyError:
            # There's only one datum in the clump.
            data_entries = [data_clump]
        else:
            # Unravel the data contained in the clump.
            del data_clump['_']
            data_entries = []
            for d in list_of_plain_encrypted_couples:
                data_entries.append(dict(data_clump, plain=d['plain'],
                                                     cipher=d['cipher']))
        for entry in data_entries:
            entry.setdefault('encrypter_type', BasicEncrypter)
        unravelled_test_data.extend(data_entries)
    return unravelled_test_data

rsa_test_data = unravel_rsa_test_data(rsa_test_data)

# -------------------- #
#  Go with the tests.  #
# -------------------- #

@with_params(rsa_test_data)
def test_encrypt_pubkey(key, plain, cipher, encrypter_type):
    encrypter = encrypter_type(PublicKey(key['n'], key['e']))
    assert encrypter.encrypt(plain) == cipher

@with_params(rsa_test_data)
def test_encrypt_privkey(key, plain, cipher, encrypter_type):
    encrypter = encrypter_type(PrivateKey(key['p'], key['q'], key['e']))
    assert encrypter.encrypt(plain) == cipher

@with_params(rsa_test_data)
def test_decrypt(key, plain, cipher, encrypter_type):
    encrypter = encrypter_type(PrivateKey(key['p'], key['q'], key['e']))
    assert encrypter.decrypt(cipher) == plain

# Without the Chinise Remainder theorem optimization, this would take
# a ridicoulously long time: on the test machine, it took ~ half an
# hour.  With the optimization enabled, it completes in ~ 200 seconds.
# FIXME: having a timeout here would be better than risking to have the
# testsuite almost hang ...
def test_decrypt_speed():
    p = 2**11213 - 1
    q = 2**9941 - 1
    e = 2**3217 - 1
    encrypter = BasicEncrypter(PrivateKey(p, q, e))
    encrypter.decrypt((p - 10) * (q - 23) / 2)

# vim: et sw=4 ts=4 ft=python
