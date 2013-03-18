import numpy as np
from scipy import linalg
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from sklearn import metrics
from sklearn.datasets import load_svmlight_file
from sklearn.utils.extmath import safe_sparse_dot


def test_precomputed():
    clf = SVC(kernel="precomputed")
    X, y = load_svmlight_file("/Users/mxf/paper_codes/clmm/ntcir/ntcir.ch.vec")
    kf = StratifiedKFold(y, k=5, indices=True)
    for train_index, test_index in kf:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        K_train = safe_sparse_dot(X_train, X_train.T, dense_output=True)
        K_test = safe_sparse_dot(X_test, X_train.T, dense_output=True)
        n = K_train.shape[0]
        M = np.identity(n)
        K_train, K_test = deform(0.1, K_train, M, K_test)

        clf.fit(K_train, y_train)
        y_predicted = clf.predict(K_test)
        print metrics.classification_report(y_test, y_predicted)
        print metrics.confusion_matrix(y_test, y_predicted)


def deform(r, K, M, K_test=None):
    """K: the gram matrix of a kernel over labeled+unlabeled data (nxn matrix)
    M: a graph regularizer (nxn  matrix)
    K_test: the gram matrix of a kernel between training and test points
    (optional) size m x n for m test points.
    r: deformation ratio (gamma_I/gamma_A)
    Outputs:
    Ktilde: the gram matrix of the semi-supervised deformed kernel
    over labeled+unlabeled data
    K_test_tilde: the gram matrix of the semi-supervised deformed kernel
    between training and test points"""
    n = K.shape[1]
    I = np.identity(n)
    Ktilde = np.dot(linalg.inv(I + r * np.dot(K,  M)), K)
    if (K_test != None):
        K_test_tilde = K_test - r * np.dot(K_test, np.dot(M, Ktilde))

    if (K_test != None):
        return Ktilde, K_test_tilde
    else:
        return Ktilde


def test():
    magic = np.array([
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]])
    I = np.identity(3)
    print deform(1, magic, magic, I)

if __name__ == "__main__":
    test_precomputed()
