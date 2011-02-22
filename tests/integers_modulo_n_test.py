#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for the RSA.py's implementation of integers (mod n)"""

import pytest
import RSA
from tests.lib import s2i, integers_mod, with_params, \
                      without_duplicates, pytest_generate_tests


###  HELPER FUNCTIONS/DECORATORS

def check_integermod_result(cls, expect, result):
    __tracebackhide__ = True
    assert result.__class__ == cls
    assert result.residue == expect


###  DATA

class DummyClass:
    pass

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
        # the following have been found with GAP
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

        # Check that our optimization in the calculation of exponentiation
        # when the modulo is product of two primes (based on the Chinese
        # Remainder Theorem) allows us to calculate powers which would
        # otherwise take too long.  To be precise, on the test machine,
        # these calculations take ~ 120 seconds with the optimization
        # enabled, and ~ 250 with the optimization disabled.
        # The expected results has been obtained with GAP.

        dict(
            modulo = (2**4253 - 1, 2**4423 - 1),
            base = (2**3217 - 1)**2,
            exponent = (2**3217 - 1),
            result = s2i("""
920162636001300086225166132728809547162544021013244857538540787172508170867
205644646981660498247936274623390743234720871370311312182365840743901401259
162888772325163023130263118792927685816727497068350699366597954260875916347
030079212856040958909159430739374164195585502229853764057035754893994667476
937858356652424840330775414793857567326068230840883912192923512514179142172
631475606568708102921368493952436572965933598643420762982137097233206620675
811151888551482885357838118788425833022160129985615523771953524833343082660
930431291018026987946443968811689402759150377156799360054829376076741160554
770741447596330776501670591474758372237584627581558712390000518664659497748
492235736853795606680213460054256348012450147632159592385157942543124548949
214309401181002011760643555176560645292406148314788663006944646060593238843
490849203968631580440019718197051356719830820746798485914853837666005959291
627324148800212329052725683932692539125590925960699244492360947945878531816
506817321680661524977530722376809725785106994209239481163261712017901199079
022800683187520255027003076331344866044967790510859439663202263230598109226
836890327132631196532574603393555302680227564270229470853300780701676043531
350023646146467652774212586981497045826427595709499538217948408721762012230
643773897790459336061599717994039279162909405952558654526603310428703128021
583388824721842866873449934774580220358929985764624167193980630029551717757
243539617585339789792242361494364411956777007658784079502344752971885449682
463095017340120245151494945328523644890678183991248296573593811208443949711
988110991455733989800647649451119637993681509919187293781589650216673846494
601922077793711392051561394265009936018341024949238925810219327271264404341
637608741853853686418572192265412111385902921332221068609865083660007633442
316679273920047137597371256495263927190133003895933161660410154964398575300
279738476606178208931246032391092639999452986469611620863735449265452103628
644260530440431574033274257545801887903148973959371920384591923278055006086
493020460189161855684367042187896188735751958769892775302448172714501054132
455082135223895075728311353179491402725127871443766645597147189008145406336
122723843548499648545955125931002259998532603896197472332334837639970130421
944920874481053560987263448105869949302732466017171511375317651080603697901
971712265622734069920074327231895891903400366938845871406245314404923682764
581671877988373675077878431192082031988222006263991316207542832896415855298
451872945653541019939927489597007745772845284654326599517126569477724888679
9366247490459615494860057024303598074949576916822108360247415""")),

    dict(
        modulo = (2**4253 - 1, 2**4423 - 1),
        base = 2**3217 - 1,
        exponent = 2**3217 - 1,
        result = s2i("""
490868908054884190169339561219173587886505695770997741973108287443718302062
637024788776610389357390297851112062651319193367276751706762929033118573288
186786957068790283231048543991123483678186798178014345381048923016084083250
954813485570569453625235418264891024033750915774842391661548191126404060267
839397078461297061423613125935063102750687337660806342500790996195146856334
731519765263100616736908951942882779866347701379485852407147811727827962928
545066784009482442545974861957546326009292561034901850638852918489990906803
119323708756319389008993203627561811285263252097902184916636098099438204868
168923330291047224775632115359336142734853278512220775058304232537950402796
121663676356765530667302987671188803222642576954129655513785565083952116250
359179536914193712062294112693465652665757069112466788355438563741908059621
032390575443117981234819997659179379841854023196581457494626230899325499916
037870114503675203862903947746608592263991953738657626796849638280412010510
919275213632210247109721687471137557608497286068558778019811356112088054353
168370834809682628312378999899891519273774734385497528902872707425333599506
286633919174733044484235759822729615893310425286241209199958231735611415021
055219202814023687907685140484819397829737952887940803509050449373317730929
526208084308806416864475367771773950968739731839138758157300320306608877511
126986633689485357716827512680221380008947401185430448850247640610519647172
373672228185524250716534259817113456760702883369312005812469241901312597122
999938617639701047052972937317789795282565691089237258587112185784074636590
694920589607538750536135612506201215801475727559984593106091061567497352270
167111480846963991095777908041744138196259738297624258712177200598392929785
888643584555907994114232563776959634460705911569874884493989553161270570666
243494236958860431158206598748829805955972102479295531493015178091837625492
554844761102776261848719485614818255607578294877695276527261861390427719345
632101260665089947811712756573150501165735661876818871307823548322749232357
073203016669474091918749678521536520607613259751792860277434323070386262820
302149635427090377508301680271241452117296639481396016562563092576227684020
294032682208678698407892103905951917627498354682215111198875444419175833317
107315471554672533309297098606006705322305709839004660605329240123759426369
035495416111339573357608453970804493069102148905063401351284011375004471883
884945929892315614070032299852858290900859345774153867956890760433304817490
691007179598402558400221988064858853467560097375444970985178145056458506498
2082349264853433443487550116583408111162320694488836559994683""")),

        dict(
            modulo = (2**4253 - 1, 2**4423 - 1),
            base = (2**3217 - 1)**2,
            exponent = (2**3217 - 1)**2,
            result = s2i("""
307232204178679527538446954519201465008790719266037055573783843212971121198
062616244679784717776510823716222640144350893519641503536621962097171423520
956080254124656928174857968581344217222337811333704782968279937563914906353
211377389745399543566165465161396377915825007124386222157740536040900024340
580028037513417439164102387731808425234940971133947010652913018154240708878
976247754395700923685624405312156119200570117804194481533798874056239368341
410833392391000310231138841373824823532760233211862763417287535008761478103
802963013292639937169082115561599623009415800867239916997345160232510242833
048361761759059670295681007925579934445483453231313454169423044407775569586
110082219531182747679279799453619415340926498232804785577681063208718690568
311179990806975493837110779445667971357759025980492643049915894401882209092
226705715016828136969284067221101677551226909948278512679301297704002528701
723483021310976745469025567864119009528942185811744356645912003037149494815
566891072001004241150283177192364525008868981923245922090855698141531910375
147471340377658899922280951509353029188539858045835859179115015523293672705
360514527504289330355200916011542325581134190720204979976002334483803759342
767402248864761006046544061314914008829508752581851462557171218292124868811
826665438257316917298275304888291031054736040537217751766904497605541325757
060640910103501379708205135489219708370486936811883422153170000270606589699
513964463041171414122430491721785141921051156117575767413638111826577072743
955838767510854455701718497622473539526915130189147557826512458876051031773
343517764296406306307461936686270952685202035772162460586657413163770343874
017561246740436941547908856866642831260722446408070208206789726774983179348
776670511175565016407183084163146692166675319869707458107835853072804095699
527309135613538931896616672842349571807755926801536619826753725279505224268
851453931399995640539917825090324091405005069987769420672177825358824591833
202343281047343084390507222552416843859914349819462991030992951381457624353
894001985301845401848405180650103103414875504572406560810870664853546116985
150454638371541779975126399790280186850883888974576912732427393470685273327
434055908184888031328914540203036083052614835970910349742820128262118253930
092822021352549249435438712040269277510783289629168416766157284439438107664
694889486425641996845353477573290628392112587416891314925855845853033998255
006870929740451814831450739966815920337125461449462557471965340185411071511
950627578899315250313097083509519488501719845072065911978211075739774801300
71615837658256293439784481379153752927793706425514174670192381""")),

    ]:
        # Given a^n, we want to try also (-a)^n, in two different
        # "flavors".
        d1, d2 = d.copy(), d.copy()
        d1['base'] = - d['base']
        modulo = d['modulo']
        if isinstance(modulo, (tuple, list)):
            modulo = reduce(lambda x, y : x*y, modulo)
        d2['base'] = modulo - d['base']
        if d['exponent'] % 2 == 1 and d['result'] != 0:
            d2['result'] = d1['result'] = modulo - d['result']
        data.extend([d, d1, d2])
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

