from serialPlot import serialPlot
from SerialPlotOx import serialPlotOx
from serialPlotElectro import serialPlotElectro
from tkinter import *
from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import copy
import pandas as pd
from PIL import ImageTk, Image
from tkinter import filedialog
import os





path = 'Unibague_ESCUDO.PNG'



root = Tk()

root.title("Prototipo Myo ArmBand")
image1 = Image.open(path)
test = ImageTk.PhotoImage(image1)

label1 = Label(image=test)
label1.image = test


label1.place(x=150, y=0)
root.geometry('260x100')
"""
# root window title and dimension

# Set geometry(widthxheight)

"""

# adding a label to the root window
lbl = Label(root, text = "COM:")
lbl.grid(column =0, row =0)
 
# adding Entry Field
txt = Entry(root, width=10)
txt.grid(column =1, row =0)


 
 
# function to display user text when
# button is clicked
def BntAcc():
 
    #res = "You Press Acc" + txt.get()
    #lbl.configure(text = res)
    
    def makeFigure(xLimit, yLimit, title):
        xmin, xmax = xLimit
        ymin, ymax = yLimit
        fig = plt.figure()
        ax = plt.axes(xlim=(xmin, xmax), ylim=(int(ymin - (ymax - ymin) / 10), int(ymax + (ymax - ymin) / 10)))
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel("Accelerometer Output")
        return fig, ax


    def mainaCC():
        portName = txt.get() #'COM3'
       
        baudRate = 115200
        maxPlotLength = 100     # number of points in x-axis of real time plot
        dataNumBytes = 4        # number of bytes of 1 data point
        numPlots =   3         # number of plots in 1 graph
        s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes, numPlots)   # initializes all required variables
        s.readSerialStart()                                               # starts background thread

        # plotting starts below
        pltInterval = 50    # Period at which the plot animation updates [ms]
        xmin = 0
        xmax = maxPlotLength
        ymin = -(100)
        ymax = 100
        fig = plt.figure(figsize=(10, 8))
        ax = plt.axes(xlim=(xmin, xmax), ylim=(float(ymin - (ymax - ymin) / 10), float(ymax + (ymax - ymin) / 10)))
        ax.set_title('Acelerometro')
        ax.set_xlabel("Time")
        ax.set_ylabel("Accelerometer Output")

        lineLabel = ['X', 'Y', 'Z']
        style = ['r-', 'c-', 'b-']  # linestyles for the different plots
        timeText = ax.text(0.70, 0.95, '', transform=ax.transAxes)
        lines = []
        lineValueText = []
        for i in range(numPlots):
            lines.append(ax.plot([], [], style[i], label=lineLabel[i])[0])
            lineValueText.append(ax.text(0.70, 0.90-i*0.05, '', transform=ax.transAxes))
        anim = animation.FuncAnimation(fig, s.getSerialData, fargs=(lines, lineValueText, lineLabel, timeText), interval=pltInterval)    # fargs has to be a tuple

        plt.legend(loc="upper left")
        plt.show()
        s.close()
    mainaCC();


