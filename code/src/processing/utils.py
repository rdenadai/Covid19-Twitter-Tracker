import re
from unicodedata import normalize
from string import punctuation
from functools import lru_cache

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spacy.lang.pt import Portuguese
import emoji


def divide_chunks(lista, n):
    # looping till length l
    for i in range(0, len(lista), n):
        yield lista[i : i + n]


@lru_cache(maxsize=256)
def is_number(s):
    try:
        complex(s)  # for int, long, float and complex
    except ValueError:
        return False
    return True


@lru_cache(maxsize=256)
def get_stopwords():
    stpwords = stopwords.words("portuguese")
    rms = ["um", "não", "mais", "muito"]
    for rm in rms:
        del stpwords[stpwords.index(rm)]
    return stpwords, punctuation


def tokenizer(phrase, clean=False):
    if not clean:
        phrase = clean_up(phrase, False)
    clean_frase = []
    clfa = clean_frase.append
    for palavra in phrase:
        palavra = "".join([word.lemma_ for word in NLP(palavra)])
        # clfa(STEMMER.stem(palavra))
        clfa(palavra)
    return " ".join(clean_frase).strip()


def clean_up(phrase, join=True):
    STOPWORDS, PUNCT = get_stopwords()
    # Transforma as hashtags em palavras
    try:
        for group in re.findall(r"#\S+\b", phrase, re.DOTALL):
            g2 = re.sub(r"([A-Z])", r" \1", group, flags=re.MULTILINE)
            phrase = re.sub(r"{}\b".format(group), g2, phrase, flags=re.MULTILINE)
    except Exception:
        pass
    # lowercase para fazer outros pre-processamentos
    phrase = phrase.lower()
    # Remoção de emojis
    phrase = emoji.get_emoji_regexp().sub(r"", phrase)
    for stw in STOPWORDS:
        phrase = re.sub(r"\b{}\b".format(stw), "", phrase, flags=re.MULTILINE)
    for punct in PUNCT:
        phrase = phrase.replace(punct, " ")
    for o, r in RM:
        phrase = re.sub(o, r, phrase, flags=re.MULTILINE)

    # Limpeza extra
    phrase = word_tokenize(phrase)
    clean_frase = []
    clfa = clean_frase.append
    for palavra in phrase:
        if not is_number(palavra) and len(palavra) > 2:
            clfa(palavra)
    clean_frase = " ".join(clean_frase) if join else clean_frase
    return clean_frase.strip()


def remover_acentos(txt):
    return normalize("NFKD", txt).encode("ASCII", "ignore").decode("ASCII")


def normalizar(phrase, sort=True):
    if phrase:
        phrase = remover_acentos(phrase.lower())
        for punkt in punctuation:
            phrase = phrase.replace(punkt, " ")
        phrase = phrase.split()
        if sort:
            phrase = sorted(phrase)
        phrase = "".join(phrase).strip()
    return phrase


# GLOBALS
NLP = Portuguese()
# STEMMER = nltk.stem.RSLPStemmer()
STEMMER = nltk.stem.SnowballStemmer("portuguese")
STOPWORDS, PUNCT = get_stopwords()
RM = [
    (r"(http[s]*?:\/\/)+.*[\r\n]*", r""),
    (r"@", r""),
    (r"\n+", r" . "),
    (r'"', r" "),
    (r"\'", r" "),
    (r"#", r""),
    (r"(RT)", r""),
    (r"[…]", " . "),
    (r"[0-9]*", r""),
    (r"“", r""),
    (r"”", ""),
    (r"([aeiouqwtyupdfghjklçzxcvbnm|!@$%&\.\[\]\(\)+-_=<>,;:])\1+", r"\1"),
    (r"(\bñ\n)", "não"),
    (r"(nã)", "não"),
    (r"\s+", r" "),
    (r"(nãoo)", "não"),
]
