'''

based in algorithm described in the Post-Processing section from Maxim's Recommended Configurations and Operating Profiles
for MAX30101/MAX30102 EV Kits
https://pdfserv.maximintegrated.com/en/an/AN6409.pdf

'''

import numpy as np
import matplotlib.pyplot as plt
import signalProcessor as signal
import scipy.signal as sps
import signalProcessor


def triangleAlgorithm(red_raw, ir_raw):

    #find peaks and valleys
    red_peaks_X, red_peaks_Y, red_valleys_X, red_valleys_Y = signalProcessor.get_peaksAndValleys(red_raw)
    ir_peaks_X, ir_peaks_Y, ir_valleys_X, ir_valleys_Y = signalProcessor.get_peaksAndValleys(ir_raw)

    # si empieza con un pico antes q un valley saco el primer pico pq no lo voy a considerar
    if red_peaks_X[0] < red_valleys_X[0]:
        red_peaks_X = red_peaks_X[1:]
        red_peaks_Y = red_peaks_Y[1:]
    if ir_peaks_X[0] < ir_valleys_X[0]:
        ir_peaks_X = ir_peaks_X[1:]
        ir_peaks_Y = ir_peaks_Y[1:]

    #find m of each cycle
    red_DC_points = signalProcessor.get_DC_points(red_peaks_X, red_valleys_X, red_valleys_Y)
    ir_DC_points = signalProcessor.get_DC_points(ir_peaks_X, ir_valleys_X, ir_valleys_Y)


    #find AC component of each cycle
    red_AC_points = signalProcessor.get_AC_points(red_DC_points, red_peaks_Y)
    ir_AC_points = signalProcessor.get_AC_points(ir_DC_points, ir_peaks_Y)

    #find R of each cycle: (redAC*irDC)/(irAC*redDC)
    partialRs = []
    for red_DC_point, red_AC_point, ir_DC_point, ir_AC_point in zip(red_DC_points, red_AC_points, ir_DC_points, ir_AC_points):
        partialRs.append((red_AC_point[1] * ir_DC_point[1]) / (ir_AC_point[1] * red_DC_point[1]))

    #get the mean of R for the hole data
    R = np.mean(partialRs)

    # plot signals
    fig, axs = plt.subplots(2)  # crea tres graficos distintos, uno arriba del otro
    fig.set_size_inches(18.5, 10.5)
    # graph of the raw signal
    axs[0].plot(red_raw, color='red')
    axs[1].plot(ir_raw, color='blue')

    #grafica peaks and valleys
    axs[0].scatter(red_peaks_X, red_peaks_Y)
    axs[1].scatter(ir_peaks_X, ir_peaks_Y)
    axs[0].scatter(red_valleys_X, red_valleys_Y)
    axs[1].scatter(ir_valleys_X, ir_valleys_Y)

    axsMin, _ = axs[0].get_ylim()
    for peak_X, peak_Y, AC_point in zip(red_peaks_X, red_peaks_Y, red_AC_points):
        axs[0].vlines(peak_X, axsMin, peak_Y, color='#ffaaaa', linestyles='--') #grafica una linea punteada vertical hasta cada pico
        axs[0].vlines(peak_X, peak_Y - AC_point[1], peak_Y, color='#ffaaaa', linestyles='-') #grafica una linea solida vertical desde cada DC point hasta cada pico
    axsMin, _ = axs[1].get_ylim()
    for peak_X, peak_Y, AC_point in zip(ir_peaks_X, ir_peaks_Y, ir_AC_points):
        axs[1].vlines(peak_X, axsMin, peak_Y, color='#ffaaaa', linestyles='--') #grafica una linea punteada vertical hasta cada pico
        axs[1].vlines(peak_X, peak_Y - AC_point[1], peak_Y, color='#ffaaaa', linestyles='-')  #grafica una linea solida vertical desde cada DC point hasta cada pico

    #grafica los DC points
    axs[0].plot(*zip(*red_DC_points), marker='.', linestyle='none', color='#ffaaaa')
    axs[1].plot(*zip(*ir_DC_points), marker='.', linestyle='none', color='#aaaaff')

    plt.show()

    print(partialRs)
    return R