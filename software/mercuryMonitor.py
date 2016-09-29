
import time
import numpy as np

import sys

sys.path.append("c:/Users/benno/Dropbox/Hardware/mercuryITC")
import mercuryITC

tC = mercuryITC.temperatureControllerEthernet()

temp = tC.getSignal("mb1", "TEMP")
print "Temp: ", temp

logfilename = "201609xxlog.txt"
logfile = open(logfilename, "w")
logfile.write("Time \t  T Cryostat \t T Sample\n======================================")
logfile.close()

while True:
    try:
        print time.time()
        
        temp1 = tC.getSignal("mb1", "TEMP")
        print "Cryostat Temperature: ", temp1

        temp2 = tC.getSignal("db7", "TEMP")
        print "Probe Temperature: ", temp2

        print "\n"

        logfile = open(logfilename, "a")
        logfile.write("\n" + str(time.time()) + "\t" + str(temp1) + "\t" + str(temp2))
        logfile.close()

        time.sleep(30)
        
    except KeyboardInterrupt:
            break
