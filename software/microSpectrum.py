
import time
import numpy as np

import sys

sys.path.append("c:/Users/benno/Dropbox/Hardware/mercuryITC")
import mercuryITC

tC = mercuryITC.temperatureControllerEthernet()

temp = tC.getSignal("mb1", "TEMP")
print "Temp: ", temp

def recordMicrowaveSpectrum(micro, keith, microRange, kea = 0, duration = 195):
    """Set kea = 1 only if doing a noise scan!
    #microRange is something like this
    microRange = np.linspace(187780, 188050, 19)"""

    if kea:
        f = microRange[0]
        micro.setFrequency(f)
        #run keith.prepareTTL() or so to enable TTL pulses
        keith.pulse()
        time.sleep(duration)
        
    micro.switchOn()
    for k in range(len(microRange)):
        f = microRange[k]
        micro.setFrequency(f)
        time.sleep(1)
        keith.pulse()

        print "Temp: ", tC.getSignal("db7", "TEMP")
        print "k: ", k
        print "f: ", f

        time.sleep(duration)

    keith.pulse()
    time.sleep(125)
    keith.pulse()


    
def recordMicrowavePowerDependence(micro, keith, powerRange,  duration = 75):
    """powerRange could look lie this.
    powerRange = [0.5, 1, 2, 5, 10, 20, 50]"""
    
    micro.switchOn()
    for k in range(len(powerRange)):
        p = powerRange[k]
        micro.setPower(p)
        time.sleep(1)
        keith.pulse()

        print "Temp: ", tC.getSignal("db7", "TEMP")
        print "k: ", k
        print "P: ", p

        time.sleep(duration)

    micro.switchOff()




def invFrequencyChange(micro, keith,f1, f2, duration = 75, jumps = 60):
    
    "keith.prepareTTL()"
    micro.setPower(30)
    "micro.switchOn()"
    for l in range(0, jumps):
        print "N: ", l
        time.sleep(0.5)
        micro.setFrequency(f1)
        time.sleep(0.5)
        print "f: ", f1
        time.sleep(1)
        micro.switchOn()
        time.sleep(1)
        time.sleep(duration)
        time.sleep(1)
        micro.switchOff()
        time.sleep(1)
        keith.pulse()
        time.sleep(1)
        micro.setFrequency(f2)
        time.sleep(1)
        print "f: ", f2
        time.sleep(1)
        micro.switchOn()
        time.sleep(1)
        time.sleep(duration)
        time.sleep(1)
        micro.switchOff()
        time.sleep(1)
        keith.pulse()
        
    micro.switchOff()

def invSignal2D(micro, keith,f1, duration = 1):
    "be sure keith is ready"
    
    micro.setFrequency(f1) 
    micro.setPower(30)     
    micro.switchOn()       
    keith.pulse()
    time.sleep(214)         
    keith.pulse()
    time.sleep(10)        
    micro.switchOff()      
    time.sleep(duration)   
    keith.pulse()          

def nutation(micro, keith, f, duration, td1):
    """A routine to switch the microwave off during saturation and pulse, cf. one of the papers by Hovav."""
    micro.setFrequency(f)
    micro.switchOn()
    keith.prepareTTL()
    
    for k in range(td1):
        micro.switchOff()
        keith.pulse()
        time.sleep(10)
        micro.switchOn()
        time.sleep(duration - 30)
        micro.switchOff()
        time.sleep(duration - 30 - 10)
        
