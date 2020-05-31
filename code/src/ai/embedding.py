import os
import sys
import time
import pickle
from itertools import chain
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
from nltk.corpus import machado, mac_morpho, floresta
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from ..processing.utils import CleanUp


class LoadCorpus(object):
    """An interator that yields sentences (lists of str)."""

    def __init__(self, filename):
        self.normalizar = CleanUp(return_tokens=True)
        self.file_it = pd.read_csv(
            filename, header=None, iterator=True, names=["sentence"], chunksize=30000,
        )

    def __iter__(self):
        for lines in self.file_it:
            for line in lines["sentence"].tolist():
                yield self.normalizar.fit(line)


if __name__ == "__main__":
    start = time.time()
    print("-" * 20)
    print("Iniciando treinamento do Word2Vec...")
    w2v = Word2Vec(
        # sentences=LoadCorpus(f"{os.getcwd()}/data/embedding/corpus.txt"),
        corpus_file=f"{os.getcwd()}/data/embedding/corpus.txt",
        size=300,
        window=30,
        min_count=5,
        workers=cpu_count() * 2,
        sg=1,
        hs=0,
        negative=5,
        iter=20,
    )
    w2v.save(f"{os.getcwd()}/src/ai/models/w2v.model")
    print(f"Treinamento Word2Vec demorou: {round(time.time() - start, 2)}")
    print()

    start = time.time()
    print("-" * 20)
    print("Iniciando treinamento do Doc2Vec...")
    d2v = Doc2Vec(
        # documents=[
        #     TaggedDocument(sentence, [k])
        #     for k, sentence in enumerate(
        #         LoadCorpus(f"{os.getcwd()}/data/embedding/corpus.txt")
        #     )
        # ],
        corpus_file=f"{os.getcwd()}/data/embedding/corpus.txt",
        vector_size=300,
        window=30,
        min_count=5,
        workers=cpu_count() * 2,
        dm=1,
        hs=0,
        negative=5,
        dbow_words=1,
        epochs=20,
    )
    d2v.save(f"{os.getcwd()}/src/ai/models/d2v.model")
    print(f"Treinamento Doc2Vec demorou: {round(time.time() - start, 2)}")
