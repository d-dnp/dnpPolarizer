
import time
import numpy as np

import sys

sys.path.append("c:/Users/benno/Dropbox/Hardware/mercuryITC")
import mercuryITC

tC = mercuryITC.temperatureControllerEthernet()

temp = tC.getSignal("mb1", "TEMP")
print "Temp: ", temp

while True:
    try:
        temp1 = tC.getSignal("mb1", "TEMP")
        print "Cryostat Temperature: ", temp1

        temp2 = tC.getSignal("db7", "TEMP")
        print "Probe Temperature: ", temp2

        print "\n"
        time.sleep(30)
        
    except KeyboardInterrupt:
            break
