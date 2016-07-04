from socket import *
import time
import decorator
from numpy import zeros, array, random



class dissolutionShield(object):
    """This class represents a dissolution Shield.
    It can poll data for the temperature and pressure sensors; the data are stored in a list and can be made available for plotting vs time.

    It can get the set points for temperature and / or pressure, the regulation mode, whether the system is ready, and the timing (for switching the valves and sending external triggers. 

    The class can set the setTemperature, the setPressure, the regulationMode.

    It can arm the shield, manually trigger a dissolution, abort a dissolution and flush the system.

    METHODS
    ===========================
    get(): low level communication, "private"
    set(): low level communication, "private"
    getTemperatureAndPressure()
    getValveList()
    getSetPressure()
    getSetTemperature()
    getReady()
    getTiming(): get the on / off times for all valves and trig out signals (see setTiming), this method is diagnostic
    clear()
    save()

    arm()
    abort()
    dissolve()
    flush(t)

    setSetTemperature(t)
    setSetPressure(p)
    setRegulation(parameter)
    setTiming(stickValveOn, stickValveOff, pushValveOn, pushValveOff, triggerOn, triggerOff)
    setValve(#valve, True/False)


    VARIABLES
    ===========================
    baseTime
    timeList
    temperatureList
    pressureList
    heaterOn

    valveList
    setPressure
    setTemperature
    regulation 
    ready
    timing
    """
    
    def __init__(self, address):
        """
        Initialize the class and a client

        -- address: tuple consisting of IP address and port
        """
        self.address = address
        self.client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
        self.client_socket.settimeout(1) #Only wait 1 second for a response

        self.heaterOn = "0"
        self.baseTime = time.time()
        self.timeList = []
        self.temperatureList = []
        self.pressureList = []                          

        self.valves = 0b0
        self.setPressure = 8
        self.setTemperature = 100
        self.regulation = "pressure"
        self.ready = False
        self.timing = [0, 3000, 800, 3000, 3000, 4000]        

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
        self.client_socket.sendto("G" + param, self.address)
        time.sleep(0.05)
        rec_data, addr = self.client_socket.recvfrom(2048) #Read response from arduino
        return rec_data

    def set(self, param, value):
        attempt = 0
        while attempt < 5:
            try:
                self.client_socket.sendto("S" + param, self.address)
                #time.sleep(0.05)
                self.client_socket.sendto(str(value), self.address)
                time.sleep(0.5)
                rec_data, addr = self.client_socket.recvfrom(2048)
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

        if attempt == 5:
            print "Comunication failure after 5 attempts"

    
    def getTemperatureAndPressure(self):
        T = float(self.get("T"))
        time.sleep(0.05)
        P = float(self.get("P"))
        #print "T: ", T
        #print "P: ", P
        self.timeList.append(time.time() - self.baseTime)
        self.temperatureList.append(T)
        self.pressureList.append(P)
        #print "Pressure List: ", self.pressureList

    def getHeaterStatus(self):
        self.heaterOn = self.get("HEATERSTATUS")

    def getValves(self):
        self.valves = int(self.get("V"))
    
    def getRegulation(self):
        self.regulation = self.get("REG")
    
    def getSetPressure(self):
        self.setPressure = float(self.get("PSET"))        

    def getSetTemperature(self):
        self.setTemperature = float(self.get("TSET"))

    def getReady(self):
        pass

    def getTiming(self):
        pass

    def clear(self):
        self.baseTime = time.time()
        self.timeList = array()
        self.temperatureList = array()
        self.pressureList = array()

    def save(self):
        pass

    def arm(self):
        pass

    def abort(self):
        pass

    def dissolve(self):
        pass

    def flush(self, time = 5):
        pass

    def setSetTemperature(self, t):
        self.setTemperature = t
        self.set("TSET", t)

    def setSetPressure(self, p):
        self.setPressure = p
        self.set("PSET", p)
        
    def setRegulation(self, parameter):
        self.regulation = parameter
        self.set("REG", parameter)

    def setTiming(self, stickValveOn, stickValveOff, pushValveOn, pushValveOff, triggerOn, triggerOff):
        self.timing = [stickValveOn, stickValveOff, pushValveOn, pushValveOff, triggerOn, triggerOff]
        #now send values to Arduino


    def toogleValve(self, valve):
        self.valves ^= 2**(valve -1)

        print "Valves: ", bin(self.valves)
        self.setValves()
        
        
    def setValves(self):
        self.set("V", self.valves)
        #now send values to Arduino
        

class dissolutionShieldSimulator(dissolutionShield):
    """This class behaves like dissolution shield but
    it generates random data rather than requiring a physical device"""

    def get(self, param):
        return str(random.rand())
        


if __name__ == "__main__":
    # adress is .243 for cryoShield1
    address= ( '10.1.15.250', 5000) #define server IP and port

    #diss1 = dissolutionShieldSimulator(address)
    diss = dissolutionShield(address)
    

    

        
        

        
        
