from socket import *
import time
from numpy import zeros, array, random



class cryoShield(object):
    """This class represents a cryoShield.
    It can poll data for the three Allen-Bradley lines as well as fora Cernox sensor.

    Additionally it can configure the AD7794 gain and set the dwell time between points.

    Maybe we want to use it to update the LCD Display as well.
    """
    
    def __init__(self, address, cernoxCalibrationFile = ""):
        """
        Initialize the class and a client

        -- address: tuple consisting of IP address and port
        """
        self.address = address
        self.client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
        self.client_socket.settimeout(3) #Only wait 1 second for a response
        self.currentData = {"AB1": [], "AB2": [], "AB3": [], "CERNOX": []}

        #part of the data below is redundant - make sure it is the same as in the Arduino Firmware!
        self.gainAB = 32
        self.gainCERNOX = 128
        self.dataLength = 100
        self.dwellTime = 10e-3
        self.referenceVoltage = 1.17

        self.currentCernox = 4e-6
        self.currentAB = 10e-6

        #dimensions offered by this class
        self.ABxDim = ["Time (s)", "Time (m)", "Time (h)"]
        self.AByDim =  ["Digitizer Level (%)", "Voltage (mV)", "Resistance (Ohm)", "Resistance (kOhm)"]

        self.ABxConversion = array([1, 1./60, 1./3600])
        self.AByConversion = array([1,
                    1./self.gainAB*self.referenceVoltage*1000,
                    1./self.gainAB*self.referenceVoltage/10e-6,
                    1./self.gainAB*self.referenceVoltage/10e-6/1000])
               
        self.cernox_xDim = self.ABxDim
        self.cernox_yDim =  ["Digitizer Level (%)", "Voltage (mV)", "Resistance (Ohm)", "Resistance (kOhm)", "Temperature (K)"]

        #temperature will not work this way since it is not linear!
        self.cernox_xConversion = self.ABxConversion
        self.cernox_yConversion = array([1,
                    1./self.gainCERNOX*self.referenceVoltage*1000,
                    1./self.gainCERNOX*self.referenceVoltage/4e-6,
                    1./self.gainCERNOX*self.referenceVoltage/4e-6/1000,
                    1]) 
    
        #standard configuration:
        self.ABxDimIndex = 0
        self.AByDimIndex = 0

        self.cernox_xDimIndex = 0
        self.cernox_yDimIndex = 0
        
        
    def readShieldData(self, channel):
        #maybe split this routine in two 
        responseArray = zeros(self.dataLength)
        self.client_socket.sendto(channel, self.address)

        time.sleep(self.dataLength*self.dwellTime)
        if channel[0] == "A": time.sleep(1) #wait longer for Allen-Bradley due to the heat pulse
            
        for i in range(self.dataLength):
            #print "i: ", i
            rec_data, addr = self.client_socket.recvfrom(2048) #Read response from arduino
            rec_data = rec_data.rstrip(",")
            responseArray[i] = int(rec_data) #Convert string rec_data to float temp

        return responseArray
        

    def pollChannel(self, channel, xDim = 0, yDim = 0):
        """
        Poll a channel on the AD7794.

        -- String channel: AB1, AB2, AB3 or CERNOX
        -- int xDim: index describing x dimensino
        -- int yDim: index describing yDimension
        """
        responseArray = self.readShieldData(channel)
        xAxis = array(range(self.dataLength))*self.dwellTime

        self.currentData[channel] = responseArray

        yAxis = responseArray/float(0xffffff)
        
        if channel[0] == "A":
            xAxis *= self.ABxConversion[xDim]
            yAxis *= self.AByConversion[yDim]

        if channel[0] == "C":
            xAxis *= self.cernox_xConversion[xDim]
            yAxis *= self.cernox_yConversion[yDim]

        print "yAxis: ", yAxis
            
        return xAxis, yAxis

class cryoShieldSimulator(cryoShield):
    """This class behaves like cryoShield but
    it generates random data rather than requiring a phyiscal device"""

    def readShieldData(self, channel):
        return 0xffffff*random.rand(self.dataLength)


    
if __name__ == "__main__":
    address= ( '10.1.15.243', 5000) #define server IP and port

    cS1 = cryoShield(address)
    print(cS1.pollChannel("AB1"))
    print(cS1.pollChannel("AB2"))
    print(cS1.pollChannel("AB3"))
