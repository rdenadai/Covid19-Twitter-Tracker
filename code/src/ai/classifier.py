import os
import sys
import time
import random
import warnings
from multiprocessing import cpu_count
from itertools import chain

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import joblib
import ray

from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import SVC

from ..processing.utils import CleanUp, SNOWBALL_STEMMER, RSLP_STEMMER


if __name__ == "__main__":
    clean_up = CleanUp(stemmer=SNOWBALL_STEMMER)

    # print(clean_up.fit("meu deus eu to com falta de ar??????"))
    # sys.exit()

    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv(f"{os.getcwd()}/data/dataset.csv", sep="|")
    df["x"] = df["comentario"].apply(lambda comment: clean_up.fit(str(comment)))
    df["y"] = df["classificacao"].apply(lambda clasf: 0 if clasf == "negativo" else 1)
    textos = df[["x", "y"]].to_numpy()
    corpus = [item for item in list(textos[:, 0])]

    X = textos[:, 0]
    y = textos[:, 1].astype(np.int).ravel()

    print("Running best TF-IDF ngram value...")
    # Check to see which variation of TF-IDF is good enough for SVM
    validacoes, N = [], 6
    for ngram_range in zip(np.ones((N), dtype=np.int), range(1, N)):
        acc, f1 = [], []
        tfidf = TfidfVectorizer(ngram_range=ngram_range, lowercase=False).fit(corpus)
        for _ in range(5):
            clf = SVC(kernel="linear", C=5, random_state=0)
            pipe = make_pipeline(tfidf, clf)

            Xc = textos[:, 0]
            yc = textos[:, 1].astype(np.int).ravel()

            X_train, X_test, y_train, y_test = train_test_split(Xc, yc, test_size=0.2)

            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)

            acc.append(round(accuracy_score(pred, y_test) * 100, 2))
            f1.append(round(f1_score(pred, y_test) * 100, 2))

        validacoes.append(
            (
                ngram_range,
                round(np.mean(acc), 2),
                np.max(acc),
                round(np.mean(f1), 2),
                np.max(f1),
            )
        )

    # Choose the best variation which has the highest F1 score
    columns = ["NGram", "Accuracy", "Acc Max.", "F1", "F1 Max."]
    df = pd.DataFrame(validacoes, columns=columns)
    df = df.sort_values(by=["F1 Max.", "Acc Max.", "NGram"], ascending=False)
    ngram_range = df.reset_index().loc[0]["NGram"]

    # Print the choosen ngram and start a TF-IDF
    print(f"Choosen ngram: {ngram_range}")
    tfidf = TfidfVectorizer(ngram_range=ngram_range, lowercase=False).fit(corpus)

    # Create SVM classifier
    clf = SVC(kernel="linear", C=5, random_state=0)

    # Build a pipeline
    pipe = make_pipeline(tfidf, clf)

    # Split the dataset with fixed state to validate
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    # Fit the dataset to pipeline
    pipe.fit(X_train, y_train)

    print("Validating TF-IDF + Linear SVM")
    # Verify cross validation ... above 0.75 is good enough
    scores = cross_val_score(pipe, X_train, y_train, cv=5)
    print(
        "Cross Validation accuracy: %0.2f (+/- %0.2f)"
        % (scores.mean(), scores.std() * 2)
    )
    print(scores)
    print("-" * 20)

    # Predict the test data and show others metrics
    pred = pipe.predict(X_test)
    print("Classification Report")
    print("-" * 20)
    print(classification_report(y_test, pred))
    print("Confusion Matrix")
    print("-" * 20)
    print(confusion_matrix(pred, y_test))

    # Rebuild the classifier, build a new pipeline (equal as above), fit and save the model
    print(f"Saving model in: {os.getcwd()}/src/ai/models/tweets_classifier.model")
    clf = SVC(kernel="linear", C=5, random_state=0)
    pipe = make_pipeline(tfidf, clf)
    pipe.fit(X, y)
    joblib.dump(pipe, f"{os.getcwd()}/src/ai/models/tweets_classifier.model")
