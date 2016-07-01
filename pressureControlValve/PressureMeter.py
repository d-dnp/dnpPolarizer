# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:39:50 2013

@author: 
"""

import serial
import time
import numpy as np
import matplotlib.pyplot as plt

def getStatus(port):
    print("This is the serial number of the port.")
    print("The port to look at is {0}".format(port))
    
    ser = serial.Serial(port, baudrate=9600, stopbits=serial.STOPBITS_ONE,timeout=1)    
    #ser = serial.Serial(port, timeout=1)
    setValue(ser,'JC')
#    print("The device we talk to is " + getValue(ser, "GSN"))

    serialNumber = getValue(ser, "GSN")
    print("The serial number is " + serialNumber)
    print("The set point value is " + getValue(ser, "R1"))
    
    setValue(ser,'L1')
    setValue(ser,'V0.00')
    #'T1x' When x=1, the set-point type is pressure.
    setValue(ser,'T11')
    
#    setValue(ser,'V100.00')
    #set range of valve connected to port 1
    setValue(ser, 'N110')
  
    #set range of valve connected to port 2
#    setValue(ser, 'N21000')


    #Auto select CDG1 or CDG2 for best resolution    
      


    print("The set point type is " + getValue(ser, "R26"))
    #Used to program a value for set point xx.xx is any number between 0.00 and 100.00, representing the % of gauge full scale
    setValue(ser,'S100.10')
    setValue(ser,'V100.00')
    setValue(ser,'D1')
    print("The set point value is " + getValue(ser, "R1"))
    print("The current pressure is " + getValue(ser, "R5"))
    print("Requests full scale range of CDG1 " + getValue(ser, "RN1"))
    
 
    
    print("The current pressure is " + getValue(ser, "R5"))

    return ser
#    setValue(ser,'O')
#    print("The valve is OPEN now")
#    print("The current valve position : " + getValue(ser, "R6"))
#    time.sleep(1)
#    setValue(ser,'C')
#    print("The valve is closed now")
#    time.sleep(2)
#    setValue(ser,'V50.00')
#    print("The valve is Half Open/Closed now")
#    print("The current valve position : " + getValue(ser, "R6"))
#    time.sleep(0.3)
#    setValue(ser,'V0.00')
  
  
#    print("Range of Gauge1 = " + getValue(ser, "RN1"))
#    print("Range of Gauge2 = " + getValue(ser, "RN2"))

#    setValue(ser,'RESET') 
#    print("Software version " + getValue(ser, "R38"))
#    setValue(ser,'T11')
#    print("Report set point type " + getValue(ser, "R26"))
#    ser.close()


def initialize(port):
    ser = serial.Serial(port, baudrate=9600, stopbits=serial.STOPBITS_ONE,timeout=1)    

    setValue(ser,'JC')
    #    print("The device we talk to is " + getValue(ser, "GSN"))
    getValue(ser, "")
    serialNumber = getValue(ser, "GSN")
    print("The serial number is " + serialNumber)
    print("The set point value is " + getValue(ser, "R1"))

    setValue(ser, "N11000")
    
    
    setValue(ser, "N210")
    
    setValue(ser, "O")
    time.sleep(1)
    setValue(ser, "C")    
    
    print "Setting Device to pressure control mode"
    setValue(ser, "T11")
    
    #print "Setting Device to manual control mode"
    #setValue(ser, "T10")    
    
    range1 = getValue(ser, "RN1")
    print "Range1: ", range1
    
    range2 = getValue(ser, "RN2")
    print "Range2: ", range2
    
    return ser
    
def setValue(ser, string):
    ser.write(string+"\r\n")
    string = ser.readline().rstrip()
    time.sleep(0.3)
    print(string)
    return string

def getValue(ser, string):
    ser.write(string+"\r\n")
#       ser.write(string+"\r")
    time.sleep(0.3)
    string = ser.readline().rstrip()
    return string  
    
#getStatus(4)

def poll(ser):
    val = getValue(ser, "R5")
    #reading is in percent of 1000 torr
    p = float(val[1:])/100*1000/750.06168
    
    print("The current pressure is {:.4f} mbar".format(p*1000))
    return p

def autoPoll(ser):
    count = 0
    while True:
        try:
            print "Minutes passed: ", count/12.
            count = count + 1
            poll(ser)
            time.sleep(5)
        except KeyboardInterrupt:
            break


def vapourPressureFromTemperature(T, unit = "Pa"):
    """This function calculates the vapour pressure of helium at a given temperature, based on the Clausius-Clapeyron law."""
    p1dict  = {"Pa" : 10000, "bar" : 1, "Torr" : 770}
    T1 = 4.2
    deltaH = 84.5 #enthalpy of vapourization in J/mol
    R = 8.3145 #gas constant, in J/(mol*K)
    p2 = p1dict[unit]*np.exp(deltaH/R*(1/T1 - 1/T)) 

    return p2
    

def sweepPressure(ser):
    #vary the pressure in time, useful for calibration of temperature sensors.

    print "Setting Device to pressure control mode"
    setValue(ser, "T11")

    timeStart = time.time()
    delay = 3*60

    temperatures = np.linspace(1.3, 4.2, num=20)

    temperatures = np.array([1.5,1.6,1.7,1.8,1.9,2,2.1])

    pressures = vapourPressureFromTemperature(temperatures, unit = "Torr")

    print "Pressures: ", pressures
    #base pressure of the system is approximately 5 mbar. Take some overhead and start from 1 mbar.

    oldIndex = 0
    
    while True:
        index = np.round((time.time() - timeStart)/delay - 0.5)

        if index > len(pressures) - 1:
            break
        
        try:
            if index != oldIndex:
                pressure = pressures[index]
                print "Setting set to  point {:.2f} Torr".format(pressure)
                setValue(ser, "S1{:.2f}".format(100*pressure/1000))#1000 Torr is full scale
                time.sleep(1)
                print "Value of set point: ", getValue(ser, "R1")
                time.sleep(1)
                setValue(ser, "D1")
                oldIndex = index
                         
            #print "Minutes passed: ", count
            #count = count + 1
            print "Time passed: ", time.time() - timeStart
            poll(ser)
            time.sleep(10)
        except KeyboardInterrupt:
            print "Keyboard Interrupt, closing serial interface."
            ser.close()
            break
    

    
    
    

if __name__ == "__main__":
    ser = getStatus(3)
    sweepPressure(ser)
    count = 0


def somethingElse():    
    while True:
        try:
            print "Minutes passed: ", count
            count = count + 1
            poll(ser)
            time.sleep(5)
        except KeyboardInterrupt:
            print "Keyboard Interrupt, closing serial interface."
            ser.close()
            break

    #ser.close()
