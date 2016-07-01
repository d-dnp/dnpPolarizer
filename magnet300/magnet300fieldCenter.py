import matplotlib.pyplot as plt
from numpy import array
x = array(range(46))

y = array([4.86, 5.19, 5.52, 5.76, 6.01, 6.345, 6.451, 6.530, 6.595, 6.620, 6.641, 6.656, 6.661, 6.664, 6.665, 6.666, 6.666, 6.666, 6.666, 6.666, 6.666, 6.667, 6.667, 6.667, 6.667, 6.667, 6.667, 6.669, 6.669, 6.669, 6.667, 6.665, 6.660, 6.655, 6.641, 6.619, 6.579, 6.416, 6.425, 6.306, 6.136, 6.028, 5.795, 5.540, 5.148, 4.810])


lStick = 140

extensionG10 =34.5

magnetHeight = 1140
fieldCenterFromTop =  378

print "Distance from Top by Ole: ", magnetHeight - fieldCenterFromTop

distanceSensorFromTopOfMagnet = lStick - x - extensionG10

plt.plot(distanceSensorFromTopOfMagnet, y, "-bx")


plt.xlabel("Displacement")
plt.ylabel("Field")

plt.show()
