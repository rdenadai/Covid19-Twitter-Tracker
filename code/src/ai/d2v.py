import os
import sys
import time
import pickle
from multiprocessing import cpu_count

from nltk.corpus import machado, mac_morpho, floresta
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from ..processing.utils import CleanUp


if __name__ == "__main__":

    start = time.time()
    print("Carregando sentenças...")

    normalizar = CleanUp(return_tokens=True)

    sentences = []
    with open(f"{os.getcwd()}/data/wikipedia.pkl", "rb") as fh:
        sentences = pickle.load(fh)[:10]
        sentences = [
            TaggedDocument(normalizar.fit(sent), [i])
            for i, sent in enumerate(sentences)
        ]

    k = len(sentences)
    with open(f"{os.getcwd()}/data/fapesp.pkl", "rb") as fh:
        sentences = pickle.load(fh)
        sentences = [
            TaggedDocument(normalizar.fit(sent), [k + i])
            for i, sent in enumerate(sentences)
        ]

    k = len(sentences)
    objs = [machado, mac_morpho, floresta]
    for obj in objs:
        for fileid in obj.fileids():
            sentences += [
                TaggedDocument(normalizar.fit(" ".join(sent)), [k + i])
                for i, sent in enumerate(obj.sents(fileid))
            ]

    print(f"Qtde sentenças: {len(sentences)}")
    print(f"Carregar sentenças demorou: {round(time.time() - start, 2)}")

    start = time.time()
    print("Iniciando treinamento do Doc2Vec...")
    model = Doc2Vec(
        documents=sentences,
        vector_size=300,
        window=5,
        min_count=1,
        workers=cpu_count() * 2,
        dm=1,
        hs=0,
        epochs=20,
    )
    model.save(f"{os.getcwd()}/src/ai/models/d2v.model")
    print(f"Treinamento Doc2Vec demorou: {round(time.time() - start, 2)}")
