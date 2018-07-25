#!/usr/bin/python3
import os
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gsc

path = os.path.dirname(os.path.realpath(__file__))

x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []

print(path)
filename = sys.argv[1]#input("Enter filename: ")

with open(filename,'r') as tsvf:
    plots = csv.reader(tsvf, delimiter='\t')
    for row in plots:
        y1.append(float(row[8]))
        y2.append(float(row[9]))
        y3.append(float(row[10]))
        y4.append(float(row[11]))
        y5.append(float(row[12]))
        y6.append(float(row[13]))
        y7.append(float(row[14]))

x = list(range(1,1001))

fig = plt.figure(figsize=(22,12), dpi=80)
fig_size = plt.rcParams["figure.figsize"]

gs = gsc.GridSpec(7,1)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])
ax4 = fig.add_subplot(gs[3])
ax5 = fig.add_subplot(gs[4])
ax6 = fig.add_subplot(gs[5])
ax7 = fig.add_subplot(gs[6])

ax1.plot(x,y1, c='r')
ax2.plot(x,y2, c='r')
ax3.plot(x,y3, c='r')
ax4.plot(x,y4, c='r')
ax5.plot(x,y5, c='r')
ax6.plot(x,y6, c='r')
ax7.plot(x,y7, c='r')

gs.tight_layout(fig)
plt.show()

