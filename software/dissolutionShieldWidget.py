import time


from gui.dissolutionShieldWidgets import liveData, settings, valves
reload(liveData)
reload(settings)
reload(valves)

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import  Tkinter as Tk
print "Python Version: ", sys.version_info[0]

import dissolutionShield as dS


import plotOptions as pO
reload(dS)
reload(pO)

class dissolutionShieldWidget(Tk.Frame):
  
    #    def __init__(self, parent, queue, endCommand, cryoShield):

    def __init__(self, parent, dissolutionShield):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.dS = dissolutionShield
        self.pOpressure = pO.plotOptions(0, 1, 0, 15, self.dS, datatype = "Pressure", autoXlim = True, autoYlim = True)
        self.pOtemperature = pO.plotOptions(0, 1, 10, 170, self.dS, datatype="Pt100", autoXlim = True, autoYlim = True)

        self.initUI()
        
    
    def initUI(self):
        try:
            self.parent.title("Dissolution Shield")
        except AttributeError:
            #Parent window is not a root window
            pass
        
        self.grid(row=0, column=0)

        self.t = Tk.StringVar()
        self.t.set("0")

        self.regulation = Tk.StringVar()
        self.regulation.set("pressure")

        self.p = Tk.StringVar()
        self.p.set("0")

        self.tset = Tk.StringVar()
        self.tset.set("10")

        self.pset = Tk.StringVar()
        self.pset.set("0")
        
        self.valve1 = Tk.IntVar()
        self.valve2 = Tk.IntVar()

        self.autoPollOn = Tk.IntVar()
        
        self.whichDataSet = 0


        # Main Frame Elements 
        title = Tk.Label(self.parent, text="Dissolution Settings", font="TkHeadingFont 16", foreground = "#000000")

        ### General Frames
        liveDataFrame = Tk.LabelFrame(self.parent, bd=3, text="Live Data")
        liveData.createLiveDataFrame(self, liveDataFrame)

        settingsFrame = Tk.LabelFrame(self.parent, bd=3, text="Settings", width = 200)
        settings.createSettingsFrame(self, settingsFrame)

        valvesFrame = Tk.LabelFrame(self.parent, bd=3, text="Valves")
        valves.createValvesFrame(self, valvesFrame)
        
        armFrame = Tk.LabelFrame(self.parent, bd=1, text="Arm", width=15)

        readButton = Tk.Button(self.parent, text="Read", command=lambda: self.readShield())        
        autoUpdateButton = Tk.Checkbutton(self.parent, text="Auto Poll",  variable=self.autoPollOn, command=lambda: self.autoPoll(self.autoPollOn.get()))

        #Main Frame gridding
        title.grid(row = 0, column = 0, padx = 2, pady = 2, sticky = Tk.W+Tk.E)
        liveDataFrame.grid(row = 1, column = 0, rowspan = 2)
        settingsFrame.grid(row = 1, column = 1, sticky = Tk.E + Tk.W + Tk.N)
        valvesFrame.grid(row = 2, column = 1, sticky = Tk.N)

        readButton.grid(row= 3, column = 0, padx = 2, pady = 2)
        autoUpdateButton.grid(row = 3, column = 1, padx = 2, pady = 2)

        #tReadButton.focus_set()

        print "Tk widget obtained and gridded"

    def changePlotOptions(self, options):
        pO.plotOptionPoller(self.parent, options)
        #if autoPoll is not active do readCryoShield
        if not int(self.autoPollOn.get()):
            self.readShield()
            
            
    def readShield(self):
        self.dS.getHeaterStatus()
        self.dS.getTemperatureAndPressure()
        self.t.set(str(self.dS.temperatureList[-1]) + " C")
        self.p.set(str(self.dS.pressureList[-1]) + " bar")
        liveData.updateLiveData(self)

        
    def autoPoll(self, var):
        
        def task():
			self.readShield()
			time.sleep(0.1)
			print "Auto Poll Variable: ", self.autoPollOn.get()
			if int(self.autoPollOn.get()):
				self.master.after(1000, task)

        self.master.after(200, task())

        
def main():
    address= ( '10.1.15.250', 5000) #define server IP and port

    root = Tk.Tk()
    #root.geometry("750x700+300+300")
	#    queue = Queue.Queue()
    global dissShield

    print "Sys Arguments: ", sys.argv

    if len(sys.argv) > 1 and sys.argv[1] == "sim":
        print "Using Simulator"
        dissShield= dS.dissolutionShieldSimulator(address)
    else:
        dissShield = dS.dissolutionShield(address)

    app = dissolutionShieldWidget(root, dissShield)

    root.mainloop()  


if __name__ == '__main__':
    main()
