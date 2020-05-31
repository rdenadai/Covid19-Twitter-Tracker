import os
import pickle
from itertools import chain


if __name__ == "__main__":
    sentences = []
    with open(f"{os.getcwd()}/data/livros/livros.txt", "r") as fh:
        for line in fh.readlines():
            for phrase in line.strip().split("."):
                if len(phrase) > 15:
                    sentences += [phrase.strip()]
    sentences = list(set(filter(None, sentences)))
    with open(f"{os.getcwd()}/data/embedding/livros.pkl", "wb") as fh:
        pickle.dump(sentences, fh)
