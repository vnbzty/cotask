import pickle
import ast
import json
import sys
import csv
import matplotlib
from numpy.core.multiarray import ndarray

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
from numpy import nan

x_ticks = [[1,2,3,4,5],[1,2,3,4,5],[1,10,100,1000,10000],[1.0,1.5,2.0,2.5,3.0]]
x_labels = ['edge server', 'cotask', 'task num', 'ratio']

def draw(k):
    labels = ['no mec', 'RRF', 'RRP', 'MINF', 'MINP', 'COOLF', 'COOLP']
    x = np.arange(0,5,1)
    start = k * 5 + 2
    end = start + 5
    for i in xrange(7):
        y = map(float, lines[i * 10 + 22][start: end])
        plt.plot(x, y, label=labels[i])

    plt.xticks(x, x_ticks[k])
    plt.xlabel(x_labels[k])
    plt.ylabel('CCT')
    plt.legend()
    plt.savefig('Data_rand_' + str(k) + '.png')

    plt.show()
    plt.clf()

with open('Data_rand.csv', 'r') as file:
    lines = csv.reader(file)
    lines = list(lines)

    for i in xrange(4):
        draw(i)



