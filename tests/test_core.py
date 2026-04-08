import pytest
from saka import tokenize, normalize, analyze

def test_tokenize():
    text = "Belajar sambil beramal di era konektivitas."
    tokens = tokenize(text)
    assert tokens == ['Belajar', 'sambil', 'beramal', 'di', 'era', 'konektivitas']

def test_normalize():
    text = "klo gimana gw hr ini"
    normalized = normalize(text)
    assert "kalau bagaimana saya hari ini" in normalized

def test_analyze():
    analysis = analyze("mempertanggungjawabkan")
    assert analysis['root'] == 'tanggung jawab'
    assert 'mem' in analysis['prefixes']
    assert 'per' in analysis['prefixes']
    assert 'kan' in analysis['suffixes']
