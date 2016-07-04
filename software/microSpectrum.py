
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
    
    keith.prepareTTL()
    for l in range(0, jumps):
        print "N: ", l
        time.sleep(1)
        micro.setFrequency(f1)
        print "f: ", f1
        time.sleep(duration)
        keith.pulse()
        time.sleep(1)
        #keith.pulse() small flip angle pulse
        micro.setFrequency(f2)
        print "f: ", f2
        time.sleep(duration)
        keith.pulse()
       


