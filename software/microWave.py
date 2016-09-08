import serial
import numpy
import time

class microWaveSource(object):
    """This class represents the ELVA microwave source"""

    def __init__(self, port = 2, type = 188):
        """Initialize a serial interface to the source.

        - port: Number of the port, e.g., 2 for COM3
        - type of the source: Currently only 188 is supported."""
        self.ser = serial.Serial(port = port, baudrate = 115200, timeout = 0.02)
        self.type = type
        self.frequency = 0
        self.power = 0
        self.isOn = False

    def readline(self):
        """We need a custom readline to read staff up to the hash key."""
        out = ""
        while True:
            out += str(self.ser.read(1))
            if out != "":
               while out[-1] != "#":
                     out += str(self.ser.read(1))
               return out
            else:
               return ""

    def dafOn(self):
        """Use this to switch frequency stabilization mode off, i.e. direct frequency control."""
        time.sleep(0.5)
        self.ser.write("@DAF!on#")
        time.sleep(0.5)
        ans = self.readline()
        print ans

    def dafOff(self):
        """Use this to switch frequency stabilfization mode on, i.e. no direct frequency control."""
        time.sleep(0.5)
        self.ser.write("@DAF!off#")
        time.sleep(0.5)
        ans = self.readline()
        print ans

            
        
    def switchOn(self):
        time.sleep(0.1)
        self.ser.write("@U27!on#")
        time.sleep(0.1)
        ans = self.readline()
        while ans[-3:-1] != 'on':
            self.ser.write("@U27!on#")
            time.sleep(0.1)
            ans = self.readline()
            print "openning Microwave"

        print "Microwave on"
        
                    
    def switchOff(self):
        time.sleep(0.1)
        self.ser.write("@U27!off#")
        time.sleep(0.1)
        ans = self.readline()
        while ans[-4:-1] != "off":
            self.ser.write("@U27!off#")
            time.sleep(0.1)
            ans = self.readline()
            print "closing Microwave"

        print "Microwave off"

    def setFrequency(self, frequency):
        """Set the frequency of the source.

        - frequency: float, frequency in MHz."""
        if self.type == 188:
            if frequency > 187499.99 and frequency < 188500.01:
                attempt = 0
                while attempt < 10:
                    try:
                        attempt += 1
                        self.ser.write("@FRQ!{:.2f}#".format(frequency))
                        ans = self.readline()
                        if float(ans[5:-1]) == frequency:
                            self.frequency = frequency
                            break
                        else:
                            raise Exception('Frequency not set')
                    except:
                        pass
                        #print "Frequency not set in attempt", attempt
                        
                    if attempt == 10:
                        print "Frequency not set in 10 attempts!: "

    def getFrequency(self):
        """
        get the current frequency (i.e. for voltage calibration.
        """

        attempt = 0
        while attempt < 10:
            try:
                attempt += 1
                time.sleep(0.05)
                self.ser.write("@FRC?#")
                ans = self.readline()
                if float(ans[5:-1]) > 100:
                    break
                else:
                    print ans
            except:
                pass
            
        print ans
        return ans[5:-1]

    def getVCO(self):
        """
        get the current frequency (i.e. for voltage calibration.
        """

        attempt = 0
        while attempt < 10:
            try:
                attempt += 1
                time.sleep(0.05)
                self.ser.write("@VCO?#")
                ans = self.readline()
                if float(ans[5:-1]) > 0:
                    break
                else:
                    print ans
            except:
                pass
            
        print ans
        return ans[5:-1]


        
    def setPower(self, power):
        """Set the power of the source.

        - power: float, power in mW."""
        if self.type == 188:
            if power >= 0 and power <= 50:
                attempt = 0
                while attempt < 10:
                    attempt += 1
                    try:
                        self.ser.write("@PWR!0{:.1f}#".format(power))
                        ans = self.readline()
                        if float(ans[5:-1]) == power:
                            self.power = power
                            break
                        else:
                            print "Power not set: ", ans
                    except:
                        print "Error setting power."
                if attempt == 10:
                    print "Power not set in 10 attempts!"
                    

    def sweep(self, start, stop, points, delay=0.001):
        freqPoints = numpy.linspace(start, stop, num = points)
        pos = 0
        count = 1
        tStart = time.time()
        while True:
            try:
               freqThis = freqPoints[pos]
               self.setFrequency(freqThis)
               time.sleep(delay)
               count += 1
               if count > len(freqPoints):
                   count = 0
                   print "Sweep done, ", time.time() - tStart
            except KeyboardInterrupt:
                break

    def close(self):
        self.ser.close()


def calibrationUsingKeithley():
    import sys
    import time
    sys.path.append("../../../Hardware/keithley/")
    import keithleyBM as keithley
    reload(keithley)
    
    k = keithley.Keithley2400(9)
    k.setSourceFunc()
    k.setComplianceCurrent(curr = 100)

    global source
    
    source = microWaveSource()
    try:
        source.dafOn()
        source.switchOn()
        source.setPower(10)
    except:
        print "failed"
        source.close()
        k.close()
        
    global vapp, vvco, freq
    
    vapp = numpy.linspace(0, 20.65)
    vvco = numpy.zeros(len(vapp))
    freq = numpy.zeros(len(vapp))

    for i, v in enumerate(vapp):
        k.switchVoltage(v)
        time.sleep(1)
        vvco[i] = float(source.getVCO())
        freq[i] = float(source.getFrequency())

    numpy.savetxt("mWcalibration_curr100.txt", zip(vapp, vvco, freq), fmt = "%.4f")
    
    k.switchVoltage(0)
    k.outputOff()
    k.close()
    source.switchOff()
    source.dafOff()
    source.close()

