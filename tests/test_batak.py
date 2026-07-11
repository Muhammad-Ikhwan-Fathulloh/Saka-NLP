import pytest
from saka import analyze, get_stopwords
from saka.core.analyzer import _BATAK_DICT

def test_batak_dict_loading():
    assert len(_BATAK_DICT) > 100
    assert "horas" in _BATAK_DICT
    assert "holong" in _BATAK_DICT
    assert _BATAK_DICT["horas"]["arti"] is not None

def test_batak_morphology():
    # horas - base word
    r1 = analyze("horas")
    assert r1['root'] == 'horas'
    assert 'batak' in r1['regional_matches']

    # mangan - base word (makan)
    r2 = analyze("mangan")
    assert r2['root'] == 'mangan'
    assert 'batak' in r2['regional_matches']

    # mangalehon - exists as base word in Batak dictionary (memberi)
    r3 = analyze("mangalehon")
    assert 'batak' in r3['regional_matches']

    # holong - base word (cinta/kasih)
    r4 = analyze("holong")
    assert r4['root'] == 'holong'
    assert 'batak' in r4['regional_matches']

def test_batak_stopwords():
    stops = get_stopwords("batak")
    assert "do" in stops      # Toba predicate operator
    assert "nge" in stops     # Karo operator
    assert "ibas" in stops    # Karo preposition
    assert "da" in stops      # Mandailing affirmative
