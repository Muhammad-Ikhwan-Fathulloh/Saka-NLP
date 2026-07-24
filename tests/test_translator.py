import pytest
from saka import dict_translate

def test_dict_translate_sunda_basic():
    """Test basic Indonesian to Sunda translation using dict"""
    result = dict_translate("saya", "sunda")
    # 'saya' should map to a Sundanese word like 'abdi' or 'kuring'
    assert result != "saya", f"Expected translation but got original: {result}"

def test_dict_translate_unknown_word_preserved():
    """Words not in dict should stay unchanged"""
    result = dict_translate("laptop", "sunda")
    assert "laptop" in result

def test_dict_translate_invalid_lang_returns_original():
    """Target language not supported should return original"""
    text = "saya makan nasi"
    result = dict_translate(text, "mars")
    assert result == text

def test_dict_translate_punctuation_preserved():
    """Punctuation should not be lost"""
    result = dict_translate("halo!", "sunda")
    assert "!" in result

def test_dict_translate_supported_languages():
    """All supported languages should not error"""
    for lang in ['sunda', 'jawa', 'bali', 'minang', 'batak']:
        result = dict_translate("saya", lang)
        assert isinstance(result, str)