def BntOxm():
 
    
   
    
    def makeFigure(xLimit, yLimit, title):
        xmin, xmax = xLimit
        ymin, ymax = yLimit
        fig = plt.figure()
        ax = plt.axes(xlim=(xmin, xmax), ylim=(int(ymin - (ymax - ymin) / 10), int(ymax + (ymax - ymin) / 10)))
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel("Accelerometer Output")
        return fig, ax


    def mainox():
        portName = txt.get() #'COM3'
        
        baudRate = 115200
        maxPlotLength = 100     # number of points in x-axis of real time plot
        dataNumBytes = 4        # number of bytes of 1 data point
        numPlots =   2         # number of plots in 1 graph
        s = serialPlotOx(portName, baudRate, maxPlotLength, dataNumBytes, numPlots)   # initializes all required variables
        s.readSerialStart()                                               # starts background thread
        
        # plotting starts below
        pltInterval = 10    # Period at which the plot animation updates [ms]
        lineLabelText = ['ir', 'red']#,'IR','RED']
        title = ['IR','RED',]#,'IR MAX30100', 'RED MAX30100']
        xLimit = [(0, maxPlotLength), (0, maxPlotLength)]#,(0, maxPlotLength),(0, maxPlotLength)]
        yLimit = [(-2000, 2000),(-2000, 2000)]#, (0, 2000), (0, 2000)]
        style = ['r-', 'g-',]#,'b-','r-']    # linestyles for the different plots
        anim = []
        for i in range(numPlots):
            fig, ax = makeFigure(xLimit[i], yLimit[i], title[i])
            lines = ax.plot([], [], style[i], label=lineLabelText[i])[0]
            timeText = ax.text(0.50, 0.95, '', transform=ax.transAxes)
            lineValueText = ax.text(0.50, 0.90, '', transform=ax.transAxes)
            anim.append(animation.FuncAnimation(fig, s.getSerialData, fargs=(lines, lineValueText, lineLabelText[i], timeText, i), interval=pltInterval))  # fargs has to be a tuple
            plt.legend(loc="upper left")
        plt.show()

        s.close()

    mainox();

def BntEmg():
 
    def makeFigure(xLimit, yLimit, title):
        
        xmin, xmax = xLimit
        ymin, ymax = yLimit
        fig = plt.figure()
        ax = plt.axes(xlim=(xmin, xmax), ylim=(int(ymin - (ymax - ymin) / 10), int(ymax + (ymax - ymin) / 10)))
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel("Accelerometer Output")
        return fig, ax


    def mainaElec():
        portName = txt.get() #'COM3'
       
        baudRate = 115200
        maxPlotLength = 100     # number of points in x-axis of real time plot
        dataNumBytes = 4        # number of bytes of 1 data point
        numPlots =   4        # number of plots in 1 graph
        s = serialPlotElectro(portName, baudRate, maxPlotLength, dataNumBytes, numPlots)   # initializes all required variables
        s.readSerialStart()                                               # starts background thread

        # plotting starts below
        pltInterval = 10    # Period at which the plot animation updates [ms]
        lineLabelText = ['Electrodo 1','Electrodo 2','Electrodo 3','Electrodo 4']
        title = ['Electrodo 1','Electrodo 2','Electrodo 3','Electrodo 4']#,'IR MAX30100', 'RED MAX30100']
        xLimit = [(0, maxPlotLength), (0, maxPlotLength),(0, maxPlotLength),(0, maxPlotLength)]
        yLimit = [(-1000, 1000),(-1000, 1000), (-1000, 1000), (-1000, 1000)]
        style = ['r-', 'g-','b-','r-']    # linestyles for the different plots
        anim = []
        for i in range(numPlots):
            fig, ax = makeFigure(xLimit[i], yLimit[i], title[i])
            lines = ax.plot([], [], style[i], label=lineLabelText[i])[0]
            timeText = ax.text(0.50, 0.95, '', transform=ax.transAxes)
            lineValueText = ax.text(0.50, 0.90, '', transform=ax.transAxes)
            anim.append(animation.FuncAnimation(fig, s.getSerialData, fargs=(lines, lineValueText, lineLabelText[i], timeText, i), interval=pltInterval))  # fargs has to be a tuple
            plt.legend(loc="upper left")
        plt.show()

        s.close()
    mainaElec();
 
#Acelerometro
btn = Button(root, text = "Acelerometro" ,fg = "black", command=BntAcc)
btn.grid(column=1, row=80)


# Oximetro
btn = Button(root, text = "Oximetro" ,fg = "black", command=BntOxm)
btn.grid(column=1, row=90)



#EMG
btn = Button(root, text = "EMG" ,fg = "black", command=BntEmg)
btn.grid(column=1, row=100)





# Execute Tkinter
root.mainloop()