def test_integermod_pq_init():
    class IntegerMod22(RSA.IntegerModPQ):
        p, q = 2, 11
    assert IntegerMod22(whole=25) == IntegerMod22(3)


@with_params([RSA.IntegerMod, RSA.IntegerModPQ], 'cls')
def test_integermod_direct_instantiation_exception(cls):
    pytest.raises(RSA.IMRuntimeError, cls, [1])

@with_params([RSA.IntegerMod, RSA.IntegerModPQ], 'cls')
def test_integermod_subclass_no_modulo_instantiation_exception(cls):
    # check that instantiation of an IntegerMod subclass fails if
    # `modulo' class attribute is not overridden
    class integermod_subclass(cls): pass
    pytest.raises(RSA.IMRuntimeError, "integermod_subclass(1)")

@with_params(['p', 'q'], 'attr')
def test_integermod_pq_subclass_incomplete_instantiation_exception(attr):
    # check that instantiation of an IntegerMod subclass fails if
    # `modulo' class attribute is not overridden
    class integermod_subclass(RSA.IntegerModPQ): pass
    setattr(integermod_subclass, attr, 5)
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
    check_integermod_result(cls, result, cls(addend1) + cls(addend2))

@with_params([integers_mod], 'factory')
@with_params(addition_data)
def test_integermod_ladd(modulo, addend1, addend2, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, cls(addend1) + addend2)

