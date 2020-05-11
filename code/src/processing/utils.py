from string import punctuation
from unicodedata import normalize


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def normalizar(txt, sort=True):
    if txt:
        txt = remover_acentos(txt.lower())
        for punkt in punctuation:
            txt = txt.replace(punkt, " ")
        txt = txt.split()
        if sort:
            txt = sorted(txt)
        txt = "".join(txt).strip()
    return txt