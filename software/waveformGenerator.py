from socket import *
import time
import decorator
from numpy import zeros, array, random, savetxt



class waveformGenerator(object):
    """This class represents the waveform generator.

    It can be used to set the DAC values and possibly start and stop the Timer for the voltage ramps.

    METHODS
    ===========================
    get(): low level communication, "private"
    set(): low level communication, "private"
    getDAC()

    setDAC()

    VARIABLES
    ===========================
    dac0
    dac1
    frequency
    """
    
    def __init__(self, address):
        """
        Initialize the class and a client

        -- address: tuple consisting of IP address and port
        """
        self.address = address
        #self.client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
        #self.client_socket.settimeout(1) #Only wait 1 second for a response

        self.dac0 = 0
        self.dac1 = 0
        self.frequency = 1000

    #this is to be used as a decorator
    def retry(howmany, *exception_types, **kwargs):
        timeout = kwargs.get('timeout', 0.0) # seconds
        @decorator.decorator
        def tryIt(func, *fargs, **fkwargs):
            for _ in xrange(howmany):
                try: return func(*fargs, **fkwargs)
                except exception_types or Exception:
                    if timeout is not None: time.sleep(timeout)
        return tryIt       
      
    @retry(5, timeout)
    def get(self, param):
        """returns a string of the value of param"""
        self.client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
        self.client_socket.settimeout(1) #Only wait 1 second for a response

        self.client_socket.sendto("G" + param, self.address)
        time.sleep(0.05)
        rec_data, addr = self.client_socket.recvfrom(2048) #Read response from arduino
        return rec_data

    def set(self, param, value):
        attempt = 0
        while attempt < 1:
            try:
                self.client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
                self.client_socket.settimeout(1) #Only wait 1 second for a response
                #//self.client_socket.connect(self.address, 5000)
                #self.client_socket.flush()
                #time.sleep(0.1)
                self.client_socket.sendto("S" + param, self.address)
                #time.sleep(0.05)
                self.client_socket.sendto(str(value), self.address)
                #time.sleep(0.5)
                print attempt
                rec_data, addr = self.client_socket.recvfrom(1024)
                print rec_data
                if rec_data != "CONFIRM":
                    print "Setting of parameter " + param + " was not confirmed!"
                    print "Response received: ", rec_data
                    raise Exception('Communication failure in dissolutionShieldModule, set')
                print "ok"
                break
            except timeout:
                attempt += 1
            except ValueError as e:
                print "Error: ", e
                print "Continuing"
            finally:
                self.client_socket.close()
                
        if attempt == 25:
            print "Comunication failure after 25 attempts"

    
    def getDAC(self):
        self.dac0 = int(self.get("DAC0"))
        self.dac1 = int(self.get("DAC1"))
        return self.dac0, self.dac1

    def setDAC(self, dac0, dac1):
        self.set("DAC0", dac0)
        self.set("DAC1", dac1)

    def rampDAC(self, target0, target1, stepsize = 50):
        def adjust(target, current, stepsize):
            if target > current + stepsize/2:
                newVal = min(current + stepsize, 4095)
            elif target < current - stepsize/2:
                newVal =  max(current - stepsize, 0)
            else:
                newVal = current
            print newVal
            return newVal
        
        while abs(target0 - self.dac0) > stepsize or abs(target1 - self.dac1) > stepsize:
            self.dac0 = adjust(target0, self.dac0, stepsize)
            self.dac1 = adjust(target1, self.dac1, stepsize)

            self.setDAC(self.dac0, self.dac1)

                
        

class waveformGeneratorSimulator(waveformGenerator):
    """This class behaves like dissolution shield but
    it generates random data rather than requiring a physical device"""

    def get(self, param):
        return str(random.rand())
        
#def getSourceMeter():
#    import sys
#    sys.path.append("~/Dropbox/Hardware/keithley")
#    import keithley2400 as keith#
#
#    sourceMeter = keith.Keithley2400(port = 9)
#    return sourceMeter

    
def calibrateWaveformGenerator(sourceMeter):
    address = ('10.1.15.232', 5000)
    wg = waveformGenerator(address)

    sourceMeter.setupVoltageMeasurement()

    dacRange = range(0, 4096, 50)
    
    output1 = zeros((3, len(dacRange)))

    for i, dac0 in enumerate([0, 2048, 4095]):
        for j, dac1 in enumerate(dacRange):
            wg.setDAC(dac0, dac1)
            #time.sleep(1)
            print "DAC1: ", dac1
            output1[i,j] = sourceMeter.read()
            print "DAC1 at i= ", str(i), ": ", str(output1[i,j])

            print output1[i,j]

    savetxt("calibrationDAC1_50.txt", output1, fmt = "%.4f")

    wg.rampDAC(0, 2048, 400)
    
    output2 = zeros((3,len(dacRange)))
    for i, dac1 in enumerate([0, 2048, 4095]):
        for j, dac0 in enumerate(dacRange):
            wg.setDAC(dac0, dac1)

            output2[i,j] = sourceMeter.read()
            print "DAC2 at i= ", str(i),  ": ", str(output2[i,j])

    savetxt("calibrationDAC0_50.txt", output2, fmt = "%.4f")

    return output1, output2

    

if __name__ == "__main__":
    # adress is .243 for cryoShield1
    address= ( '10.1.15.232', 5000) #define server IP and port

    #diss1 = dissolutionShieldSimulator(address)
    wg = waveformGenerator(address)
    

    

        
        

        
        
