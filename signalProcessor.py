import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def get_ACsignal(sig, lam=100, p=0.1, niter=10):
    baseline = []
    baseline = get_baseline_als(sig, lam, p)
    for sample in sig:
        AC_signal = sig - baseline
    return AC_signal, baseline


def get_baseline_als(y, lam, p, niter=10): #got from https://stackoverflow.com/questions/29156532/python-baseline-correction-library
    L = len(y)
    D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
    D = lam * D.dot(D.transpose()) # Precompute this term since it does not depend on `w`
    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)
    for i in range(niter):
        W.setdiag(w) # Do not create a new matrix, just update diagonal values
        Z = W + D
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z


def get_DC_mean(sig):
    return np.mean(sig)


def get_RMS(sig):
    return np.sqrt( np.mean( sig.astype(np.dtype(np.int64)) ** 2 ))


