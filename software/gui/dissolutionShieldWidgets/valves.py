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

def createValvesFrame(master, valvesFrame):
    """ createLiveDataFrame

    Arguments
    - master: a dissolutionShieldWidget object
    - valvesFrame: a Tk Frame

    The function draws a Canvas with rectangles representing the various valves.
    """
    xSpacing = 50
    
    ### valves Frame - Elements
    master.valveCanvas = Tk.Canvas(valvesFrame, width = 200, height = 130)

    #He drive, valves 1 and 2, with 2 = not 1
    master.valve1 = master.valveCanvas.create_rectangle((5,20,50,80), fill = "#0d0")
    master.valveCanvas.create_text((26, 89), text="He Drive")

    #bomb, valve4
    master.valve4 = master.valveCanvas.create_rectangle((5+xSpacing,20,50+xSpacing,80), fill = "#0d0")
    master.valveCanvas.create_text((26 + xSpacing, 89), text = "BOMB")

    #he inlet fast, valve8
    master.valve8 = master.valveCanvas.create_rectangle((5+2*xSpacing,20,50+2*xSpacing,80), fill = "#ddd")
    master.valveCanvas.create_text((26 + 2*xSpacing, 89), text = "FAST")

    master.valve9 = master.valveCanvas.create_rectangle((5+3*xSpacing,20,50+3*xSpacing,80), fill = "#ddd")
    master.valveCanvas.create_text((26 + 3*xSpacing, 89), text = "SLOW")

    master.valveCanvas.tag_bind(master.valve1, '<ButtonPress-1>', lambda _: toogleValve(master, 1))
    master.valveCanvas.tag_bind(master.valve4, '<ButtonPress-1>', lambda _: toogleValve(master, 4))
    master.valveCanvas.tag_bind(master.valve8, '<ButtonPress-1>', lambda _: toogleValve(master, 8))
    #master.valveCanvas.tag_bind(master.valve9, '<ButtonPress-1>', lambda _: toogleValve(master, 4))
     
    #now grid all these components
    master.valveCanvas.pack()

def toogleValve(master, valve):
    print "Toogling Valve ", valve

    master.dS.toogleValve(valve)

    updateValves(master)
    #the valve status can be represented by one byte
    #0b00000000 (for valves 8..1) 

    
def updateValves(master):
    valvePosition = [2**(1-1),2**(4-1),2**(8-1)]
    valveList = [master.valve1, master.valve4, master.valve8]
    for i in range(len(valvePosition)):
        #if the valve is on, set the rectangle color to green, else gray
        if (master.dS.valves & valvePosition[i]) > 0:
            master.valveCanvas.itemconfigure(valveList[i], fill="#0d0")
        else:
            master.valveCanvas.itemconfigure(valveList[i], fill = "#ddd")
    

