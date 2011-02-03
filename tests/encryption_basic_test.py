#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for our implementation of RSA applied to integers."""
import pytest
import RSA
from tests.pyrsa_testlib import s2i, with_params, without_duplicates, \
                                pytest_generate_tests

# ---------------------------- #
#  Create data for the tests.  #
# ---------------------------- #

# Temporary definition, will be post-processed later.
rsa_test_data = [

    # Inspired from http://en.wikipedia.org/wiki/RSA#A_worked_example
    dict(
        n = 3233,
        p = 61,
        q = 53,
        e = 17,
        d = 2753,
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
    # Generated with the help of:
    #   http://critto.liceofoscarini.it/critto/rsa/rsa_demo.phtml
    dict(
        n = 31243,
        p = 157,
        q = 199,
        e = 5,
        d = 18533,
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
    # Generated by http://people.eku.edu/styere/Encrypt/RSAdemo.html
    # Hmpf, that page doesn't allow the user to choose `e' ...
    dict(
        e = 17,
        n = 77028186510125710835232907121,
        p = 459983137786273,
        q = 167458717901777,
        d = 45310697947132401996104246513,
        _ = [
            dict(
                plain = 0,
                cipher = 0,
            ),
            dict(
                plain = 2,
                cipher = 2**17,
            ),
            dict(
                plain = 57128184570925880835232907122,
                cipher = 6764407817379484644525719120,
            ),
        ],
    ),
    # Again generated by http://people.eku.edu/styere/Encrypt/RSAdemo.html
    dict(
        e = 19,
        n = s2i("""
            81921567314082977661194180175378694208028080487095042140
            99597921367850945315474143925943532423516957495472126238
            57652061972441899562100158646230426553421319267911017057
            92539724815773563824224453532477 """),
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
    # Again generated by http://people.eku.edu/styere/Encrypt/RSAdemo.html
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
        n = s2i("""
            27268805042304371190222132181572894447082219120902043851
            66795736060840276639896794190982468195689042207559165472
            71706667469909857267760739464438990358218229685457571717
            21061506696834359042554106478101987848286656679197173685
            14018333672765349975846516765319522575282480595708379610
            65211461298935757922835206921034565558318160810507009875
            19116036670176563942174778239541106498897980410343853445
            82672779 """),
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
    # Generated by http://islab.oregonstate.edu/koc/ece575/02Project/Mor/
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
        n = s2i("""
            70971115736117038726645550808214912052317223150289444865
            68850452716884464912432452157422271636962314705740044261
            09383333023987136931631791015636064727390811662234936898
            62980829299505605287443573845147749776913677674203657688
            18809998100337646576854750161941304168537597552264512727
            1366940074964421597648545841 """),
        d = s2i("""
            63351870184876835585431387724817307426653355312934254433
            98757481676594836161596022553903775439617937319209185623
            43814069463941935041290726073178588924673147237234343289
            30934984753958699188098524755853400102146423188123417706
            69378009436948246256883151445897872307080823304524583421
            292732722435687824755422997 """),
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

    # With help of http://islab.oregonstate.edu/koc/ece575/02Project/Mor/
    # Also check some corner cases.
    dict(
        p = 2**2281 - 1,
        q = 2**2203 - 1,
        n = s2i("""
658416274830184544125027519921443515789888264156074733099244040126213682497
714032798116399288176502462829255784525977722903018714434309698108208388664
768262754316426220651576623731617882923164117579624827261244506084274371250
277849351631679441171018418018498039996472549893150577189302871520311715179
730714312181456245097848491669795997289830612988058523968384808822828370900
198489249243399165125219244753790779764466236965135793576516193213175061401
667388622228362042717054014679032953441034021506856017081062617572351195418
505899388715709795992029559042119783423597324707100694064675909238717573058
764118893225111602703838080618565401139902143069901117174204252871948846864
436771808616432457102844534843857198735242005309073939051433790946726672234
643259349535186268571629077937597838801337973092285608744209951533199868228
040004432132597073390363357892379997655878857696334892216345070227646749851
381208554044940444182864026513709449823489593439017366358869648168238735087
593808344484365136284219725233811605331815007424582890821887260682886632543
613109252862114326372077785369292570900594814481097443781269562647303671428
895764224084402259605109600363098950091998891375812839523613295667253813978
434879172781217285652895469194181218343078754501694746598738215243769747956
572555989594598180639098344891175879455994652382137038240166358066403475457
"""),
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
"""),
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

def unravel_rsa_test_data(data):
    unravelled_test_data = []
    for data_clump in [ x.copy() for x in data ]:
        data_clump.setdefault('encrypter_type', RSA.BasicEncrypter)
        try:
            plain_encrypted_couples_list = data_clump['_']
        except KeyError:
            # There's only one datum in the clump.  Register it.
            unravelled_test_data.append(data_clump)
        else:
            # Unravel the data contained in the clump, and register each of
            # them singularly.
            del data_clump['_']
            for d in plain_encrypted_couples_list:
                unravelled_test_data.append(
                    dict(data_clump, plain=d['plain'], cipher=d['cipher']))
    return unravelled_test_data

def extract_rsa_keys_data(data):
    munged_data = []
    for datum in data:
        munged_data.append(dict([(k, v) for k, v in datum.iteritems()
                                        if k in 'npqed']))
    return munged_data

rsa_keys_data = extract_rsa_keys_data(rsa_test_data)
rsa_test_data = unravel_rsa_test_data(rsa_test_data)

# -------------------- #
#  Go with the tests.  #
# -------------------- #

@with_params(rsa_keys_data)
def test_build_key(n, p, q, e, d):
    key = RSA.PrivateKey(p, q, e)
    assert key.n == n and key.d == d

@with_params(rsa_test_data)
def test_encrypt_pubkey(n, p, q, e, d, plain, cipher, encrypter_type):
    encrypter = encrypter_type(RSA.PublicKey(n, e))
    assert encrypter.encrypt(plain) == cipher

@with_params(rsa_test_data)
def test_encrypt_privkey(n, p, q, e, d, plain, cipher, encrypter_type):
    encrypter = encrypter_type(RSA.PrivateKey(p, q, e))
    assert encrypter.encrypt(plain) == cipher

@with_params(rsa_test_data)
def test_decrypt(n, p, q, e, d, plain, cipher, encrypter_type):
    encrypter = encrypter_type(RSA.PrivateKey(p, q, e))
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
    encrypter = RSA.BasicEncrypter(RSA.PrivateKey(p, q, e))
    encrypter.decrypt((p - 10) * (q - 23) / 2)

# vim: et sw=4 ts=4 ft=python
