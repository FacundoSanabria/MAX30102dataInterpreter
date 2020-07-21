import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
import scipy.signal as sps
import matplotlib.pyplot as plt

def get_ACsignal(sig, lam=100, p=0.1, niter=10):
    baseline = get_baseline_als(sig, lam, p)
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

def get_intersection(dx, dy, ex, ey, fx):
    m = get_slope(dx, dy, ex, ey)
    b = dy - m * dx
    rx = fx
    ry = m * rx + b
    return rx, ry

def get_slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)

def get_peaksAndValleys(sig):
    #find peaks
    peaks_X, auxDict = sps.find_peaks(sig, height=4000, width= 2, prominence = 0.3)
    peaks_Y = auxDict["peak_heights"]

    # find valleys (invert the signal, find the peaks, then invert the Y values)
    inverted_sig = [sample * -1 for sample in sig]
    valleys_X, auxDict = sps.find_peaks(inverted_sig, height=-40000000, width=2, prominence=0.3)
    valleys_Y = auxDict["peak_heights"]
    valleys_Y = [valley * -1 for valley in valleys_Y]

    return peaks_X, peaks_Y, valleys_X, valleys_Y

def get_DC_points(sig_peaks_X, sig_valleys_X, sig_valleys_Y): #get the DC point from the intercestion of two valleys an a peak
    DC_points = []
    i = 0
    while i+1 < len(sig_valleys_X) and i < len(sig_peaks_X):
        DC_points.append( get_intersection( sig_valleys_X[i], sig_valleys_Y[i], sig_valleys_X[i+1], sig_valleys_Y[i+1], sig_peaks_X[i]))
        i = i + 1
    return DC_points

def get_AC_points(DC_points, peaks_Y):
    AC_points = []
    for point, peak_Y in zip(DC_points, peaks_Y):
        AC_points.append([point[0], peak_Y - point[1]])
    return AC_points