@with_params([integers_mod], 'factory')
@with_params(addition_data)
def test_integermod_radd(modulo, addend1, addend2, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, addend1 + cls(addend2))


@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_sub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, cls(minuend) - cls(subtrahend))

@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_lsub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, cls(minuend) - subtrahend)

@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_rsub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, minuend - cls(subtrahend))


@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_mul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, cls(factor2) * cls(factor1))

@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_lmul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, cls(factor1) * factor2)

@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_rmul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, factor1 * cls(factor2))


@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_div(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, cls(dividend) / cls(divisor))

@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_ldiv(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, cls(dividend) / divisor)

@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_rdiv(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, dividend / cls(divisor))


@with_params([integers_mod], 'factory')
@with_params(additive_inversion_data)
def test_integermod_inverse(modulo, residue, inverse, factory):
    cls = factory(modulo)
    check_integermod_result(cls, inverse, - cls(residue))


@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_pow(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    check_integermod_result(cls, reciprocal, cls(residue)**(-1))

@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_rdiv(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    check_integermod_result(cls, reciprocal, cls(1) / residue)

@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_ldiv(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    check_integermod_result(cls, reciprocal, 1 / cls(residue))

@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_func(modulo, residue, reciprocal):
    assert RSA.modular_reciprocal(residue, modulo) == reciprocal

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

@with_params(noncoprime_modulo_and_residue_data)
def test_integermod_invalid_reciprocal_func(modulo, residue):
    pytest.raises(RSA.IMValueError, RSA.modular_reciprocal,
                  residue, modulo)


@with_params([integers_mod], 'factory')
@with_params(exponentiation_data)
def test_integermod_exponentiation(modulo, base, exponent, result, factory):
    cls = factory(modulo)
    check_integermod_result(cls, result, cls(base)**exponent)


@with_params([1.0, '1', [1], (1,), {1:1}, DummyClass(), object()], 'other')
@with_params(['+', '-', '*', '/', '**'], 'operation')
@with_params([integers_mod], 'factory')
@with_params([2, 100, (5, 11), (97, 73)], 'modulo')
def test_integermod_invalid_operation(other, operation, modulo, factory):
    cls = factory(modulo)
    pytest.raises(RSA.IMTypeError, "cls(0) %s other" % operation)
    if operation != '**':
        pytest.raises(RSA.IMTypeError, "other %s cls(0)" % operation)

@with_params([dict(b=3, e=2), dict(b=(3, 5), e=8)])
@with_params([integers_mod], 'factory')
def test_integermodpq_invalid_exponentation(factory, b, e):
    int_mod_b = factory(b)
    int_mod_e = factory(e)
    pytest.raises(RSA.IMTypeError, "int_mod_b(1) ** int_mod_b(1)")
    pytest.raises(RSA.IMTypeError, "int_mod_b(1) ** int_mod_e(1)")


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
