from saka import query_basabali, latin_to_aksara_bali, aksara_bali_to_latin, get_stopwords

def test_query_basabali_offline():
    # Test common word in offline dict
    res = query_basabali("rahajeng", use_online=False)
    assert res['status'] == 'found'
    assert 'selamat' in res['definitions'][0]['arti'].lower()

def test_query_basabali_online():
    # Test online query (requires internet)
    res = query_basabali("rahajeng", use_online=True)
    assert res['status'] == 'found'
    assert len(res['definitions']) > 0

def test_transliteration_accuracy():
    # Basic Balinese script test
    latin = "hanacaraka"
    aksara = latin_to_aksara_bali(latin)
    # Check if starts with Ha (ᬳ)
    assert aksara.startswith("ᬳ")
    assert aksara_bali_to_latin(aksara) == "hanacaraka"

def test_transliteration_complex():
    # Test numbers and punctuation
    latin = "bali 2026."
    aksara = latin_to_aksara_bali(latin)
    assert "᭒᭐᭒᭖" in aksara # 2026
    assert aksara.endswith("᭟") # Period
    assert aksara_bali_to_latin(aksara) == "bali 2026."

def test_bali_stopwords():
    stops = get_stopwords(lang='bali')
    assert "tiang" in stops
    assert "ngajeng" in stops
    assert len(stops) > 10
