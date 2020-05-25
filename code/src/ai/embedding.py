import os
import sys
import time
import pickle
from itertools import chain
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor

from nltk.corpus import machado, mac_morpho, floresta
from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from ..processing.utils import CleanUp


def carregar_sentencas(filename):
    sentences = []
    with open(filename, "rb") as fh:
        sentences = pickle.load(fh)
        sentences = [normalizar.fit(sent) for sent in sentences]
    return sentences


def carregar_nltk_datasets(dataset):
    from nltk.corpus import machado, mac_morpho, floresta

    corpus, fileid = dataset
    if corpus == "machado":
        corpus = machado
    elif corpus == "mac_morpho":
        corpus = mac_morpho
    elif corpus == "floresta":
        corpus = floresta
    return [normalizar.fit(" ".join(sent)) for sent in corpus.sents(fileid)]


if __name__ == "__main__":

    start = time.time()
    print("Carregando sentenças...")

    normalizar = CleanUp(return_tokens=True)

    sentences = []

    datasets = [["machado", fileid] for fileid in machado.fileids()]
    datasets += [["mac_morpho", fileid] for fileid in mac_morpho.fileids()]
    datasets += [["floresta", fileid] for fileid in floresta.fileids()]

    filenames = [
        f"{os.getcwd()}/data/wikipedia.pkl",
        f"{os.getcwd()}/data/fapesp.pkl",
        f"{os.getcwd()}/data/mundo.pkl",
        f"{os.getcwd()}/data/bulas.pkl",
    ]

    # Carregar arquivos com frases em formato pickle
    with ProcessPoolExecutor(max_workers=4) as executor:
        sentences += list(chain(*list(executor.map(carregar_sentencas, filenames))))

    # Carregar frases da NLTK
    with ProcessPoolExecutor(max_workers=cpu_count() * 2) as executor:
        sentences += list(
            chain(*list(executor.map(carregar_nltk_datasets, datasets, chunksize=5)))
        )

    print(f"Qtde sentenças: {len(sentences)}")
    print(f"Carregar sentenças demorou: {round(time.time() - start, 2)}")

    start = time.time()
    print("Iniciando treinamento do Word2Vec...")
    w2v = Word2Vec(
        sentences=sentences,
        size=300,
        window=15,
        min_count=1,
        workers=cpu_count() * 2,
        sg=1,
        iter=30,
    )
    w2v.save(f"{os.getcwd()}/src/ai/models/w2v.model")
    print(f"Treinamento Word2Vec demorou: {round(time.time() - start, 2)}")

    start = time.time()
    print("Iniciando treinamento do Doc2Vec...")
    d2v = Doc2Vec(
        documents=[
            TaggedDocument(sentence, [k]) for k, sentence in enumerate(sentences)
        ],
        vector_size=300,
        window=15,
        min_count=1,
        workers=cpu_count() * 2,
        dm=1,
        hs=0,
        epochs=30,
    )
    d2v.save(f"{os.getcwd()}/src/ai/models/d2v.model")
    print(f"Treinamento Doc2Vec demorou: {round(time.time() - start, 2)}")
