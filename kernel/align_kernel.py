"""
use custom gram matrix instead of linear kernel for sentiment classification

"""

import numpy as np
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from sklearn import metrics


def intersection_kernel(X, X_ref):
    """
    X and X_ref are a list of list of words.

    Return G,
    G_ij is the intersection of vocabulary between X_i and X_ref_j
    """

    len_i = len(X)
    len_j = len(X_ref)

    G = np.zeros((len_i, len_j))

    for i in range(len_i):
        for j in range(len_j):
            vocab_i = set(X[i])
            vocab_j = set(X_ref[j])

            G[i, j] = len(vocab_i.intersection(vocab_j))

    return G


def load_dataset(data_file):
    """load X and y from the data file
    """
    X = []
    y = []

    with open(data_file) as f:
        for line in f:
            li = line.split()
            y.append(int(li[0]))
            X.append(li[1:])

    return X, np.array(y)


if __name__ == "__main__":

    X, y = load_dataset("ntcir.en")

    clf = SVC(kernel='precomputed')
    G = intersection_kernel(X, X)
    clf.fit(G, y)

    X_test, y_test = load_dataset("ntcir.ch")
    X_translate, _ = load_dataset("ntcir_en_transformed.txt")

    G_predict = intersection_kernel(X_test, X_translate)
    y_predict = clf.predict(G_predict)

    print metrics.confusion_matrix(y_test, y_predict)
    print metrics.classification_report(y_test, y_predict)
