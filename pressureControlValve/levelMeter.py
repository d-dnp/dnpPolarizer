import serial
import time
import numpy as np
import matplotlib.pyplot as plt

def getStatus(port):
    print("This is the status report of levelMeter.")
    print("The port to look at is {0}".format(port))
    
    ser = serial.Serial(int(port), baudrate=9600, stopbits=serial.STOPBITS_TWO,timeout=1)    
    #ser = serial.Serial(port, timeout=1)
    
    print("The device we talk to is " + getValue(ser, "V"))

    HeLevel = getValue(ser, "R1")
    HeLevel = HeLevel[-4:-1] + "." + HeLevel[-1]
    print("The level of the He channel  is " + HeLevel + "%")

    NLevel = getValue(ser, "R2")
    NLevel = NLevel[-4:-1] + "." + NLevel[-1]
    print("The level of the N channel  is " + NLevel + "%")

    ser.close()

    return HeLevel, NLevel

def logLevels(port, interval):
    HeLevelList =[]
    NLevelList = []
    
    global xRange
    if interval == 3600:
        xLabel = "Time (h)"
    elif interval == 3600*24:
        xLabel = "Time (d)"
    elif interval == 60:
        xLabel = "Time (m)"

    totalTime = 0
    count = 0
    while True:
        count += 1
        HeLevel, NLevel = getStatus(port)
        print "LogTime: " + str(totalTime) + ", HeLevel: " + HeLevel + "%, NLevel: " + NLevel + "%"
        HeLevelList.append(float(HeLevel))
        NLevelList.append(float(NLevel))
        totalTime = totalTime + interval
        xRange = np.array(range(count))#0, totalTime/interval, totalTime/interval)
        plt.close()
        plt.plot(xRange, np.array(HeLevelList), "-x")
        plt.plot(xRange, np.array(NLevelList), "-x")
        plt.xlabel(xLabel)
        plt.ylabel("Level (%)")
        plt.legend(["He Level", "N Level"])
        plt.savefig("level.pdf")
        np.savetxt("level.txt", zip(xRange, HeLevelList, NLevelList), fmt="%.1f")

        time.sleep(interval)

def setRemote(ser):
    setValue(ser, "C3")

def setLocalLocked(ser):
    setValue(ser, "C0")

def setValue(ser, string):
    ser.write(string+"\r")
    string = ser.readline().rstrip()
    #print(string)
    return string

def getValue(ser, string):
    ser.write(string+"\r")
    time.sleep(0.3)
    string = ser.readline().rstrip()
    return string    

def getSerial(port):
    ser = serial.Serial(int(port), baudrate=9600, stopbits=serial.STOPBITS_TWO,timeout=1)
    return ser

def closeSerial(ser):
    ser.close()

def check(ser):
    goToSet(ser)
    time.sleep(10)
    goToZero(ser)


def alarm(string):
    print("="*20 + " ! ERROR! " + "="*20)
    print(string)
    print("Refer to the IPS-120-10-Manual, p. 33ff to see what this means")
    print("="*50)

if __name__ == "__main__":
    #getStatus(0)
    logLevels(0,3600*24)
