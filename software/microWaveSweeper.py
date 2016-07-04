import microWave as mW
import dissolutionShield as dS
import time
import numpy as np
reload(mW)


diss = dS.dissolutionShield(("10.1.15.250", 5000))

#Trigger command: diss.set("TRIG", 1)

micro = mW.microWaveSource()
micro.setPower(50)
micro.setFrequency(188000)
micro.switchOn()

frequency = np.linspace(187500, 188500, num = 41)
print frequency

raw_input("Start Pulse Programm with 41 experiments and press enter when waiting for Trigger.")

print "Noise Scan"
micro.setFrequency(187500)
diss.set("TRIG", 1)
time.sleep(80)

for i, f in enumerate(frequency):
    print "Point ", i, "/41"
    micro.setFrequency(f)
    diss.set("TRIG", 1)
    time.sleep(80)

print "Complete."

