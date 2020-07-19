import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
import signalProcessor as signal




red_raw = []
ir_raw = []

#cargo los vectores con los valores medidos desde un csv
with open('C:\\Users\\katyVa\\Desktop\\Facundo\\medicionesMAX30102\\viejas\\oxigenacionCopia.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        red_raw.append(int(row[0]))
        ir_raw.append(int(row[1]))

red_raw = red_raw[90:]
ir_raw = ir_raw[90:]

# calcular el DC mean
red_DC_mean = signal.get_DC_mean(red_raw)
ir_DC_mean = signal.get_DC_mean(ir_raw)


# restar DC mean a la señal (no hace falta)
'''for red_raw_sample, ir_raw_sample in zip(red_raw, ir_raw):
    red_AC.append(red_raw_sample - red_DC_mean)
    ir_AC.append(ir_raw_sample - ir_DC_mean)''' #este es el metodo q utilizaba robertF

# get only the AC component of signal
red_AC = []
ir_AC = []
red_AC, red_baseline = signal.get_ACsignal(red_raw, 1000, 0.1)
ir_AC, ir_baseline = signal.get_ACsignal(ir_raw, 1000, 0.1)

#get root mean square of the AC component
red_RMS = signal.get_RMS(red_AC)
ir_RMS = signal.get_RMS(ir_AC)

#asigno el DC mean al promedio de la baseline(para mi deberia ser asi)
red_DC_mean = red_baseline[np.argmax(red_AC)]
ir_DC_mean = ir_baseline[np.argmax(ir_AC)]
#asigno el valor de AC al pico de la señal
red_RMS = np.max(red_AC)
ir_RMS = np.max(ir_AC)

#se calcula R: (redAC*irDC)/(irAC*redDC)
R = (red_RMS * ir_DC_mean)/(ir_RMS*red_DC_mean)


#plot signals

fig, axs = plt.subplots(3) #crea tres graficos distintos, uno arriba del otro
fig.set_size_inches(18.5, 10.5)
# graph of the raw signal
axs[0].plot(red_raw, color='red')
axs[1].plot(ir_raw, color='blue')
axs[0].hlines(red_DC_mean, 1, len(red_AC), color='#ffaaaa')
axs[1].hlines(ir_DC_mean, 1, len(ir_AC), color='#aaaaff')
axs[0].plot(red_baseline, color='#ff5555')
axs[1].plot(ir_baseline, color='#5555ff')
# graph of the raw signal
axs[2].plot(red_AC, color='red')
axs[2].plot(ir_AC, color='blue')
axs[2].hlines(red_RMS, 1, len(red_AC), color='#ff5555')
axs[2].hlines(ir_RMS, 1, len(ir_AC), color='#5555ff')



plt.show()
print("red DC mean:", red_DC_mean)
print("ir DC mean:", ir_DC_mean)
print("red RMS:", red_RMS)
print("ir RMS:", ir_RMS)
print("R:", R)

print()



