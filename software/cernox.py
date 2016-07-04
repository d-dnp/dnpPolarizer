from scipy import interpolate
import numpy as np

class cernox(object):
    """This class represents general cernox sensors
    """
    
    def __init__(self, calibrationFile):
        """
        
        Arguments:
        - `calibrationFile`: a path to a calibration file containing resistance and temperature information.
        """
        calibrationFile = calibrationFile

        data = np.loadtxt(calibrationFile)
        data = data[data[:,0].argsort(axis=0)]
        
        r = data[:, 0]
        t = data[:, 1]
        self.f = interpolate.interp1d(r, t, kind = "slinear", bounds_error = False, fill_value = 50)

    def getTemperatureFromResistance(self, R):
        """
        Arguments:
        - `R`: resistance in Ohm
        """
        return self.f(R)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    calibrationData = "./cernoxCalibration/cernox_cryostatOle.dat"
    c = cernox(calibrationData)
    data = np.loadtxt(calibrationData)
    data = data[data[:,0].argsort(axis=0)]
        
    r = data[:, 0]
    t = data[:, 1]

    # the data looks pretty linear on a loglog plot - this could probably be used for extrapolation
    #    plt.loglog(r,t, "bx")
    plt.semilogx(r,t, "bx")

    #plt.xlim([0, 100e3])
    plt.xlabel("Resistance (Ohm)")
    rNew = np.linspace(r[0], r[-1], num=1000)
    print rNew
    plt.semilogx(rNew, c.getTemperatureFromResistance(rNew), "-r")
