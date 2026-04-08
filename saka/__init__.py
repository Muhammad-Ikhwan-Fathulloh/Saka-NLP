from .core.tokenizer import tokenize, async_tokenize
from .core.normalizer import normalize, async_normalize
from .core.analyzer import analyze, async_analyze
from .dict.stopwords import get_stopwords
from .plugins.kbbi_scraper import query_kbbi
from .plugins.sunda.sundadigi_scraper import query_sundadigi

__all__ = [
    "tokenize",
    "async_tokenize",
    "normalize",
    "async_normalize",
    "analyze",
    "async_analyze",
    "get_stopwords",
    "query_kbbi",
    "query_sundadigi",
]
