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

def alignment_kernel():
    pass

if __name__ == "__main__":

    X = []
    y = []

    with open("ntcir.en") as f:
        for line in f:
            li = line.split()
            y.append(int(li[0]))
            X.append(li[1:])

    y = np.array(y)
    kf = StratifiedKFold(y, k=5, indices=True)

    clf = SVC(kernel='precomputed')
    for train_index, test_index in kf:
        X_train = []
        for i in train_index:
            X_train.append(X[i])
        X_test = []
        for i in test_index:
            X_test.append(X[i])

        y_train, y_test = y[train_index], y[test_index]

        G = intersection_kernel(X_train, X_train)
        clf.fit(G, y_train)

        G_predict = intersection_kernel(X_test, X_train)
        y_predict = clf.predict(G_predict)

        print metrics.confusion_matrix(y_test, y_predict)
        print metrics.classification_report(y_test, y_predict)
