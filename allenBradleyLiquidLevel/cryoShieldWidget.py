import matplotlib.pyplot as plt
import numpy as np
import time

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style
style.use('ggplot')
import matplotlib.animation as animation

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import  Tkinter as Tk
print "Python Version: ", sys.version_info[0]

import cryoShield as cS
import plotOptions as pO
reload(cS)
reload(pO)

class cryoShieldWidget(Tk.Frame):
  
    #    def __init__(self, parent, queue, endCommand, cryoShield):

    def __init__(self, parent, queue, endCommand, cryoShield):
        Tk.Frame.__init__(self, parent)
        
        self.cS = cryoShield
        self.parent = parent
        self.queue = queue
        self.pOAB = pO.plotOptions(0, 1, 0, 1, self.cS)
        self.pOCERNOX = pO.plotOptions(0, 1, 0, 1, self.cS, datatype="CERNOX")

        self.doAutoPoll = Tk.StringVar()

        self.initUI()
        
    
    def initUI(self):
      
        self.parent.title("Cryo Shield")
        self.grid(row=0, column=0)

        self.tCernox = Tk.StringVar()
        self.tCernox.set("153.52 K")

        self.pollLongAB = Tk.IntVar()
        self.pollLongCERNOX = Tk.IntVar()
        
        self.whichDataSet = 0
        
        #ITEMS - First specify all the items!
        title = Tk.Label(self.parent, text="DNP Insert CryoShield", font="TkHeadingFont 16", foreground = "#000000")

        ### ALLEN BRADLEY
        abDataFrame = Tk.LabelFrame(self.parent, bd=1, text="Allen-Bradley", width=15)

        self.fig = Figure(figsize=(8, 3.5))
        self.ax1 = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        self.ax1.set_ylabel("AB1")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.grid(False)

        self.ax1.set_xlim([self.pOAB.xlimL, self.pOAB.xlimU])
        self.ax1.set_ylim([self.pOAB.ylimL, self.pOAB.ylimU])

        self.canvas = FigureCanvasTkAgg(self.fig, master=abDataFrame)

        plotOptionButtonAB = Tk.Button(abDataFrame, text="Plot Options", command = lambda: self.changePlotOptionsAB(self.pOAB, only="AB"))

        longTermSignalAB = Tk.Checkbutton(abDataFrame, text = " Long term", 
                                          variable = self.pollLongAB, command=self.readCryoShield)

        
        #use the frame colour to match the plot colour for a given resistor!
        levelCanvas = Tk.Canvas(abDataFrame, width=400, height = 50)
        levelCanvas.create_rectangle(30, 10, 120, 40, 
            outline="#f00", fill="#acf")
        levelCanvas.create_rectangle(150, 10, 240, 40, 
            outline="#f0f", fill="#acf")
        levelCanvas.create_rectangle(270, 10, 370, 40, 
            outline="#00f", fill="#acf")  

        #Cernox Frame
        cernoxFrame = Tk.LabelFrame(self.parent, bd=1, text="Cernox", width=15)

        #this contains the temperature plot and goes into a second canvas
        self.fig2 = Figure(figsize=(8, 3.5))
        self.ax2 = self.fig2.add_axes([0.1, 0.1, 0.8, 0.8])
        self.ax2.set_ylabel("T (K)")
        self.ax2.set_xlabel("Time (h)")
        self.ax2.grid(False)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=cernoxFrame)

        self.ax2.set_xlim([self.pOCERNOX.xlimL, self.pOCERNOX.xlimU])
        self.ax2.set_ylim([self.pOCERNOX.ylimL, self.pOCERNOX.ylimU])

        plotOptionButtonCERNOX = Tk.Button(cernoxFrame, text="Plot Options", command = lambda: self.changePlotOptionsCERNOX(self.pOCERNOX, only="CERNOX"))

        temperatureFrame = Tk.Frame(cernoxFrame, width=400, height=50, background="#dddddd")
        tCernoxLabel = Tk.Label(temperatureFrame, width=12, text="Temperature:", anchor=Tk.W, foreground="#0000CC", font="TkIconFont 15")
        tCernoxValue = Tk.Label(temperatureFrame, textvariable = self.tCernox, anchor=Tk.W, foreground="#0000CC", font="TkIconFont 15")


        longTermSignalCERNOX = Tk.Checkbutton(cernoxFrame, text = " Long term", variable = self.pollLongCERNOX, command=self.readCryoShield)
        
        tReadButton = Tk.Button(self.parent, text="Read", command=lambda: self.readCryoShield(only = ""))        

        self.var = Tk.IntVar()
        autoUpdateButton = Tk.Checkbutton(self.parent, text="Auto Poll",  variable=self.var, command=lambda: self.autoPoll(self.var.get()))
        #autoPollButton.var = self.doAutoPoll

        cernoxFrame.columnconfigure(2, minsize=400)
        cernoxFrame.rowconfigure(1, minsize=40)
        
        #LAYOUT - Now arrange the layout
        title.grid(row = 0, column = 0, padx = 2, pady = 2, sticky = Tk.W+Tk.E)

        abDataFrame.grid(row = 1, column = 0, padx = 2, pady = 2, sticky=Tk.W+Tk.E)
        self.canvas.get_tk_widget().grid(row = 0, column = 0, columnspan = 3, sticky = Tk.W + Tk.E + Tk.N + Tk.S)
        plotOptionButtonAB.grid(row=1, column = 0, padx = 2, pady = 2, sticky = Tk.E)
        longTermSignalAB.grid(row = 1, column = 1, padx = 2, pady = 2, sticky = Tk.E)
        levelCanvas.grid(row=1, column=2, sticky = Tk.E)
        
        cernoxFrame.grid(row = 2, column=0, padx = 2, pady = 2, sticky = Tk.E)
        self.canvas2.get_tk_widget().grid(row = 0, column=0, columnspan=3, sticky = Tk.W + Tk.E + Tk.N + Tk.S)
        plotOptionButtonCERNOX.grid(row=1, column=0, padx = 2, pady = 2, sticky = Tk.E)

        longTermSignalCERNOX.grid(row = 1, column = 1, padx = 2, pady = 2, sticky = Tk.E)
        temperatureFrame.grid(row = 1, column = 2, padx = 2, pady = 2)

        tCernoxValue.pack(side=Tk.RIGHT)
        tCernoxLabel.pack(side=Tk.RIGHT)

        
        tReadButton.grid(row = 3, column = 0, padx = 2, pady = 2, sticky = Tk.E)
        autoUpdateButton.grid(row=5, column=0, padx = 2, pady = 2, sticky = Tk.E)




        #self.canvas2.get_tk_widget().grid(row = 1, column = 0, columnspan = 4, sticky = Tk.W + Tk.E + Tk.N + Tk.S)

        tReadButton.focus_set()

        print "Tk widget obtained and gridded"

    def changePlotOptionsAB(self, options, only=""):
        pO.plotOptionPoller(self.parent, options)
        #if autoPoll is not active do readCryoShield
        if not int(self.var.get()):
            self.readCryoShield(only = "AB")

    def changePlotOptionsCERNOX(self, options, only=""):
        pO.plotOptionPoller(self.parent, options)
        #if autoPoll is not active do readCryoShield
        if not int(self.var.get()):
            self.readCryoShield(only="CERNOX")


            
            
    def readCryoShield(self, only="CERNOX"):
        #this function is quite redundant with changePlotOptions. Edit
        print "only is: ", only
        if only != "CERNOX":
            x1, d1 = self.cS.pollChannel("AB1", xDim = self.pOAB.xDimIndex, yDim = self.pOAB.yDimIndex)
            x2, d2 = self.cS.pollChannel("AB2", xDim = self.pOAB.xDimIndex, yDim = self.pOAB.yDimIndex)
            x3, d3 = self.cS.pollChannel("AB3", xDim = self.pOAB.xDimIndex, yDim = self.pOAB.yDimIndex)

        
            self.ax1.clear()

            self.ax1.set_xlim([self.pOAB.xlimL, self.pOAB.xlimU])
            self.ax1.set_ylim([self.pOAB.ylimL, self.pOAB.ylimU])

            self.ax1.set_xlabel(self.pOAB.xDim[self.pOAB.xDimIndex])
            self.ax1.set_ylabel(self.pOAB.yDim[self.pOAB.yDimIndex])
        
            self.ax1.plot(x1, d1, "rx")
            self.ax1.plot(x2, d2, "mx")
            self.ax1.plot(x3, d3, "bx")
            self.canvas.draw()

        if only != "AB": 
            x4, d4 = self.cS.pollChannel("CERNOX", xDim = self.pOCERNOX.xDimIndex, yDim = self.pOCERNOX.yDimIndex)
            self.ax2.clear()

            #this depends!!
            self.ax2.set_xlim([self.pOCERNOX.xlimL, self.pOCERNOX.xlimU])
            self.ax2.set_ylim([self.pOCERNOX.ylimL, self.pOCERNOX.ylimU])
        
            self.ax2.set_xlabel(self.pOCERNOX.xDim[self.pOCERNOX.xDimIndex])
            self.ax2.set_ylabel(self.pOCERNOX.yDim[self.pOCERNOX.yDimIndex])
        
            self.ax2.plot(x4, d4, "-rx")        
            self.canvas2.draw()
        


    def autoPoll(self, var):
        
        def task():
			self.readCryoShield()
			time.sleep(0.1)
			print "Auto Poll Variable: ", var
			if int(self.var.get()):
				self.master.after(2000, task)

        self.master.after(200, task())

        

#    def quit(self):
#        self.parent.quit()
#        self.parent.destroy()

class Bunch(object):
    """
    http://code.activestate.com/recipes/52308
    foo=Bunch(a=1,b=2)
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

def main():
    address= ( '10.1.15.243', 5000) #define server IP and port

    root = Tk.Tk()
    #root.geometry("750x700+300+300")
	#    queue = Queue.Queue()
    cryoShield = cS.cryoShield(address)
    app = cryoShieldWidget(root, None, None, cryoShield)
    root.mainloop()  


if __name__ == '__main__':
    main()
