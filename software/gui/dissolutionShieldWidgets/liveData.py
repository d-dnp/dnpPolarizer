import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style
style.use('ggplot')


#import matplotlib.pyplot as plt
import numpy as np


import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import  Tkinter as Tk

#needs to get the master frame
#programm it in a functional style

def createLiveDataFrame(master, liveDataFrame):
    """ createLiveDataFrame

    Arguments
    - master: a dissolutionShieldWidget object
    - liveDataFrame: a Tk Frame

    The function generates various labels and buttons that depend on the Tk.StringVars master.t and master.p, as well as mater.pOpressure and master.pOtemperature

    It furthermore creates
    master.fig: a figure showing a plot
    master.ax1: axis to show pressure data
    master.ax2: axis to show temperature data

    as well as two plotOptionButtons (private)"""
    
    ### Live Data Frame - Elements
    pressureNameLabel = Tk.Label(liveDataFrame, text="Pressure:", anchor=Tk.E,
                                  foreground = "#00c", font=("Arial", 14))

    pressureValueLabel = Tk.Label(liveDataFrame, textvariable = master.p, anchor=Tk.W,
                                        foreground = "#0000cc", font=("Arial", 14, "bold"))

    temperatureNameLabel = Tk.Label(liveDataFrame, text="Temperature:", anchor=Tk.E,
                                     foreground="#c00", font=("Arial", 14))

    temperatureValueLabel = Tk.Label(liveDataFrame, textvariable = master.t, anchor=Tk.W,
                                           foreground = "#cc0000", font=("Arial", 14, "bold"))

    master.heaterIndicator = Tk.Canvas(liveDataFrame, width = 70, height = 70)
    master.heaterIndicatorCircle = master.heaterIndicator.create_oval((10, 10, 60, 60), fill = "#ddd", outline = "#ddd")
    master.heaterIndicatorText = master.heaterIndicator.create_text(36, 34, text = "HEATER")

        
    master.fig = Figure(figsize=(6, 6.5))
    master.ax1 = master.fig.add_axes([0.15, 0.6, 0.8, 0.35])
    
    master.ax1.set_ylabel("Pressure (bar)")
    master.ax1.set_xlabel("Time (m)")
    master.ax1.grid(True)

    master.ax1.set_xlim([master.pOpressure.xlimL, master.pOpressure.xlimU])
    master.ax1.set_ylim([master.pOpressure.ylimL, master.pOpressure.ylimU])

    master.ax2 = master.fig.add_axes([0.15, 0.15, 0.8, 0.35])
    master.ax2.set_ylabel("Temperature (C)")
    master.ax2.set_xlabel("Time (m)")
    master.ax2.grid(False)
    
    master.canvas = FigureCanvasTkAgg(master.fig, master=liveDataFrame)
    
    plotOptionButtonPressure = Tk.Button(liveDataFrame, text="Plot Options Pressure", command = lambda: master.changePlotOptions(master.pOpressure))
    plotOptionButtonTemperature = Tk.Button(liveDataFrame, text="Plot Options Temperature", command = lambda: master.changePlotOptions(master.pOtemperature))

    #now grid all these components
    pressureNameLabel.grid(row= 0, column=0, padx =2, pady = 2)
    pressureValueLabel.grid(row= 0, column=1, padx =2, pady = 2)

    temperatureNameLabel.grid(row= 1, column=0, padx =2, pady = 2)
    temperatureValueLabel.grid(row= 1, column=1, padx =2, pady = 2)

    master.heaterIndicator.grid(row = 0, column = 2, rowspan = 2, padx = 2, pady = 2)

    master.canvas.get_tk_widget().grid(row = 2, column = 0, columnspan = 3, padx = 2, pady = 2)
    plotOptionButtonPressure.grid(row=3, column = 0, columnspan = 1, padx = 2, pady = 2)   
    plotOptionButtonTemperature.grid(row=3, column = 1, columnspan = 1, padx = 2, pady = 2)


def updateLiveData(master):
    master.ax1.clear()

    if (master.dS.heaterOn == "1"):
        master.heaterIndicator.itemconfig(master.heaterIndicatorCircle, fill="#d00")
    elif (master.dS.heaterOn == "0"):
        master.heaterIndicator.itemconfig(master.heaterIndicatorCircle, fill="#ddd")
    else:
        print "heaterOn Value: ", master.dS.heaterOn
        master.heaterIndicator.itemconfig(master.heaterIndicatorCircle, fill="#0ff")
        
    time = np.array(master.dS.timeList)*master.pOpressure.xConversion[master.pOpressure.xDimIndex]
            
    if (master.pOpressure.autoXlim == True and time[-1] > master.pOpressure.xlimU):
        newPlotWidth = (master.pOpressure.xlimU - master.pOpressure.xlimL)*1.2
        master.pOpressure.xlimU = master.pOpressure.xlimL + newPlotWidth
                
    master.ax1.set_xlim([master.pOpressure.xlimL, master.pOpressure.xlimU])
    master.ax1.set_ylim([master.pOpressure.ylimL, master.pOpressure.ylimU])
    
    master.ax1.set_xlabel(master.pOpressure.xDim[master.pOpressure.xDimIndex])
    master.ax1.set_ylabel(master.pOpressure.yDim[master.pOpressure.yDimIndex])
        
    master.ax1.plot(time, master.dS.pressureList, "-bx")

    master.ax2.clear()

    time = np.array(master.dS.timeList)*master.pOtemperature.xConversion[master.pOtemperature.xDimIndex]

    if (master.pOtemperature.autoXlim == True and time[-1] > master.pOtemperature.xlimU):
        newPlotWidth = (master.pOtemperature.xlimU - master.pOtemperature.xlimL)*1.2
        master.pOtemperature.xlimU = master.pOtemperature.xlimL + newPlotWidth
            

    master.ax2.set_xlim([master.pOtemperature.xlimL, master.pOtemperature.xlimU])
    master.ax2.set_ylim([master.pOtemperature.ylimL, master.pOtemperature.ylimU])

    master.ax2.set_xlabel(master.pOtemperature.xDim[master.pOtemperature.xDimIndex])
    master.ax2.set_ylabel(master.pOtemperature.yDim[master.pOtemperature.yDimIndex])
        
    master.ax2.plot(
        np.array(master.dS.timeList)*master.pOtemperature.xConversion[master.pOtemperature.xDimIndex],
        master.dS.temperatureList, "-rx")

    master.canvas.draw()
            #print "Canvas drawn"

