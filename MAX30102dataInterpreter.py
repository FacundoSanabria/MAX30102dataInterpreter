
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
import signalProcessor as signal
import dataInput
from baselineAlgorithm import baselineAlgorithm
from triangleAlgorithm import triangleAlgorithm


red_raw, ir_raw = dataInput.getDataFromCSV()

R = baselineAlgorithm(red_raw, ir_raw)
print("R:", R)
R = triangleAlgorithm(red_raw, ir_raw)
print("R:", R)

print()



