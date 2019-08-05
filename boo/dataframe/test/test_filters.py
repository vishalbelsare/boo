from io import StringIO
import pandas as pd

from boo.dataframe.filter import large_companies, minimal_columns


def _read_dataframe():
    src = 'inn,title,org,okpo,okopf,okfs,okved,unit,ok1,ok2,ok3,region,of,of_lag,ta_fix,ta_fix_lag,cash,cash_lag,ta_nonfix,ta_nonfix_lag,ta,ta_lag,tp_capital,tp_capital_lag,debt_long,debt_long_lag,tp_long,tp_long_lag,debt_short,debt_short_lag,tp_short,tp_short_lag,tp,tp_lag,sales,sales_lag,profit_oper,profit_oper_lag,exp_interest,exp_interest_lag,profit_before_tax,profit_before_tax_lag,profit_after_tax,profit_after_tax_lag,cf_oper_in,cf_oper_in_sales,cf_oper_out,paid_to_supplier,paid_to_worker,paid_interest,paid_profit_tax,paid_other_costs,cf_oper,cf_inv_in,cf_inv_out,paid_fa_investment,cf_inv,cf_fin_in,cf_fin_out,cf_fin,cf\n9723031303,КИРБИ,ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,16179225,65,16,45.31,384,45,31,0,97,0,0,0,0,0,0,1190596,0,1190596,0,30,0,0,0,0,0,0,0,1190566,0,1190596,0,1190566,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n5808004284,БЕКОВСКИЙ САХАРНЫЙ ЗАВОД,ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,88042176,12300,16,10.81,384,10,81,0,58,838114,974114,850451,1339464,112,1018,615767,2115066,1466219,3454530,1609,78759,674865,765472,1437600,3299526,13861,9353,27010,76245,1466219,3454530,258074,2973297,-27716,115924,23864,34772,4811,52861,2466,35449,2294362,2276899,2532805,2300476,49916,0,182413,0,-238443,368795,19396,0,349399,8361,120223,-111862,-906\n5256083213,АВТОКОМПОНЕНТЫ - ГРУППА ГАЗ,ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,88605449,12300,16,45.31.1,384,45,31,1,52,1605,1816,937605,17404,60288,76670,3031561,4065688,3969166,4083092,683166,354657,0,0,15735,50887,1675,230365,3270265,3677548,3969166,4083092,20005657,17298393,524309,289159,17110,39215,397456,445147,328509,353518,18245194,18061910,18271154,17865407,193038,21000,130945,60764,-25960,1217077,982770,331,234307,0,224800,-224800,-16453\n5050115503,МАЙ,ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,45678395,12300,16,82.92,384,82,92,0,50,1491045,2098817,1564484,2311733,21677,508642,630147,1538359,2194631,3850092,1055556,1430621,0,0,0,3423,0,0,1139075,2416048,2194631,3850092,3214040,2912029,1177304,1146590,116603,184009,855226,752861,674935,597651,5400857,5215986,5875113,2983446,751825,0,240438,1899404,-474256,467181,17020,0,450161,0,462870,-462870,-486965\n2983009240,ВАРАНДЕЙСКИЙ ТЕРМИНАЛ,ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,72357966,12300,16,52.10.21,384,52,10,21,29,15507533,17011233,16380791,17874644,0,0,2269210,19221763,18650001,37096407,15251256,33804444,0,0,2307856,2336906,0,0,1090889,955057,18650001,37096407,18417236,20413127,12997125,14852461,0,0,14301852,15876212,11446812,14772656,19048438,17880058,6566912,2777866,489765,0,2724465,574816,12481526,36104888,18618668,73726,17486220,0,29961000,-29961000,6746\n2723134850,"Инвестиционно строительная компания ""Реал Строй""",Общество с ограниченной ответственностью,67917848,12300,16,64.92,384,64,92,0,27,692178,256901,692178,256901,6277,58851,1215450,1213551,1907628,1470452,113123,99061,0,0,0,0,0,0,1794505,1371391,1907628,1470452,133372,147943,-1502,-91960,8,0,17619,85676,14063,68541,517769,506690,665373,472456,1803,0,6207,179755,-147604,0,0,0,0,0,0,0,-147604\n7713725683,ТОРГОВЫЙ ДОМ СВЯЗЬ ИНЖИНИРИНГ,ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,90687584,65,16,33.20,384,33,20,0,77,1549,2888,1549,2888,230,195,4879339,2876786,4880888,2879674,434474,172435,0,0,2,2,0,0,4446412,2707237,4880888,2879674,2882993,1449191,288482,208633,0,97190,327861,293963,262039,232421,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n7728694325,СРЕДНЕ-ВОЛЖСКАЯ СУДОХОДНАЯ КОМПАНИЯ,ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,60480897,65,16,61.20,384,61,20,0,77,2112941,1565059,2112941,1565059,5333,74709,149938,253104,2262879,1818163,11208,6463,2131406,1600321,2131406,1600321,0,0,120265,211379,2262879,1818163,1065493,727980,79615,181378,110811,131501,5931,3521,4745,2817,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n4211014419,"УЧАСТОК ""КОКСОВЫЙ""",ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,10901721,65,16,05.10.12,384,5,10,12,42,415818,440585,5037869,2924037,125798,4284,1255698,842944,6293567,3766981,5720260,3184182,0,0,122120,118767,0,0,451187,464032,6293567,3766981,5889154,2653418,2995290,791632,0,0,3205469,981561,2536078,772664,5752870,5750124,3632803,2295045,460126,0,668465,209167,2120067,925500,2924053,53905,-1998553,0,0,0,121514\n7805056048,ПАТРИОТ-ДЕВЕЛОПМЕНТ СЕВЕРО-ЗАПАД,ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ,79749925,12300,16,45.20,384,45,20,0,78,0,206,13626,4978,263,349,1455220,1769657,1468846,1774634,-57294,-20614,0,0,0,48216,14675,13530,1526140,1747032,1468846,1774634,88126,116843,-62835,-21008,1145,825,-45573,-13088,-36680,-10922,986663,37455,1030520,155671,67144,0,0,807705,-43857,56384,12613,0,43771,0,0,0,-86\n'
    return pd.read_csv(StringIO(src)).set_index("inn")


def test_large_companies_and_less_columns():
    df = _read_dataframe() 
    x = minimal_columns(large_companies(df))
    assert x.head(3).to_dict() == {        
        'cf': {
            2983009240: 0.0,
            4211014419: 0.1,
            5256083213: -0.0},
        'of': {
            2983009240: 15.5,
            4211014419: 0.4,
            5256083213: 0.0},
        'ok1': {
            2983009240: 52,
            4211014419: 5,
            5256083213: 45},
        'ok2': {
            2983009240: 10,
            4211014419: 10,
            5256083213: 31},
        'p': {
            2983009240: 14.3,
            4211014419: 3.2,
            5256083213: 0.4},
        'region': {
            2983009240: 29,
            4211014419: 42,
            5256083213: 52},
        'sales': {
            2983009240: 18.4,
            4211014419: 5.9,
            5256083213: 20.0},
        'ta': {
            2983009240: 18.7,
            4211014419: 6.3,
            5256083213: 4.0},
        'title': {
            2983009240: 'ВАРАНДЕЙСКИЙ ТЕРМИНАЛ',
            4211014419: 'УЧАСТОК "КОКСОВЫЙ"',
            5256083213: 'АВТОКОМПОНЕНТЫ - ГРУППА ГАЗ'}}
