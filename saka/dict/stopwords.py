import os
import json
from typing import Set
from functools import lru_cache

_SUNDA_STOPWORDS = {
    "teu", "na", "ka", "ti", "ku", "di", "nu", "anu", "oge", "wae", 
    "bae", "mah", "teh", "tea", "jeung", "sareng", "naon", "saha", 
    "mana", "kumaha", "iraha", "naha", "pikeun", "kanggo", "pisan", 
    "kacida", "pasti", "tangtu", "bisa", "tiasa", "aya", "euweuh", "kunaon", "ieu", "éta",
    "ari", "nya", "atuh", "apan", "sok", "geura", "tuh", "kieu", "kitu", "engke", 
    "ayeuna", "duka", "teuing", "pangna", "basa", "mun", "lamun", "saupama", "sanaos", 
    "najan", "kawas", "jiga", "lir", "da", "dong", "ge", "wé", "weh"
}

_JAWA_STOPWORDS = {
    "lan", "utawa", "ing", "kang", "sing", "seng", "iki", "iku", 
    "kuwi", "apa", "opo", "sapa", "sopo", "piye", "kepiye", 
    "pira", "piro", "kapan", "nyang", "karo", "kalebet", "menawa", 
    "menawi", "bisa", "iso", "uga", "ugi", "ora", "mboten", "wis", "wes", "dudu", 
    "kene", "kono", "kui", "kae", "saka", "saking", "dadi", "dados", "amarga", "amargi", 
    "nanging", "ananging", "supaya", "supados", "yen", "yèn", "bilih", "nuli", "lajeng", 
    "banjur", "kados", "kaya", "kajaba", "kejawi", "malah", "satemah", "senajan", 
    "sanadyan", "enggal", "ndang", "akeh", "akèh", "kathah"
}

_BALI_STOPWORDS = {
    "di", "ke", "teken", "apang", "saja", "ada", "ene", "ento", "i", "ni",
    "tiang", "iraga", "ia", "cai", "nyai", "nanging", "laut", "suba", "tusing",
    "ngajeng", "mandaer", "neda", "keto", "kena", "be", "ne", "mare",
    "ring", "saking", "antuk", "tur", "lan", "miwah", "yening", "yen", "pinaka", "buat", 
    "kanti", "sadurung", "sampun", "wau", "mangda", "ipun", "dane", "ida", "niki", "nika", 
    "puniki", "punika", "sane", "ane", "indik", "kadi", "buka"
}

# English stopwords
# Primary source: NLTK English stopword corpus (Bird et al., 2009) — 179 words
#   Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python.
#   O'Reilly Media. https://www.nltk.org/
# Extended with sklearn / scikit-learn stopwords (Pedregosa et al., 2011)
#   Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python.
#   JMLR 12, pp. 2825-2830. https://scikit-learn.org/
# Canonical list available at: https://gist.github.com/sebleier/554280
_EN_STOPWORDS = {
    # Personal pronouns
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    # Interrogative & relative pronouns
    "what", "which", "who", "whom", "whose",
    # Demonstratives
    "this", "that", "these", "those",
    # Copula & auxiliaries
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did", "doing",
    "will", "would", "shall", "should",
    "may", "might", "must", "can", "could",
    # Articles
    "a", "an", "the",
    # Coordinating & subordinating conjunctions
    "and", "but", "if", "or", "nor", "so", "yet",
    "because", "as", "since", "although", "though", "unless",
    "while", "until", "after", "before", "when", "whenever",
    "where", "wherever", "whether",
    # Prepositions
    "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below",
    "to", "from", "up", "down", "in", "out", "on", "off", "over",
    "under", "around", "along", "near", "across", "behind", "beside",
    "without", "within", "upon", "among", "throughout", "toward",
    # Adverbs
    "again", "further", "then", "once", "here", "there",
    "why", "how", "now", "also", "however", "therefore", "thus",
    "instead", "anyway", "already", "just", "still", "even",
    "very", "too", "quite", "rather", "enough", "almost",
    # Quantifiers & determiners
    "all", "any", "both", "each", "few", "more", "most",
    "other", "some", "such", "no", "not", "only", "own",
    "same", "than", "every", "many", "much", "several",
    # Common contractions / negation fragments
    "don", "doesn", "didn", "isn", "aren", "wasn", "weren",
    "haven", "hasn", "hadn", "won", "wouldn", "shouldn",
    "couldn", "cannot", "s", "t", "ll", "re", "ve", "d", "m",
    # Common function words
    "can", "will", "just", "should",
}

_JAKSEL_STOPWORDS = {
    "literally", "basically", "which", "which is", "whichis", "like", "tbh", "fyi", "jujurly", "at least", "so", 
    "as in", "btw", "anyway", "somehow", "even", "actually", "well", "cmiiw", "asap", "make sense", "worth it",
    "end of the day", "at the end of the day", "i mean", "you know", "in terms of", "let's say", "to be honest", 
    "not gonna lie", "ngl", "lowkey", "highkey", "for real", "fr", "periodt", "kinda", "sorta", "dunno", "lemme", 
    "gimme", "gonna", "wanna", "gotta", "obviously", "seriously", "prefer", "vibes", "relate", "cringe", "awkward"
}

