import sys
import os
import platform
import numpy as np
import tkinter
from tkinter import filedialog

import matplotlib.pyplot as plt
#import matplotlib.transforms as mtrans
#from matplotlib.transforms import offset_copy
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_pdf import PdfPages

import ImportLogDataScript_Gyro3 as ILDS_G
import CalculateCurvature as CC
import GaussianFiltering as GF
import EffectiveDiameter as ED
import WellArcLengthCalculator as WALC
import DriftLogPlotFuncLib as DLPFL

def ismember(A, B):
    return [ np.sum(a == B) for a in A]
    
# Program to find minima
def minfinder(A):
    (nElements,) = A.shape
    Indices = np.arange(0, nElements)
    minVal = sys.float_info.max
    i = 0
    
    for a in A:
        if a < minVal:
            minVal = a
            minIndex = Indices[i]
            
        i += 1
        
    return minVal, minIndex

#### CONSTANTS ####
# Define interval that separate successive records
# in tabular report (.csv file)
DEPTHPLOTINC = 10.

# Routine to return location index of a given depth value.    
def FindDepthValIndices(Depths):
    
    DepthsToPlot = np.arange(0, Depths[-1], DEPTHPLOTINC)
    DepthValIndices = np.nan*np.ones_like(DepthsToPlot)
    i = 0
    # Determine indices corresponding to depth increments
    for d in DepthsToPlot:
        DepthVal, DepthValIndices[i] = minfinder(np.abs(Depths - d))
        i += 1
        
    return DepthValIndices
     
CodeDir = os.getcwd()

######## OUTPUT FILE HANDLING ######  
# Specify directory where final report files (csv and pdf) will be saved.
# Try to auto-detect.  If not, prompt user to specify.
if (platform.node() == 'Darius'):

    WriteDir = WriteDir = 'f:\\DriftLogReports'

elif (platform.node() == 'Xerxes'):

    WriteDir = '/mnt/storage/DriftLogReports'

elif (platform.node() == 'thug2-Mac-Laptop.local'):

    DataDir = '/Volumes/F/DriftLogReports'

elif (platform.node() == 'LOGGING-ROOM-PC-Linux'):

    WriteDir = '/media/thugwithyoyo/Darius-f/DriftLogReports'

else:
    opts = {'initialdir': CodeDir, 'title': "Select a save directory"}
    root = tkinter.Tk()
    root.withdraw()
    root.update()
    WriteDir = filedialog.askdirectory(**opts)
    root.destroy()

##### SOURCE DATA HANDLING #####
# Check to see if log dataframe has been loaded already.  If not,
# prompt user to specify and source file to import.    
if 'LogDataTable' in locals():
    print('LogDataTable has already been loaded into the kernel.')
else: 
    LogDataTable = ILDS_G.ImportData()

# Parse data columns into a 3 by N NumPy array, the argument format
# expected by subsequent subroutines to follow.    
PathArray = np.array([LogDataTable['DevComp_North'], LogDataTable['DevComp_East'], LogDataTable['DevComp_Down']])

# Insert the depth column into its own separate array.
Depths = np.array(LogDataTable['Depth'])

### BEGIN USER QUERY BLOCK ####
# User specifies general heading for figures
#JobID = raw_input('Enter an identifier for this job to be used in figure titles: ')
JobID = input('Enter an identifier for this job to be used in figure titles: ')

# Perform depth-shifting on well-depth vector and downward path vector
#DepthShift = raw_input('Enter value to depth-shift (neg. for uphole, 0.0 for none): ')
DepthShift = input('Enter value to depth-shift (neg. for uphole, 0.0 for none): ')

DepthShift = float(DepthShift)
Depths = Depths + DepthShift*np.ones_like(Depths)
PathArray[2,:] = PathArray[2,:] + Depths[0]*np.ones_like(PathArray[2,:])

# User specifies casing diameter in inches.  Convert to feet for further processing.
#d_casing = raw_input('Enter Inner Diameter (in inches) of well casing or borehole diameter: ')
d_casing = input('Enter Inner Diameter (in inches) of well casing or borehole diameter: ')
d_casing = float(d_casing)/12
#d_casing = 15.5/12

# User specifies length of pump to be inserted in well.
#PumpLength = raw_input('Enter the length of the pump to be inserted (0.0 for none): ')
PumpLength = input('Enter the length of the pump to be inserted (0.0 for none): ')

# If a zero-valued pump length given by user, set pump length
# to the bottom-most point of the log.
PumpLength = float(PumpLength)
if (PumpLength == 0.):
    PumpLength = Depths[-1]

#### BEGIN DATA PRE-PROCESSING ####
# Smooth raw drift data by convolution with a Gaussian kernel.
SampFreq = 4.0  # Corresponds to a sampling interval of 0.25 feet
#KernelHalfWidth = 5.0
KernelHalfWidth = 0

