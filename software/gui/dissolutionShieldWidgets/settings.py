import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style
style.use('ggplot')


import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import  Tkinter as Tk

#needs to get the master frame
#programm it in a functional style

def createSettingsFrame(master, settingsFrame):
    """ createSettingsFrame

    Arguments
    - master: a dissolutionShieldWidget object
    - liveDataFrame: a Tk Frame

    The function generates various labels and buttons that bind to Tk.StringVars master.tset, master.pset and master.regulation
    """

    rbFrame = Tk.Frame(settingsFrame)
    Tk.Radiobutton(rbFrame, text="Regulate via Pressure", variable=master.regulation, value="pressure", command = lambda: radioAction(master)).pack(anchor=Tk.W)
    Tk.Radiobutton(rbFrame, text="Regulate via Temperature", variable=master.regulation, value="temperature", command = lambda: radioAction(master)).pack(anchor=Tk.W)
        
    pSetLabel = Tk.Label(settingsFrame, text="P Set:", anchor=Tk.E,
                         foreground = "#00c", font=("Arial", 14))

    tSetLabel = Tk.Label(settingsFrame, text="T Set:", anchor=Tk.E,
                         foreground = "#c00", font=("Arial", 14))

    
    master.pSetEntry = Tk.Entry(settingsFrame, textvariable = master.pset, width=4)
    master.tSetEntry = Tk.Entry(settingsFrame, textvariable = master.tset, width=4)

    confirmButton = Tk.Button(settingsFrame, text="Confirm", command = lambda: confirm(master))

    

    #now grid all these components
    rbFrame.grid(row = 0, column = 0, columnspan = 2, padx = 2, pady = 2)
    pSetLabel.grid(row = 1, column = 0)
    master.pSetEntry.grid(row = 1, column = 1)
    tSetLabel.grid(row = 2, column = 0)
    master.tSetEntry.grid(row = 2, column = 1)
    confirmButton.grid(row = 3, columnspan = 2, sticky = Tk.E + Tk.W)

    master.tSetEntry.configure(state='disabled')
 
    
def radioAction(master):
    if master.regulation.get() == "pressure":
        master.pSetEntry.configure(state='normal')
        master.tSetEntry.configure(state='disabled')
    elif master.regulation.get() == "temperature":
        master.pSetEntry.configure(state='disabled')
        master.tSetEntry.configure(state='normal')

def confirm(master):
    #communicate changed settings to Arduino
    master.dS.setRegulation(master.regulation.get())
    if master.regulation.get() == "temperature":
        master.dS.setSetTemperature(master.tset.get())
    elif master.regulation.get() == "pressure":
        master.dS.setSetPressure(master.pset.get())
        

