import re
from unicodedata import normalize
from string import punctuation
from functools import lru_cache

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
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
    rms = ["um", "não", "mais", "muito", "sem", "estou", "sou"]
    for rm in rms:
        del stpwords[stpwords.index(rm)]
    return stpwords, punctuation


def remover_acentos(txt):
    return normalize("NFKD", txt).encode("ASCII", "ignore").decode("ASCII")


def tokenizer(phrase, clean=False):
    if not clean:
        phrase = CleanUp(return_tokens=True).fit(phrase)
    clean_frase = []
    clfa = clean_frase.append
    for palavra in phrase:
        palavra = "".join([word.lemma_ for word in NLP(palavra)])
        # clfa(STEMMER.stem(palavra))
        clfa(palavra)
    return " ".join(clean_frase).strip()


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


class CleanUp:
    def __init__(
        self,
        remove_stopwords=False,
        remove_emojis=True,
        stemmer=None,
        lemmatizer=None,
        return_tokens=False,
    ) -> None:
        self.remove_stopwords = remove_stopwords
        self.remove_emojis = remove_emojis
        self.stemmer = stemmer
        self.lemmatizer = lemmatizer
        self.return_tokens = return_tokens
        self.STOPWORDS, self.PUNCT = self.get_stopwords()
        self.RM = [
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

    def remover_acentos(self, phrase):
        return normalize("NFKD", phrase).encode("ASCII", "ignore").decode("ASCII")

    @lru_cache(maxsize=256)
    def is_number(self, word):
        try:
            complex(word)  # for int, long, float and complex
        except ValueError:
            return False
        return True

    @lru_cache(maxsize=256)
    def get_stopwords(self):
        stpwords = stopwords.words("portuguese")
        rms = ["um", "não", "mais", "muito", "sem", "estou", "sou"]
        for rm in rms:
            del stpwords[stpwords.index(rm)]
        return stpwords, punctuation

    def fit(self, phrase):
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
        if self.remove_emojis:
            phrase = emoji.get_emoji_regexp().sub(r"", phrase)
        if self.remove_stopwords:
            for stw in self.STOPWORDS:
                phrase = re.sub(r"\b{}\b".format(stw), "", phrase, flags=re.MULTILINE)
        # Remove pontuação
        for punct in self.PUNCT:
            phrase = phrase.replace(punct, " ")
        # Remove strings padrão existente, como urls
        for o, r in self.RM:
            phrase = re.sub(o, r, phrase, flags=re.MULTILINE)
        phrase = self.remover_acentos(phrase)

        # Limpeza extra
        phrase = word_tokenize(phrase)
        clean_frase = []
        clfa = clean_frase.append
        for palavra in phrase:
            if not self.is_number(palavra) and len(palavra) > 2:
                if self.lemmatizer:
                    palavra = "".join(
                        [word.lemma_ for word in self.lemmatizer(palavra)]
                    )
                if self.stemmer:
                    clfa(self.stemmer.stem(palavra))
                else:
                    clfa(palavra)
        clean_frase = (
            " ".join(clean_frase).strip() if not self.return_tokens else clean_frase
        )
        return clean_frase


# GLOBALS
NLP_LEMMATIZER = spacy.load("pt")
RSLP_STEMMER = nltk.stem.RSLPStemmer()
SNOWBALL_STEMMER = nltk.stem.SnowballStemmer("portuguese")
STOPWORDS, PUNCT = get_stopwords()