_MINANG_STOPWORDS = {
    "nan", "jo", "dek", "di", "ko", "iko", "tu", "dari", "dan", "atau",
    "pado", "juo", "untuak", "ka", "dalam", "pulo", "lai", "lah",
    "adolah", "marupokan", "sabagai", "indak", "alah", "ado",
    "kini", "inyo", "nyo", "itu", "pun", "tapi", "namun",
    "karano", "basamo", "sarato", "sacaro", "sahinggo", "sainggo",
    "baitu", "mako", "supayo", "sadangkan", "tatapi", "walaupun",
    "ataupun", "maupun", "bahwa", "kalau", "dima", "katiko",
    "akan", "bisa", "harus", "masih", "bagi", "sarajo",
    "surang", "sajo", "hanyo", "biaso", "biasonyo", "umumnyo",
    "sangaik", "bana", "labiah", "paliang", "alun", "mangko"
}

_BATAK_STOPWORDS = {
    # ==========================================================================
    # BATAK TOBA function words
    # Source: Nababan, P.W.J. (1981). A grammar of Toba-Batak (D-37).
    #   Pacific Linguistics, Australian National University.
    #   DOI: 10.15144/PL-D37
    # Specifically: §4.4 Functors (pronouns, prepositions, modal particles,
    #   connectives, auxiliaries) and §4.2.3 predicative particles.
    # --------------------------------------------------------------------------
    # Prepositions (§4.4.2.1)
    "di",        # locative: at, in, on
    "tu",        # to, toward
    "sian",      # from
    "ni",        # possessive / agentive marker
    "na",        # attributive preposition; also relative pronoun
    "dohot",     # with; and (comitative)
    "marhite",   # by means of; through
    "so",        # as far as; like (comparative)
    "songon",    # like, as (comparative)
    "gabe",      # for; as (resultative); become
    # Pronouns (§4.4.1.1)
    "au",        # I
    "ho",        # thou/you (singular informal)
    "ibana",     # he/she/it (3rd sg)
    "hami",      # we (exclusive)
    "hita",      # we (inclusive)
    "hamu",      # you (plural / honorific sg)
    "nasida",    # they
    "iba",       # one (indefinite); sometimes self-referential
    # Demonstratives (§4.4.1.1)
    "on",        # this (close to speaker)
    "i",         # that (close to hearer); also used as the definite marker
    "an",        # that yonder
    # Predicative particles (§4.4.3.1)
    "do",        # affirmative particle (marks predicate)
    "ma",        # narrative/imperative particle
    "pe",        # concessive particle ("even if", "just")
    "dang",      # negation: not
    "nunga",     # completive: already
    "so",        # negative in subordinate clauses; also emphatic negation
    "npe",       # not … anymore (dang + be)
    # Connectives (§4.4.4)
    "jala",      # and
    "alai",      # but
    "hape",      # but (stronger, expressing surprise)
    "manang",    # or
    "duhi",      # and then; narrative connector
    # Subordinating conjunctions (§4.4.2.2)
    "molo",      # if; when (general)
    "anggo",     # if (conditional); as for
    "nang",      # although
    "agia",      # even if (stronger than nang)
    "ala",       # because; for
    "ai",        # for; because (clausal)
    "asa",       # so that; in order that
    "disi",      # as soon as
    "tikki",     # while; at the time
    "dung",      # after
    "unang",     # don't (negative imperative)
    "sanga",     # before (it's too late)
    # Auxiliaries / modal particles (§4.4.5)
    "holan",     # only
    "sor",       # almost
    "naeng",     # want to; going to
    "be",        # distributive ("each")
    "muse",      # again
    "hian",      # used to; previously
    "tar",       # somewhat (degree); pretend to (modal)
    "saik",      # always
    "pala",      # really; truly
    "nasa",      # all
    "akka",      # plural marker
    "ganup",     # each; every
    # Additional high-frequency function words
    "ima",       # that is (identificational)
    "nunga",     # already (perfective)
    "laos",      # immediately; right away
    "tongtong",  # always
    "sude",      # all
    "jolma",     # person (generic, often part of relative clauses)

    # ==========================================================================
    # BATAK KARO function words
    # Source: Woollams, G. (1996). A grammar of Karo Batak, Sumatra (C-130).
    #   Pacific Linguistics, Australian National University.
    #   DOI: 10.15144/PL-C130
    # Specifically: §4.2 Prepositions, §7.4 Operators/Particles,
    #   §8.4 Conjunctions, and §3.2 Word class descriptions.
    # --------------------------------------------------------------------------
    # Prepositions (§4.2)
    "i",         # at; in; on (locative)
    "ku",        # to (directional)
    "ibas",      # in; inside; within (locative/temporal)
    "sian",      # from
    "ras",       # with; together with (comitative)
    "erkite",    # because of; due to (causal)
    "sabap",     # because; reason
    "asum",      # when (temporal)
    "bagi",      # like; as (comparative)
    # Personal pronouns (§4.4.1.1)
    "aku",       # I
    "kam",       # you (2nd sg)
    "ia",        # he/she/it
    "kita",      # we (inclusive)
    "kami",      # we (exclusive)
    "kalak",     # people; person (generic, frequent in clauses)
    "ndu",       # you (clitic, bound)
    # Particles / operators (§7.4)
    "nge",       # operator: completive / assertive
    "me",        # operator: identifies or emphasizes subject
    "pe",        # additive ("too", "also", "even")
    "kang",      # question particle; softener
    "dage",      # so; therefore (sentence connective)
    "ngenca",    # only; just (restrictive)
    "lenga",     # not yet
    "la",        # not (negation)
    "min",       # particle: softener / encouragement
    "si",        # relative marker; also used before names
    "adi",       # if; when (conditional subordinator)
    "maka",      # so; then (result/narrative connector)
    "janah",     # and; then (additive)
    "tapi",      # but (adversative)
    "banci",     # can; may (modal)
    "emaka",     # therefore; so (causal connector)
    "lebe",      # first; before
    "entah",     # perhaps; or (disjunction)

    # ==========================================================================
    # BATAK MANDAILING / ANGKOLA function words
    # Source: Nababan (1981) ibid. — covers Angkola-Mandailing as closely
    #   related to Toba; also van der Tuuk (1864/1867). Tobasche Spraakkunst.
    #   Amsterdam: Muller. (Historical primary grammar)
    # Mandailing shares the majority of Toba function words; distinct items:
    # --------------------------------------------------------------------------
    "da",        # affirmative / emphatic particle (Mandailing variant of 'do')
    "naso",      # not; negative (variant)
    "aso",       # so that (variant of 'asa')
}

