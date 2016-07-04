import dissolutionShield as dS
import cryoShield as cS
import dissolutionShieldWidget as dSW
import cryoShieldWidget as cSW

reload(cS)
reload(cSW)


import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import  Tkinter as Tk
print "Python Version: ", sys.version_info[0]


class dnpWidget(Tk.Frame):
    def __init__(self, parent, dissShield, cryoShield):
        self.parent = parent
        self.dissShield = dissShield
        self.cryoShield = cryoShield

        self.initUI()

    def initUI(self):
        print "Initializing DNP Control UI"
        self.parent.title("DNP Control")

        dSFrame = Tk.Frame(relief = Tk.SUNKEN)
        cSFrame = Tk.Frame()
        
        self.dSWidget = dSW.dissolutionShieldWidget(dSFrame, self.dissShield)
        self.cryoWidget = cSW.cryoShieldWidget(cSFrame, self.cryoShield)
        
        dSFrame.grid(row = 0, column = 0, padx = 2, pady = 2, sticky = Tk.W + Tk.E + Tk.N)
        cSFrame.grid(row = 0, column = 1, padx = 2, pady = 2, sticky = Tk.W + Tk.E + Tk.N)

def main():
    root = Tk.Tk()
    dissAddress = ('10.1.15.250', 5000)
    cryoAddress = ('10.1.15.243', 5000)
    
    if len(sys.argv) > 1 and sys.argv[1] == "sim":
        print "Using Simulator"
        dissShield = dS.dissolutionShieldSimulator(dissAddress)
        cryoShield = None
    else:
        dissShield = dS.dissolutionShield(dissAddress)
        cryoShield = cS.cryoShield(cryoAddress)


    app = dnpWidget(root, dissShield, cryoShield)
    root.mainloop()

if __name__ == '__main__':
    main()
