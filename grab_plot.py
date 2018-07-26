#!/usr/bin/python3
import os
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gsc
import serial
from time import sleep
import subprocess as sp

path = os.path.dirname(os.path.realpath(__file__))

x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []

name = sys.argv[1]

try:
    ser = serial.Serial(
        port='/dev/ttyUSB0',\
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS)

    print("connected to: " + ser.portstr)
    ser.flushInput()
except:
    print("enable to connect to serial...")
    serial.Serial().flushInput()
    serial.Serial().close()
    exit()

def grab_1000(session,filename,test):
    ser.flushInput()
    with open(filename, 'w') as tsvf:
        tw = csv.writer(tsvf, delimiter=',')
        row = 0
        nl = False
        while nl == False:
            b=ser.readline()
            print("waiting for 102 before nl: {0}".format(len(b)))
            if len(b) >= 100:
                nl = True
            sleep(1)
        while row < 200:
            reading = ser.readline()
            data=reading.decode().split('\t')
            print(data,row,len(data))
            if len(data) == 16:
                data[15]=data[15].replace("\r\n","")
                tw.writerow(data)
                y1.append(float(data[8]))
                y2.append(float(data[9]))
                y3.append(float(data[10]))
                y4.append(float(data[11]))
                y5.append(float(data[12]))
                y6.append(float(data[13]))
                y7.append(float(data[14]))
                row+=1
            sleep(0.05)
    x = list(range(1,201))
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

def get_size(x):
    switcher = {
            0: "12mm",
            1: "15mm",
            2: "20mm",
            3: "26mm",
            4: "35mm",
            5: "40mm",
            6: "50mm"
            }
    return switcher.get(x, lambda: "Invalid entry")

session = input("Enter session number: ")
start = input("Enter test number to start(0:12mm, 1:15,2:20,3:26,4:35,5:40,6:50): ")
for i in range(int(start),7):
    size = get_size(i)
    input("Place in {0} tube,enter to continue...".format(size))
    good_data=False
    while good_data == False:
        filename = "s{0}_{2}_{1}".format(session,name,get_size(i))
        grab_1000(session,filename,i)
        yn = input("Good data? (y/n): ")
        if yn == "y":
            try:
                sp.call(["./xwriter.py",filename])
                good_data=True
            except:
                print("Data bad, retrying...")
                input("Place in {0} tube,enter to continue...".format(size))
        y1.clear()
        y2.clear()
        y3.clear()
        y4.clear()
        y5.clear()
        y6.clear()
        y7.clear()

ser.close()