# Cache Indonesian stopwords loaded from file
_ID_STOPWORDS_CACHED: Set[str] = set()
def _load_id_stopwords() -> Set[str]:
    global _ID_STOPWORDS_CACHED
    if not _ID_STOPWORDS_CACHED:
        current_dir = os.path.dirname(__file__)
        txt_path = os.path.join(current_dir, 'stopwords.txt')
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        _ID_STOPWORDS_CACHED.add(word)
        except FileNotFoundError:
            print(f"Warning: Stopwords file not found at {txt_path}.")
    return _ID_STOPWORDS_CACHED

@lru_cache(maxsize=10)
def get_stopwords(lang: str = "all") -> Set[str]:
    """
    Returns a set of stopwords.

    Supported ``lang`` values:
      - ``'id'``     — Indonesian (Tala Dataset, ~460 words)
      - ``'sunda'``  — Sundanese
      - ``'jawa'``   — Javanese
      - ``'bali'``   — Balinese
      - ``'minang'`` — Minangkabau
      - ``'batak'``  — Batak (Toba, Karo, Mandailing dialects)
      - ``'en'``     — English
      - ``'jaksel'`` — South Jakarta bilingual slang
      - ``'all'``    — Combined (default, 1 000+ words)
    """
    stopwords = set()
    
    if lang in ['id', 'all']:
        stopwords.update(_load_id_stopwords())
            
    if lang in ['sunda', 'all']:
        stopwords.update(_SUNDA_STOPWORDS)
        
    if lang in ['jawa', 'all']:
        stopwords.update(_JAWA_STOPWORDS)
        
    if lang in ['bali', 'all']:
        stopwords.update(_BALI_STOPWORDS)

    if lang in ['minang', 'all']:
        stopwords.update(_MINANG_STOPWORDS)

    if lang in ['batak', 'all']:
        stopwords.update(_BATAK_STOPWORDS)
        
    if lang in ['en', 'all']:
        stopwords.update(_EN_STOPWORDS)
        
    if lang in ['jaksel', 'all']:
        stopwords.update(_JAKSEL_STOPWORDS)
        
    return stopwords

def remove_stopwords(text: str, lang: str = "all", remove_punctuation: bool = False, extra_punctuation: str = "") -> str:
    """
    Menghapus stopwords dari teks.
    
    Args:
        text (str): Teks asal
        lang (str): Pilihan bahasa stopword ('id', 'sunda', 'jawa', 'bali', 'minang', 'batak', 'jaksel', 'en', atau 'all')
        remove_punctuation (bool): Jika True, akan membuang tanda baca dasar (.,!?;:()[]"' dsb)
        extra_punctuation (str): Karakter kustom tambahan yang ingin dibuang (misal "-_")
        
    Returns:
        str: Teks yang sudah bersih dari stopwords (dan tanda baca jika dipilih)
    """
    import string
    
    # 1. Bersihkan tanda baca jika diminta
    if remove_punctuation or extra_punctuation:
        chars_to_remove = extra_punctuation
        if remove_punctuation:
            chars_to_remove += string.punctuation
            
        if chars_to_remove:
            translation_table = str.maketrans(dict.fromkeys(chars_to_remove))
            text = text.translate(translation_table)
            
    # 2. Tokenisasi secara kasar basis spasi
    words = text.split()
    stops = get_stopwords(lang)
    
    # 3. Filter
    filtered_words = [w for w in words if w.lower() not in stops]
    
    return " ".join(filtered_words)

