import pytest
import pandas as pd
import numpy as np


from boo.dataframe.canonic import (
    canonic_df,
    canonic_dtypes,
    rename_rows,
    UnclassifiableCodeError,
    split_okved,
    fst,
)


STRINGS = ["title", "org", "okpo", "okopf", "okfs", "okved", "inn", "unit"]


def test_canonic_dtypes_on_inn():
    assert canonic_dtypes()["inn"] == str


def test_canonic_dtypes_on_strings():
    for s in STRINGS:
        assert canonic_dtypes()[s] == str


def test_canonic_dtypes_on_numeric():
    for k, v in canonic_dtypes().items():
        if k not in STRINGS:
            assert v == np.int64


def test_fst():
    assert fst("123") == 12
    assert fst(1) == 0


df1 = pd.DataFrame(
    {
        "cash": {227693: 5118911, 1134038: 176492735},
        "cash_lag": {227693: 4415161, 1134038: 97254253},
        "cf": {227693: 731457, 1134038: 79238482},
        "cf_fin": {227693: -8381375, 1134038: 0},
        "cf_fin_in": {227693: 45710000, 1134038: 0},
        "cf_fin_out": {227693: 54091375, 1134038: 0},
        "cf_inv": {227693: -9562988, 1134038: 94133337},
        "cf_inv_in": {227693: 462649, 1134038: 227215065},
        "cf_inv_out": {227693: 10025637, 1134038: 133081728},
        "cf_oper": {227693: 18675820, 1134038: -14894855},
        "cf_oper_in": {227693: 141458070, 1134038: 126623931},
        "cf_oper_in_sales": {227693: 139059783, 1134038: 76596031},
        "cf_oper_out": {227693: 122782250, 1134038: 141518786},
        "date_published": {227693: "20180522", 1134038: "20180420"},
        "debt_long": {227693: 48710000, 1134038: 0},
        "debt_long_lag": {227693: 24110000, 1134038: 0},
        "debt_short": {227693: 135225, 1134038: 0},
        "debt_short_lag": {227693: 32225249, 1134038: 0},
        "exp_interest": {227693: 4772743, 1134038: 0},
        "exp_interest_lag": {227693: 4578533, 1134038: 0},
        "inn": {227693: "2607018122", 1134038: "7702038150"},
        "name": {
            227693: 'ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "ВТОРАЯ ГЕНЕРИРУЮЩАЯ КОМПАНИЯ ОПТОВОГО РЫНКА ЭЛЕКТРОЭНЕРГИИ"',
            1134038: 'ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ ГОРОДА МОСКВЫ "МОСКОВСКИЙ ОРДЕНА ЛЕНИНА И ОРДЕНА ТРУДОВОГО КРАСНОГО ЗНАМЕНИ МЕТРОПОЛИТЕН ИМЕНИ В.И.ЛЕНИНА"',
        },
        "of": {227693: 157893868, 1134038: 1177451866},
        "of_lag": {227693: 159580634, 1134038: 1176481475},
        "okfs": {227693: "16", 1134038: "13"},
        "okopf": {227693: "12247", 1134038: "65242"},
        "okpo": {227693: "76851389", 1134038: "03324364"},
        "okved": {227693: "35.11.1", 1134038: "49.31.24"},
        "paid_fa_investment": {227693: 8151560, 1134038: 75846216},
        "paid_interest": {227693: 4263663, 1134038: 0},
        "paid_other_costs": {227693: 10533749, 1134038: 49285848},
        "paid_profit_tax": {227693: 1194945, 1134038: 1334091},
        "paid_to_supplier": {227693: 101635288, 1134038: 36403948},
        "paid_to_worker": {227693: 5154605, 1134038: 54494899},
        "profit_after_tax": {227693: 6653155, 1134038: -2941167},
        "profit_after_tax_lag": {227693: 3496694, 1134038: 478499},
        "profit_before_tax": {227693: 9565794, 1134038: -1264096},
        "profit_before_tax_lag": {227693: 5568938, 1134038: 1499730},
        "profit_oper": {227693: 18777329, 1134038: -3824454},
        "profit_oper_lag": {227693: 14148372, 1134038: -2933568},
        "report_type": {227693: "2", 1134038: "2"},
        "sales": {227693: 139613447, 1134038: 108266266},
        "sales_lag": {227693: 134284652, 1134038: 93793008},
        "ta": {227693: 199987631, 1134038: 1976579092},
        "ta_fix": {227693: 168086888, 1134038: 1790840290},
        "ta_fix_lag": {227693: 170327660, 1134038: 1646655499},
        "ta_lag": {227693: 201623040, 1134038: 1752602357},
        "ta_nonfix": {227693: 31900743, 1134038: 185738802},
        "ta_nonfix_lag": {227693: 31295380, 1134038: 105946858},
        "tp": {227693: 199987631, 1134038: 1976579092},
        "tp_capital": {227693: 120149020, 1134038: 1321233565},
        "tp_capital_lag": {227693: 114235134, 1134038: 1316041991},
        "tp_lag": {227693: 201623040, 1134038: 1752602357},
        "tp_long": {227693: 60118904, 1134038: 816784},
        "tp_long_lag": {227693: 38310705, 1134038: 753699},
        "tp_short": {227693: 19719707, 1134038: 654528743},
        "tp_short_lag": {227693: 49077201, 1134038: 435806667},
        "unit": {227693: "384", 1134038: "384"},
    },
    index=None,
)


def test_rename_complete():
    assert canonic_df(df1).title["7702038150"] == "Московский метрополитен"


def test_substitute_complete():
    assert canonic_df(df1).title["2607018122"] == "ВТОРАЯ ОГК"


def test_rename_rows():
    df2 = pd.DataFrame(
        {
            "title": {
                1134038: "МОСКОВСКИЙ ОРДЕНА ЛЕНИНА И ОРДЕНА ТРУДОВОГО КРАСНОГО ЗНАМЕНИ МЕТРОПОЛИТЕН ИМЕНИ В.И.ЛЕНИНА"
            },
            "inn": {1134038: "7702038150"},
        }
    ).set_index("inn")
    assert rename_rows(df2).loc["7702038150", "title"] == "Московский метрополитен"


def test_okved3():
    with pytest.raises(UnclassifiableCodeError):
        split_okved("1.2.3...")


if __name__ == "__main__":
    pytest.main()
