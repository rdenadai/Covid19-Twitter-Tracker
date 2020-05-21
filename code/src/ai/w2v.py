import os
import sys
import time
import pickle
from multiprocessing import cpu_count

from nltk.corpus import machado, mac_morpho, floresta
from gensim.models import Word2Vec

from ..processing.utils import CleanUp


if __name__ == "__main__":

    start = time.time()
    print("Carregando sentenças...")

    normalizar = CleanUp(return_tokens=True)

    sentences = []
    with open(f"{os.getcwd()}/data/wikipedia.pkl", "rb") as fh:
        sentences = pickle.load(fh)
        sentences = [normalizar.fit(sent) for sent in sentences]

    with open(f"{os.getcwd()}/data/fapesp.pkl", "rb") as fh:
        sentences = pickle.load(fh)
        sentences = [normalizar.fit(sent) for sent in sentences]

    objs = [machado, mac_morpho, floresta]
    for obj in objs:
        for fileid in obj.fileids():
            sentences += [normalizar.fit(" ".join(sent)) for sent in obj.sents(fileid)]

    print(f"Qtde sentenças: {len(sentences)}")
    print(f"Carregar sentenças demorou: {round(time.time() - start, 2)}")

    start = time.time()
    print("Iniciando treinamento do Word2Vec...")
    model = Word2Vec(
        sentences=sentences,
        size=300,
        window=5,
        min_count=1,
        workers=cpu_count() * 2,
        sg=1,
        iter=20,
    )
    model.save(f"{os.getcwd()}/src/ai/models/w2v.model")
    print(f"Treinamento Word2Vec demorou: {round(time.time() - start, 2)}")
