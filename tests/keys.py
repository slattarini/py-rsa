#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Define RSA keys to be used in tests."""
from tests.lib import s2i


keys = {

    # useful for some basic checks
    'small' :
    dict(
        e = 5,
        p = 19,
        q = 13,
        d = 173,
    ),

    # http://en.wikipedia.org/wiki/RSA#A_worked_example
    'wikipedia' : 
    dict(
        e = 17,
        p = 61,
        q = 53,
        d = 2753,
    ),

    # http://critto.liceofoscarini.it/critto/rsa/rsa_demo.phtml
    'foscarini':
    dict(
        e = 5,
        p = 157,
        q = 199,
        d = 18533,
    ),

    # Generated by http://people.eku.edu/styere/Encrypt/RSAdemo.html
    # Hmpf, that page doesn't allow the user to choose `e' ...
    'styere_e17':
    dict(
        e = 17,
        p = 459983137786273,
        q = 167458717901777,
        d = 45310697947132401996104246513,
    ),

    # Again generated by http://people.eku.edu/styere/Encrypt/RSAdemo.html
    'styere_e19':
    dict(
        e = 19,
        p = s2i("""
            86076676546733337382541713532930911669195989929427722917
            74483174554334639686435205788216773797485261 """),
        q = s2i("""
            95172781525324761550958382729138993399010715034419778646
            91087067627598695056123147611078875505156657 """),
        d = s2i("""
            17246645750333258454988248457974461938532227470967377292
            84125878182705462171678767142303901562845674880626851687
            99905921783651713156251597987268518464404158865728125313
            38779996264720034637594768608539 """),
    ),

    # Again generated by http://people.eku.edu/styere/Encrypt/RSAdemo.html
    'styere_e23':
    dict(
        e = 23,
        p = s2i("""
            28489954601611388619553404108203940433044351078137040591
            81494348969757053217922323275113898676968284552125125922
            10205434892574383192749047579813853880999080798598532792
            76819931119816921680155926991183 """),
        q = s2i("""
            95713753930524166760301951288420363242532132446588458509
            17739142065187781401349506282049076294091685319583133052
            87247143534507773905136325071665562455341347287680839410
            18182719419208882940511234327813 """),
        d = s2i("""
            13041602411536873177932324086839210387734974362170542711
            66728395507358393175602814613078571745764324534050035660
            86468406181261236084581223222122995388713066371305795169
            10072894507181649976873703098222095822748464720003353323
            80210382741738587322414769736017557941047540983521045905
            04008577459287464238373847186202413102516208255578101792
            87439570860532280811085803806118248747666021377185831065
            92821375 """),
    ),

    # Generated by http://islab.oregonstate.edu/koc/ece575/02Project/Mor/
    'oregonstate' :
    dict(
        e = 11003726294547297341,
        p = s2i("""
            39922612611027959996394545074456026825528070497539331989
            65522778701176759774228164458929820969741232235437307666
            098693849666316699040528739377011697295297 """),
        q = s2i("""
            17777172157443534741640362925797767962391967472203175519
            74208260988332940678809197918545764552224898846609386062
            0045629916088136348616227187589818338698353 """),
        d = s2i("""
            63351870184876835585431387724817307426653355312934254433
            98757481676594836161596022553903775439617937319209185623
            43814069463941935041290726073178588924673147237234343289
            30934984753958699188098524755853400102146423188123417706
            69378009436948246256883151445897872307080823304524583421
            292732722435687824755422997 """),
    ),

    'M521_M607' :
    dict(
        p = 2**521 - 1,
        q = 2**607 - 1,
        e = (2**521 - 2) * (2**607 - 2) - 1,
        d = (2**521 - 2) * (2**607 - 2) - 1,
    ),

    # With help of http://islab.oregonstate.edu/koc/ece575/02Project/Mor/
    'M2281_M2203' :
    dict(
        p = 2**2281 - 1,
        q = 2**2203 - 1,
        e = 2**61 - 1,
        d = s2i("""
373604615764701937927552301550763558027191550794396688094290185732295365535
726544956941047127742595274459193015181479884225628326441864809144445285561
557567961426145593463891273851001402059737831250545031684591438017619186082
115682176425072739068276372139600491595495537880796048501601790999155838558
749887619914020288310736022122841400120443964913160503784484591562174077657
280780445991013982426902012057330960968801383024729922657266936849813493913
672247686280845821675257281318685404923028201778243992255066225983776024963
571959588183231845748597814767001008154821453425454875103445234982245354104
079271437422692697556950591749036381649031772019438708520207645271285833810
258741439239232865122290813168358276081158439520520202093918187175546979115
694397802838618976822047563734584739480796023845386548285274720892293514698
570156055782459219026346232868947562830670958954364135798778730237537593538
067026853919458717211033590194727811058551288044287187778552126973545907790
765753449566536974420096362934566266780967619199841194395845111118452693982
395851738717762005000005971527647211130038033222277760908180611772538035705
792669836348965460790910065700480584701557479927421632881656786256640444186
354747096246297579188206741738726953953948725327938766625915137595902076189
147582865318086912314710413714271658174241059221078105192161128780960995951
"""), ),

}

for key in keys.values():
    key['n'] = key['p'] * key['q']
del key

# vim: et sw=4 ts=4 ft=python
