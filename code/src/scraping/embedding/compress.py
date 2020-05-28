import os
import time
import pickle

from ...processing.utils import CleanUp


def carregar_sentencas(filename):
    with open(filename, "rb") as fh:
        sentences = pickle.load(fh)
        for sent in sentences:
            yield normalizar.fit(sent)


if __name__ == "__main__":

    start = time.time()
    print("Carregando sentenças...")

    normalizar = CleanUp(return_tokens=True)

    filenames = [
        f"{os.getcwd()}/data/embedding/wikipedia.pkl",
        f"{os.getcwd()}/data/embedding/fapesp.pkl",
        f"{os.getcwd()}/data/embedding/mundo.pkl",
        f"{os.getcwd()}/data/embedding/uol.pkl",
        f"{os.getcwd()}/data/embedding/g1.pkl",
        f"{os.getcwd()}/data/embedding/bulas.pkl",
    ]

    with open(f"{os.getcwd()}/data/embedding/corpus.txt", "w") as fh:
        for filename in filenames:
            for sentence in carregar_sentencas(filename):
                fh.write(f"{' '.join(sentence)}\n")
