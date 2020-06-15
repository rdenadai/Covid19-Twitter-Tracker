import os
import sys
import time
import random
import warnings
from multiprocessing import cpu_count
from itertools import chain

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import joblib
import ray

from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

from ..data.processing.utils import CleanUp, SNOWBALL_STEMMER, RSLP_STEMMER


warnings.filterwarnings("ignore")


if __name__ == "__main__":
    clean_up = CleanUp(stemmer=SNOWBALL_STEMMER)

    # print(clean_up.fit("meu deus eu to com falta de ar??????"))
    # sys.exit()

    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv(f"{os.getcwd()}/data/processed/dataset.csv", sep="|")
    df["x"] = df["comentario"].apply(lambda comment: clean_up.fit(str(comment)))
    df["y"] = df["classificacao"].apply(lambda clasf: 0 if clasf == "negativo" else 1)
    textos = df[["x", "y"]].to_numpy()
    corpus = [item for item in list(textos[:, 0])]

    X = textos[:, 0]
    y = textos[:, 1].astype(np.int).ravel()

    # Split the dataset with fixed state to validate
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    print("Starting grid search...")
    # Build a pipeline
    parameters = {
        "tfidf__ngram_range": [(1, 1), (2, 2), (3, 3), (1, 2), (1, 3), (1, 4), (1, 5)],
        "tfidf__lowercase": [False],
        "svm__kernel": ["linear", "rbf"],
        "svm__C": [1, 5, 7, 15],
        "svm__random_state": [0, 10, 100, 1000],
        "svm__shrinking": [True, False],
    }
    pipe = Pipeline(steps=[("tfidf", TfidfVectorizer()), ("svm", SVC())])
    pipe = GridSearchCV(pipe, parameters, n_jobs=-1)

    # Fit the dataset to pipeline
    pipe.fit(X_train, y_train)
    print("Best parameter (CV score=%0.3f):" % pipe.best_score_)
    print(pipe.best_params_)

    # Best params for each step of pipeline
    tfidf_params = pipe.best_estimator_.named_steps["tfidf"].get_params()
    svm_params = pipe.best_estimator_.named_steps["svm"].get_params()

    # After run GridSearchCV
    print("Validating TF-IDF + SVM")
    pipe = make_pipeline(TfidfVectorizer(**tfidf_params), SVC(**svm_params))

    # Verify cross validation ... above 0.75 is good enough
    scores = cross_val_score(pipe, X_train, y_train, cv=5)
    print(
        "Cross Validation accuracy: %0.2f (+/- %0.2f)"
        % (scores.mean(), scores.std() * 2)
    )
    print(scores)
    print("-" * 20)

    # Predict the test data and show others metrics
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    print("Classification Report")
    print("-" * 20)
    print(classification_report(y_test, pred))
    print("Confusion Matrix")
    print("-" * 20)
    print(confusion_matrix(pred, y_test))

    # Rebuild the classifier, build a new pipeline (equal as above), fit and save the model
    print(f"Saving model in: {os.getcwd()}/models/tweets_classifier.model")
    pipe = make_pipeline(TfidfVectorizer(**tfidf_params), SVC(**svm_params))
    pipe.fit(X, y)
    joblib.dump(pipe, f"{os.getcwd()}/models/tweets_classifier.model")
