#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 08:35:09 2018

@author: ryaneaton
"""
# Import NumPy
import numpy as np

# Load functions to import gyro log
import ImportLogDataScript_Gyro3 as ILDS_G

# Graphics generating libraries to import
import matplotlib.pyplot as plt
#import matplotlib.scatter as scatter
import matplotlib.patches as patches
import matplotlib.transforms as mtrans
from matplotlib.transforms import offset_copy
from mpl_toolkits.mplot3d import Axes3D

# Import drift trajectory calculation function library
import DriftPathCalcLib as DPCL

# Import gyro data
LogDataTable = ILDS_G.ImportData()

# Setup and initialize figure to be plotted
fig = plt.figure(figsize=(8,10.5))
ax = fig.add_subplot(111, projection='3d')

ASPECTRATIO = 0.8
#ax.set_aspect(ASPECTRATIO)
plt.gca().invert_zaxis()
plt.gca().invert_yaxis()

# Run average angle computation method
DelNorth, DelEast, DelTVD = DPCL.AverageAngleMethod(LogDataTable['Depth'], 
                                               LogDataTable['DevInclination'], 
                                               LogDataTable['DevAzimuth'], 
                                               AngleUnits='degrees')

# Plot AA trajectory
ax.plot(np.cumsum(DelNorth), np.cumsum(DelEast), np.cumsum(DelTVD),color='k')

# Run balanced tangential computation method
DelNorth, DelEast, DelTVD = DPCL.BalancedTangentialMethod(LogDataTable['Depth'], 
                                                     LogDataTable['DevInclination'], 
                                                     LogDataTable['DevAzimuth'], 
                                                     AngleUnits='degrees')

# Plot BT trajectory
ax.plot(np.cumsum(DelNorth), np.cumsum(DelEast), np.cumsum(DelTVD),color='c')

# Run radius of curvature computation method
DelNorth, DelEast, DelTVD = DPCL.RadiusOfCurvatureMethod(LogDataTable['Depth'], 
                                                     LogDataTable['DevInclination'], 
                                                     LogDataTable['DevAzimuth'], 
                                                     AngleUnits='degrees')

# Plot trajectory
ax.plot(np.cumsum(DelNorth), np.cumsum(DelEast), np.cumsum(DelTVD),color='r')

# Run minimum curvature computation method
DelNorth, DelEast, DelTVD = DPCL.MinimumCurvatureMethod(LogDataTable['Depth'], 
                                                     LogDataTable['DevInclination'], 
                                                     LogDataTable['DevAzimuth'], 
                                                     AngleUnits='degrees')

# Plot trajectory
ax.plot(np.cumsum(DelNorth), np.cumsum(DelEast), np.cumsum(DelTVD),color='g')




# Method: color of curve
# -----------------------------------
# AverageAngleMethod: Black
# BalancedTangentialMethod: Cyan
# RadiusOfCurvatureMethod: Red
# MinimumCurvatureMethod: Green