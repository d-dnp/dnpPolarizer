import tkSimpleDialog
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import  Tkinter as Tk


class plotOptions(object):
    def __init__(self, xlimL, xlimU, ylimL, ylimU, shield, datatype="AB"):
        """Plot Options
        limits are limits of the plot.

        cryoShield: A Cryo-Shield Object
        type: AB for Allen-Bradley or CERNOX for Cernox

        Depending on the type the xDimensions are chosen.
        """
        self.xlimL = xlimL
        self.xlimU = xlimU
        self.ylimL = ylimL
        self.ylimU = ylimU
        if datatype == "AB":
            self.xDim = shield.ABxDim
            self.yDim = shield.AByDim

            self.xConversion = shield.ABxConversion
            self.yConversion = shield.AByConversion
                        
            self.xDimIndex = shield.ABxDimIndex
            self.yDimIndex = shield.AByDimIndex

        elif datatype == "CERNOX":
            self.xDim = shield.cernox_xDim
            self.yDim = shield.cernox_yDim

            self.xConversion =shield.cernox_xConversion
            self.yConversion =shield.cernox_yConversion

            self.xDimIndex = shield.cernox_xDimIndex
            self.yDimIndex = shield.cernox_yDimIndex



    def changeYDimension(self, new_yDimIndex, conversionFactor):
        pass
    
        

        
class plotOptionPoller(tkSimpleDialog.Dialog):
    def __init__(self, parent, pO, title="Plot Options"):
        """A Tk widget to poll for plot options. 
        Parent: the parent frame
        pO: A plot options object
        """
        
        self.xlimL = Tk.StringVar()
        self.xlimU = Tk.StringVar()
        self.ylimL = Tk.StringVar()
        self.ylimU = Tk.StringVar()

        self.xlimL.set(pO.xlimL)
        self.xlimU.set(pO.xlimU)
        self.ylimL.set(pO.ylimL)
        self.ylimU.set(pO.ylimU)

        self.pO = pO #this is a shallow copy (?)
        
        if sys.version_info[0] < 3:
            tkSimpleDialog.Dialog.__init__(self, parent, title=title)
        else:
            super().__init__()
        
    def body(self, master):

        Tk.Label(master, text="X Unit:").grid(row=0)
        Tk.Label(master, text="Y Unit:").grid(row=1)
        Tk.Label(master, text = "X Lim: ").grid(row=2)
        Tk.Label(master, text = "Y Lim: ").grid(row=3)


        
        self.xUnit = Tk.StringVar(master)
        self.xUnit.set("  " + self.pO.xDim[self.pO.xDimIndex])

        self.yUnit = Tk.StringVar(master)
        self.yUnit.set("  " + self.pO.yDim[self.pO.yDimIndex])

        xList = ["  " + x for x in self.pO.xDim]
        yList = ["  " + y for y in self.pO.yDim]

        
        self.xUnitOption = Tk.OptionMenu(master, self.xUnit, *xList)
        self.yUnitOption = Tk.OptionMenu(master, self.yUnit, *yList)

        self.xUnitOption.config(width=14)
        self.xUnitOption.config(anchor='w')#align text within the option menu on the left side. 
        self.yUnitOption.config(anchor='w')
        
        
        self.xlimLEntry = Tk.Entry(master, width=5, textvariable = self.xlimL)
        self.xlimUEntry = Tk.Entry(master, width=5, textvariable = self.xlimU)

        self.ylimLEntry = Tk.Entry(master, width=5, textvariable = self.ylimL)
        self.ylimUEntry = Tk.Entry(master, width=5, textvariable = self.ylimU)

        
        self.xUnitOption.grid(row=0, column=1, columnspan=2, sticky=Tk.W + Tk.E)
        self.yUnitOption.grid(row=1, column=1, columnspan=2, sticky=Tk.W + Tk.E)

        self.xlimLEntry.grid(row=2, column=1, sticky = Tk.W)
        self.xlimUEntry.grid(row=2, column=2, sticky = Tk.W)

        self.ylimLEntry.grid(row=3, column=1, sticky = Tk.W)
        self.ylimUEntry.grid(row=3, column=2, sticky = Tk.W)


    def apply(self):
        new_xlimL = float(self.xlimLEntry.get())
        new_xlimU = float(self.xlimUEntry.get())

        new_ylimL = float(self.ylimLEntry.get())
        new_ylimU = float(self.ylimUEntry.get())

        newX = self.pO.xDim.index(self.xUnit.get().lstrip())
        newY = self.pO.yDim.index(self.yUnit.get().lstrip())

        #if x or y limits have changed update them and do not recalculate limits. Else if only x or 
        #y dimensions have changed update the limits.

        #x:
        if new_xlimL != self.pO.xlimL or new_xlimU != self.pO.xlimU:
            #change xDim, but leave the axis as they are, they have been set explicitly by the user
            self.pO.xDimIndex = newX
            self.pO.xlimL = float(self.xlimLEntry.get())
            self.pO.xlimU = float(self.xlimUEntry.get())
        elif newX != self.pO.xDimIndex:
            conversionOldToSI = 1./self.pO.xConversion[self.pO.xDimIndex]
            conversionNewToSI = self.pO.xConversion[newX]
            self.pO.xlimL *= conversionOldToSI*conversionNewToSI
            self.pO.xlimU *= conversionOldToSI*conversionNewToSI
            self.pO.xDimIndex = newX

        #y:
        if new_ylimL != self.pO.ylimL or new_ylimU != self.pO.ylimU:
            #change yDim, but leave the axis as they are, they have been set explicitly by the user
            self.pO.yDimIndex = newY
            self.pO.ylimL = float(self.ylimLEntry.get())
            self.pO.ylimU = float(self.ylimUEntry.get())
        elif newY != self.pO.yDimIndex:
            conversionOldToSI = 1./self.pO.yConversion[self.pO.yDimIndex]
            conversionNewToSI = self.pO.yConversion[newY]
            self.pO.ylimL *= conversionOldToSI*conversionNewToSI
            self.pO.ylimU *= conversionOldToSI*conversionNewToSI
            self.pO.yDimIndex = newY            



