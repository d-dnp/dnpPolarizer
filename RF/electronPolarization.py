import scipy as sp
import scipy.constants as con
import matplotlib.pyplot as plt
import numpy as np

gammaE = 1.760859708e11
print con.hbar
print "Boltzmann: ", con.k
def getPolarization(B,T):
    larmorE = gammaE*B
    exponent = con.hbar*larmorE/(con.k*T)
    return 1 - (sp.exp(exponent)+1)**(-1)

def getPolarizationOrthoPara(dE,T):
    """This is a very rough approximation assuming only two levels!!"""
    exponent = -dE/(con.k*T)
    return 2.*1/(3.*sp.exp(exponent)+1.)-1.

def getPopulationAllOrthoStates(dE,T):
    exponent = -dE/(con.k*T)
    return 3*sp.exp(exponent)/(1+3*sp.exp(exponent))

def getPopulationParaState(dE, T):
    return 1 - getPopulationAllOrthoStates(dE, T)


def plotPolarizationVsTemperature(dE, T):
    global pol
    pol = [getPopulationAllOrthoStates(dE, t) for t in T]
    plt.plot(T, pol)
    plt.ylim(0.00001, 1.1)
    plt.grid()
    plt.show()

if __name__ == "__main__":
    global T
    T = np.array(range(1,300))
    plotPolarizationVsTemperature(500e9*2*sp.pi*con.hbar, np.array(range(1,300)))
