#!/usr/bin/env python

from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import copy
import pandas as pd


class serialPlotElectro:
    def __init__(self, serialPort='/dev/ttyUSB0', serialBaud=38400, plotLength=100, dataNumBytes=2, numPlots=1):
        self.port = serialPort
        self.baud = serialBaud
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.numPlots = numPlots
        self.rawData = bytearray(numPlots * dataNumBytes)
        self.dataType = None
        self.dataType = 'i'     # 4 byte float
        self.data = []
        self.privateData = None     # for storing a copy of the data so all plots are synchronized
        for i in range(numPlots):   # give an array for each type of data and store them in a list
            self.data.append(collections.deque([0] * plotLength, maxlen=plotLength))
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        self.csvData = []

        print('Trying to connect to: ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=1.0)
            self.serialConnection.write(bytes('3', 'utf-8'))
            print('Connected to ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')

    def readSerialStart(self):
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.05)

    def getSerialData(self, frame, lines, lineValueText, lineLabel, timeText, pltNumber):
        if pltNumber == 0:  # in order to make all the clocks show the same reading
            currentTimer = time.perf_counter()
            self.plotTimer = int((currentTimer - self.previousTimer) * 1000)     # the first reading will be erroneous
            self.previousTimer = currentTimer
        self.privateData = copy.deepcopy(self.rawData)    # so that the 3 values in our plots will be synchronized to the same sample time
        timeText.set_text('Plot Interval = ' + str(self.plotTimer) + 'ms')
        data = self.privateData[(pltNumber*self.dataNumBytes):(self.dataNumBytes + pltNumber*self.dataNumBytes)]
        value,  = struct.unpack(self.dataType, data)
        self.data[pltNumber].append(value)    # we get the latest data point and append it to our array
        print()
        lines.set_data(range(self.plotMaxLength), self.data[pltNumber])
        lineValueText.set_text('[' + lineLabel + '] = ' + str(value))
        
        #self.csvData.append([self.data[0][-1], self.data[1][-1], self.data[2][-1],self.data[3][-1]])
    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.serialConnection.readinto(self.rawData)
            self.isReceiving = True

    def close(self):
        self.isRun = False
        self.serialConnection.write(bytes('6', 'utf-8'))
        self.thread.join()
        self.serialConnection.close()
        
        print('Disconnected...')
        #df = pd.DataFrame(self.csvData)
        #df.to_csv("data.csv")