# Only perfom smoothing if kernel half-width is greater than zero.
if KernelHalfWidth != 0:
    x_fPathArray = GF.FilterSignal(PathArray[0,:], SampFreq, KernelHalfWidth)
    y_fPathArray = GF.FilterSignal(PathArray[1,:], SampFreq, KernelHalfWidth)
    z_fPathArray = GF.FilterSignal(PathArray[2,:], SampFreq, KernelHalfWidth)
    
    # Overwrite original path data with smoothed path data
    fPathArray = np.array([x_fPathArray, y_fPathArray, z_fPathArray])
    
    # Filter to ignore convolution margin artifact
    # Need to improve on this!
    (nElements,) = z_fPathArray.shape
    Indices = np.arange(0, nElements)
    StartIndex = np.floor(0.025*nElements)
    EndIndex = np.ceil(0.975*nElements)
    
else:
    x_fPathArray = PathArray[0,:]
    y_fPathArray = PathArray[1,:]
    z_fPathArray = PathArray[2,:]

    fPathArray = np.array([x_fPathArray, y_fPathArray, z_fPathArray])
    
    (nElements,) = z_fPathArray.shape
    Indices = np.arange(0, nElements)
    StartIndex = Indices[0]
    EndIndex = Indices[-1]

#EndIndex = Indices[z_fPathArray == np.max(z_fPathArray)][-1]
ValidFilter = slice(StartIndex,EndIndex+1)

fPathArray = fPathArray[:, ValidFilter]
#Depths = Depths[ValidFilter]

# Post convolution filtering check
plt.plot(Depths, PathArray[2,:])
plt.plot(Depths[ValidFilter], fPathArray[2,:])
plt.show()
##### END DATA PRE-PROCESSING #####

##### BEGIN REPORT ANALYSES ######
WellArcLength = WALC.WellArcLengthCalculator(Depths[ValidFilter], fPathArray)

# Calculate curvature along smoothed well path
Curvature = CC.CalculateCurvature(Depths[ValidFilter], fPathArray)

# Multiply curvature by 100 for easier units to read.
AngleOver100ft = np.degrees(100.*Curvature)

# Add curvature information to dataframe
DogLegAdd = np.nan*np.ones_like(Depths)
DogLegAdd[ValidFilter] = AngleOver100ft
LogDataTable['Dogleg'] = np.round(DogLegAdd, decimals=2)

# Calculate clearance over well depth.
DepthVal, DepthIndex = minfinder(np.abs(PumpLength - Depths))
DepthSlice = slice(0, DepthIndex)
d_eff = ED.EffectiveDiameter(PathArray[:, DepthSlice], d_casing)

# Add effective diameter vector to dataframe
LogDataTable['EffDiam'] = np.nan*np.ones_like(Depths)
LogDataTable['EffDiam'][DepthSlice] = np.round(12*d_eff, decimals=2)

# Format values in LogDataTable before writing to file.
LogDataTable['Depth'] = np.round(Depths, 2)
LogDataTable['DevComp_North'] = np.round(PathArray[0,:], 2)
LogDataTable['DevComp_East'] = np.round(PathArray[1,:], 2)
LogDataTable['DevComp_Down'] = np.round(PathArray[2,:], 2)

ExtractionIndices = FindDepthValIndices(Depths)

# Uses obsolete method, .ix(), of pandas dataFrame object.
# reportData = LogDataTable[['Depth', 'DevAzimuth', 'DevInclination', 
#     'DevComp_North', 'DevComp_East', 'DevComp_Down', 
#     'Dogleg', 'EffDiam']].ix[ExtractionIndices]

# Successor method, .iloc(), for extracting dataFrame records
#  by numeric integer indices.
reportData = LogDataTable[['Depth', 'DevAzimuth', 'DevInclination', 
    'DevComp_North', 'DevComp_East', 'DevComp_Down', 
    'Dogleg', 'EffDiam']].iloc[ExtractionIndices.astype(int)]

# Geneate report plots, each function returns a figure pointer.    
plot1 = DLPFL.PlotTopViewRadial(Depths, PathArray, JobID)
plot2 = DLPFL.PlotProjections(Depths, PathArray, JobID)
plot3 = DLPFL.Plot3DReconstruction(Depths, PathArray, JobID)
plot4 = DLPFL.WellStandardComparisonPlot(Depths, d_casing, PathArray, JobID)
plot5 = DLPFL.PlotEffectiveDiameter(Depths[DepthSlice], 12*d_eff, 12*d_casing, JobID)
plot6 = DLPFL.ClearanceDiagram(Depths, 12*d_eff, 12*d_casing, JobID)
plot7 = DLPFL.PlotDoglegTrace(Depths[ValidFilter], AngleOver100ft, JobID)
#### END REPORT ANALYSES ######

#### BEGIN REPORT CONSOLIDATION AND SAVE #####
# Navigate to save directory
os.chdir(WriteDir)

# Save tabulated data to a .csv file
reportData.to_csv(JobID + 'DriftLogTabData.csv')

# Initialize a pdf object for merging together 
# separate plot figures as individual pages
pp = PdfPages(JobID + 'DriftLogReportFigs.pdf')

# Insert each report plot into pdf one by one.
pp.savefig(plot1)
pp.savefig(plot2)
pp.savefig(plot3)
pp.savefig(plot4)
pp.savefig(plot5)
pp.savefig(plot6)
pp.savefig(plot7)

# Close pdf object
pp.close()

# Return to original directory of script
os.chdir(CodeDir)
###### REPORT CONSOLIDATION AND SAVE #####