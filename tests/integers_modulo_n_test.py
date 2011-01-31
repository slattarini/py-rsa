#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# This file is part of RSA.py testsuite.

"""Tests for the RSA.py's implementation of integers (mod n)"""
import pytest
import RSA
import functools
from tests.pyrsa_testlib import with_params, without_duplicates, \
                                integers_mod, pytest_generate_tests


###  HELPER FUNCTIONS/DECORATORS

def check_integermod_operation(func):
    def wrapper(**kwargs):
        cls, expect, result = func(**kwargs)
        assert result.__class__ == cls
        assert result.residue == expect
    return functools.update_wrapper(wrapper, func)


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

        dict(modulo=(2**4253 - 1, 2**4423 - 1), base=(2**3217 - 1)**2,
             exponent=(2**3217 - 1), result=int("""\
9201626360013000862251661327288095471625440210132448575385407871725081708672056446469816604982479362746233907\
4323472087137031131218236584074390140125916288877232516302313026311879292768581672749706835069936659795426087\
5916347030079212856040958909159430739374164195585502229853764057035754893994667476937858356652424840330775414\
7938575673260682308408839121929235125141791421726314756065687081029213684939524365729659335986434207629821370\
9723320662067581115188855148288535783811878842583302216012998561552377195352483334308266093043129101802698794\
6443968811689402759150377156799360054829376076741160554770741447596330776501670591474758372237584627581558712\
3900005186646594977484922357368537956066802134600542563480124501476321595923851579425431245489492143094011810\
0201176064355517656064529240614831478866300694464606059323884349084920396863158044001971819705135671983082074\
6798485914853837666005959291627324148800212329052725683932692539125590925960699244492360947945878531816506817\
3216806615249775307223768097257851069942092394811632617120179011990790228006831875202550270030763313448660449\
6779051085943966320226323059810922683689032713263119653257460339355530268022756427022947085330078070167604353\
1350023646146467652774212586981497045826427595709499538217948408721762012230643773897790459336061599717994039\
2791629094059525586545266033104287031280215833888247218428668734499347745802203589299857646241671939806300295\
5171775724353961758533978979224236149436441195677700765878407950234475297188544968246309501734012024515149494\
5328523644890678183991248296573593811208443949711988110991455733989800647649451119637993681509919187293781589\
6502166738464946019220777937113920515613942650099360183410249492389258102193272712644043416376087418538536864\
1857219226541211138590292133222106860986508366000763344231667927392004713759737125649526392719013300389593316\
1660410154964398575300279738476606178208931246032391092639999452986469611620863735449265452103628644260530440\
4315740332742575458018879031489739593719203845919232780550060864930204601891618556843670421878961887357519587\
6989277530244817271450105413245508213522389507572831135317949140272512787144376664559714718900814540633612272\
3843548499648545955125931002259998532603896197472332334837639970130421944920874481053560987263448105869949302\
7324660171715113753176510806036979019717122656227340699200743272318958919034003669388458714062453144049236827\
6458167187798837367507787843119208203198822200626399131620754283289641585529845187294565354101993992748959700\
77457728452846543265995171265694777248886799366247490459615494860057024303598074949576916822108360247415""")),

    dict(modulo=(2**4253 - 1, 2**4423 - 1), base=2**3217 - 1,
         exponent=2**3217 - 1, result=int("""\
4908689080548841901693395612191735878865056957709977419731082874437183020626370247887766103893573902978511120\
6265131919336727675170676292903311857328818678695706879028323104854399112348367818679817801434538104892301608\
4083250954813485570569453625235418264891024033750915774842391661548191126404060267839397078461297061423613125\
9350631027506873376608063425007909961951468563347315197652631006167369089519428827798663477013794858524071478\
1172782796292854506678400948244254597486195754632600929256103490185063885291848999090680311932370875631938900\
8993203627561811285263252097902184916636098099438204868168923330291047224775632115359336142734853278512220775\
0583042325379504027961216636763567655306673029876711888032226425769541296555137855650839521162503591795369141\
9371206229411269346565266575706911246678835543856374190805962103239057544311798123481999765917937984185402319\
6581457494626230899325499916037870114503675203862903947746608592263991953738657626796849638280412010510919275\
2136322102471097216874711375576084972860685587780198113561120880543531683708348096826283123789998998915192737\
7473438549752890287270742533359950628663391917473304448423575982272961589331042528624120919995823173561141502\
1055219202814023687907685140484819397829737952887940803509050449373317730929526208084308806416864475367771773\
9509687397318391387581573003203066088775111269866336894853577168275126802213800089474011854304488502476406105\
1964717237367222818552425071653425981711345676070288336931200581246924190131259712299993861763970104705297293\
7317789795282565691089237258587112185784074636590694920589607538750536135612506201215801475727559984593106091\
0615674973522701671114808469639910957779080417441381962597382976242587121772005983929297858886435845559079941\
1423256377695963446070591156987488449398955316127057066624349423695886043115820659874882980595597210247929553\
1493015178091837625492554844761102776261848719485614818255607578294877695276527261861390427719345632101260665\
0899478117127565731505011657356618768188713078235483227492323570732030166694740919187496785215365206076132597\
5179286027743432307038626282030214963542709037750830168027124145211729663948139601656256309257622768402029403\
2682208678698407892103905951917627498354682215111198875444419175833317107315471554672533309297098606006705322\
3057098390046606053292401237594263690354954161113395733576084539708044930691021489050634013512840113750044718\
8388494592989231561407003229985285829090085934577415386795689076043330481749069100717959840255840022198806485\
88534675600973754449709851781450564585064982082349264853433443487550116583408111162320694488836559994683""")),

        dict(modulo=(2**4253 - 1, 2**4423 - 1), base=(2**3217 - 1)**2,
             exponent=(2**3217 - 1)**2, result=int("""\
3072322041786795275384469545192014650087907192660370555737838432129711211980626162446797847177765108237162226\
4014435089351964150353662196209717142352095608025412465692817485796858134421722233781133370478296827993756391\
4906353211377389745399543566165465161396377915825007124386222157740536040900024340580028037513417439164102387\
7318084252349409711339470106529130181542407088789762477543957009236856244053121561192005701178041944815337988\
7405623936834141083339239100031023113884137382482353276023321186276341728753500876147810380296301329263993716\
9082115561599623009415800867239916997345160232510242833048361761759059670295681007925579934445483453231313454\
1694230444077755695861100822195311827476792797994536194153409264982328047855776810632087186905683111799908069\
7549383711077944566797135775902598049264304991589440188220909222670571501682813696928406722110167755122690994\
8278512679301297704002528701723483021310976745469025567864119009528942185811744356645912003037149494815566891\
0720010042411502831771923645250088689819232459220908556981415319103751474713403776588999222809515093530291885\
3985804583585917911501552329367270536051452750428933035520091601154232558113419072020497997600233448380375934\
2767402248864761006046544061314914008829508752581851462557171218292124868811826665438257316917298275304888291\
0310547360405372177517669044976055413257570606409101035013797082051354892197083704869368118834221531700002706\
0658969951396446304117141412243049172178514192105115611757576741363811182657707274395583876751085445570171849\
7622473539526915130189147557826512458876051031773343517764296406306307461936686270952685202035772162460586657\
4131637703438740175612467404369415479088568666428312607224464080702082067897267749831793487766705111755650164\
0718308416314669216667531986970745810783585307280409569952730913561353893189661667284234957180775592680153661\
9826753725279505224268851453931399995640539917825090324091405005069987769420672177825358824591833202343281047\
3430843905072225524168438599143498194629910309929513814576243538940019853018454018484051806501031034148755045\
7240656081087066485354611698515045463837154177997512639979028018685088388897457691273242739347068527332743405\
5908184888031328914540203036083052614835970910349742820128262118253930092822021352549249435438712040269277510\
7832896291684167661572844394381076646948894864256419968453534775732906283921125874168913149258558458530339982\
5500687092974045181483145073996681592033712546144946255747196534018541107151195062757889931525031309708350951\
948850171984507206591197821107573977480130071615837658256293439784481379153752927793706425514174670192381""")),

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


