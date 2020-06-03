import os
import time
import pickle

import numpy as np
import pandas as pd

from ...processing.utils import CleanUp


def carregar_sentencas(filename):
    sentences = pd.read_pickle(filename)
    for sent in sentences:
        frase = normalizar.fit(sent)
        if len(frase) > 15:
            yield frase


if __name__ == "__main__":

    start = time.time()

    print("Carregando sentenças...")

    normalizar = CleanUp(return_tokens=True)

    filenames = [
        f"{os.getcwd()}/data/embedding/uol.pkl",
        f"{os.getcwd()}/data/embedding/g1.pkl",
        f"{os.getcwd()}/data/embedding/frases.pkl",
        f"{os.getcwd()}/data/embedding/livros.pkl",
        f"{os.getcwd()}/data/embedding/wikipedia.pkl",
        f"{os.getcwd()}/data/embedding/fapesp.pkl",
        f"{os.getcwd()}/data/embedding/mundo.pkl",
        f"{os.getcwd()}/data/embedding/bulas.pkl",
    ]

    with open(f"{os.getcwd()}/data/embedding/corpus.txt", "ab") as fh:
        for filename in filenames:
            for sentence in carregar_sentencas(filename):
                np.savetxt(fh, [f"{' '.join(sentence)}"], fmt="%s")

    print(f"Tempo total da compressao: {round(time.time() - start, 2)}s")
