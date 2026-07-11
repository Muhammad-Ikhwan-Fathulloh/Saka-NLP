import pytest
from saka import get_stopwords

def test_english_stopwords():
    stops = get_stopwords("en")
    assert "i" in stops
    assert "you" in stops
    assert "however" in stops
    assert "although" in stops
    assert len(stops) > 100