@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(addition_data)
def test_integermod_add(modulo, addend1, addend2, result, factory):
    cls = factory(modulo)
    return cls, result, cls(addend1) + cls(addend2)

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(addition_data)
def test_integermod_ladd(modulo, addend1, addend2, result, factory):
    cls = factory(modulo)
    return cls, result, cls(addend1) + addend2

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(addition_data)
def test_integermod_radd(modulo, addend1, addend2, result, factory):
    cls = factory(modulo)
    return cls, result, addend1 + cls(addend2)


@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_sub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    return cls, result, cls(minuend) - cls(subtrahend)

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_lsub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    return cls, result, cls(minuend) - subtrahend

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(subtraction_data)
def test_integermod_rsub(modulo, minuend, subtrahend, result, factory):
    cls = factory(modulo)
    return cls, result, minuend - cls(subtrahend)


@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_mul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    return cls, result, cls(factor2) * cls(factor1)

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_lmul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    return cls, result, cls(factor1) * factor2

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(multiplication_data)
def test_integermod_rmul(modulo, factor1, factor2, result, factory):
    cls = factory(modulo)
    return cls, result, factor1 * cls(factor2)


@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_div(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    return cls, result, cls(dividend) / cls(divisor)

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_ldiv(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    return cls, result, cls(dividend) / divisor

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(division_data)
def test_integermod_rdiv(modulo, dividend, divisor, result, factory):
    cls = factory(modulo)
    return cls, result, dividend / cls(divisor)


@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(additive_inversion_data)
def test_integermod_inverse(modulo, residue, inverse, factory):
    cls = factory(modulo)
    return cls, inverse, - cls(residue)


@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_pow(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    return cls, reciprocal, cls(residue)**(-1)

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_rdiv(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    return cls, reciprocal, cls(1) / residue

@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(multiplicative_inversion_data)
def test_integermod_reciprocal_ldiv(modulo, residue, reciprocal, factory):
    cls = factory(modulo)
    return cls, reciprocal, 1 / cls(residue)

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


@check_integermod_operation
@with_params([integers_mod], 'factory')
@with_params(exponentiation_data)
def test_integermod_exponentiation(modulo, base, exponent, result, factory):
    cls = factory(modulo)
    return cls, result, cls(base) ** exponent


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
