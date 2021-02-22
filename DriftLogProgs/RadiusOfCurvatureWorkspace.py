import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import CalcRadiusOfCurvature as CROC
import WellPathIntegrator as WPI
import ImportLogDataScript_Gyro as ILDSG

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

LogDataTable = ILDSG.ImportData()

angles = np.arange(0,8*np.pi, 0.02)

TestArray = np.array([3*np.cos(angles), 2*np.sin(angles), -5.*angles])
dTestArray = np.diff(TestArray)

#plt.plot(TestArray[0,:], TestArray[1,:], TestArray[2,:])

#WellPathArray = WPI.WellPathIntegrator(dTestArray.transpose())
CompArray = np.array([np.array(LogDataTable['DevComp_North']), 
    np.array(LogDataTable['DevComp_East']),
    np.array(LogDataTable['DevComp_Down'])])
    
WellPathArray = WPI.WellPathIntegrator(CompArray.transpose())

angles, radii = CROC.CalcRadiusOfCurvature(TestArray.transpose(), 50)
