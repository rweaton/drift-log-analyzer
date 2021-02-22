# Do not use this version as of yet!
# It is missing some functionality compared to RadiusOfCurvatureWorkspace2.py
#   specifically:
#       pump bowl setting for Effective diameter measurement
#
# Here, a different means of filtering out convolution artifacts is attempted.
# Eventually, I intend this version to work with Python 3 using Spyder
# As of tonight, 5/9/18, it is not working.
# RE

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.transforms as mtrans
#from matplotlib.transforms import offset_copy
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.backends.backend_pdf import PdfPages

import ImportLogDataScript_Gyro as ILDS_G
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

DEPTHPLOTINC = 10.    
def FindDepthValIndices(Depths):
    
    DepthsToPlot = np.arange(0, Depths[-1], DEPTHPLOTINC)
    DepthValIndices = np.nan*np.ones_like(DepthsToPlot)
    i = 0
    # Determine indices corresponding to depth increments
    for d in DepthsToPlot:
        DepthVal, DepthValIndices[i] = minfinder(np.abs(Depths - d))
        i += 1
        
    return DepthValIndices
    
def file_save(JobID, FigPointers):
    
    import platform
    #from Tkinter import *
    from tkinter import *
    from tkFileDialog import asksaveasfile
    from matplotlib.backends.backend_pdf import PdfPages
    
    if (platform.node() == 'Darius'):
    
        WriteDir = 'f:\\DriftLogReports'
    
    elif (platform.node() == 'Xerxes'):
    
        WriteDir = '/mnt/storage/DriftLogReports'
    
    elif (platform.node() == 'thug2MacLaptop'):

        #WriteDir = '/Volumes/f/DriftLogReports'
        WriteDir = '/Volumes/F/DriftLogReports'
    
    elif (platform.node() == 'LOGGING-ROOM-PC-Linux'):
    
        WriteDir = '/media/thugwithyoyo/Darius-f/DriftLogReports'
    
    root = Tk() ; root.withdraw()
    FilterSpec = ".pdf"
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".pdf", 
        initialdir=WriteDir, filetypes=[('Save as', FilterSpec)])
        
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
        
    text2save = str(text.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.
    
    os.chdir(WriteDir)

    reportData.to_csv(JobID + 'DriftLogTabData.csv')

    pp = PdfPages(JobID + 'DriftLogReportFigs.pdf')
    
    for fp in FigPointers:
        
        pp.savefig(fp)
        
    pp.close()

    os.chdir(CodeDir)
 
CodeDir = os.getcwd()
 
# Specify directory to which AutoCAD script files are to be written.
if (os.name == 'nt'):
    
    WriteDir = 'f:\\DriftLogReports'
    
elif (os.name == 'posix'):
    
    #WriteDir = '/mnt/storage/DriftLogReports'
    WriteDir = '/Volumes/F/DriftLogReports'
     
LogDataTable = ILDS_G.ImportData()
PathArray = np.array([LogDataTable['DevComp_North'], LogDataTable['DevComp_East'], LogDataTable['DevComp_Down']])
Depths = np.array(LogDataTable['Depth'])

JobID = input('Enter an identifier for this job to be used in figure titles: ')

# Specify casing diameter (in feet!)
d_casing = 15.25/12
#d_casing = 16./12.

# Filter well path
SampFreq = 4.0  # Corresponds to a sampling interval of 0.25 feet
KernelHalfWidth = 1.5

if KernelHalfWidth != 0:
    x_fPathArray = GF.FilterSignal(PathArray[0,:], SampFreq, KernelHalfWidth)
    y_fPathArray = GF.FilterSignal(PathArray[1,:], SampFreq, KernelHalfWidth)
    z_fPathArray = GF.FilterSignal(PathArray[2,:], SampFreq, KernelHalfWidth)
    
else:
    x_fPathArray = PathArray[0,:]
    y_fPathArray = PathArray[1,:]
    z_fPathArray = PathArray[2,:]

fPathArray = np.array([x_fPathArray, y_fPathArray, z_fPathArray])

# Filter to ignore convolution margin artifact
(nElements,) = z_fPathArray.shape
Indices = np.arange(0, nElements)
EndIndex = Indices[z_fPathArray == np.max(z_fPathArray)][-1]
ValidFilter = slice(0,EndIndex+1)

fPathArray = fPathArray[:, ValidFilter]
#Depths = Depths[ValidFilter]

plt.plot(Depths, PathArray[2,:])
plt.plot(Depths[ValidFilter], fPathArray[2,:])
plt.show()

WellArcLength = WALC.WellArcLengthCalculator(Depths[ValidFilter], fPathArray)

# Calculate curvature along smoothed well path
Curvature = CC.CalculateCurvature(Depths[ValidFilter], fPathArray)

# Multiply curvature by 100 for easier units to read.
AngleOver100ft = np.degrees(100.*Curvature)

# Add curvature information to dataframe
DogLegAdd = np.nan*np.ones_like(Depths)
DogLegAdd[ValidFilter] = AngleOver100ft
LogDataTable['Dogleg'] = DogLegAdd

# Calculate clearance over well depth.
d_eff = ED.EffectiveDiameter(PathArray, d_casing)

# Add effective diameter vector to dataframe
LogDataTable['EffDiam'] = 12*d_eff


ExtractionIndices = FindDepthValIndices(Depths)

#reportData = LogDataTable[['Depth', 'DevAzimuth', 'DevInclination', 
#    'DevComp_North', 'DevComp_East', 'DevComp_Down', 
#    'Dogleg', 'EffDiam']].ix[ExtractionIndices]

#reportData = LogDataTable[['Depth', 'DevAzimuth', 'DevInclination', 
#    'DevComp_North', 'DevComp_East', 'DevComp_Down', 
#    'Dogleg', 'EffDiam']].ix[ExtractionIndices]

reportData = LogDataTable[['Depth', 'DevAzimuth', 'DevInclination', 
    'DevComp_North', 'DevComp_East', 'DevComp_Down', 
    'Dogleg', 'EffDiam']].iloc[ExtractionIndices]


#FigPointers = np.empty(7)
#FigPointers[0] = DLPFL.PlotTopViewRadial(Depths, PathArray, JobID)
#FigPointers[1] = DLPFL.PlotProjections(Depths, PathArray, JobID)
#FigPointers[2] = DLPFL.Plot3DReconstruction(Depths, PathArray, JobID)
#FigPointers[3] = DLPFL.WellStandardComparisonPlot(Depths, d_casing, PathArray, JobID)
#FigPointers[4] = DLPFL.PlotEffectiveDiameter(Depths, 12*d_eff, 12*d_casing, JobID)
#FigPointers[5] = DLPFL.ClearanceDiagram(Depths, 12*d_eff, 12*d_casing, JobID)
#FigPointers[6] = DLPFL.PlotDoglegTrace(Depths[ValidFilter], AngleOver100ft, JobID)    
            
plot1 = DLPFL.PlotTopViewRadial(Depths, PathArray, JobID)
plot2 = DLPFL.PlotProjections(Depths, PathArray, JobID)
plot3 = DLPFL.Plot3DReconstruction(Depths, PathArray, JobID)
plot4 = DLPFL.WellStandardComparisonPlot(Depths, d_casing, PathArray, JobID)
plot5 = DLPFL.PlotEffectiveDiameter(Depths, 12*d_eff, 12*d_casing, JobID)
plot6 = DLPFL.ClearanceDiagram(Depths, 12*d_eff, 12*d_casing, JobID)
plot7 = DLPFL.PlotDoglegTrace(Depths[ValidFilter], AngleOver100ft, JobID)

#os.chdir(WriteDir)
#
#reportData.to_csv(JobID + 'DriftLogTabData.csv')
#
#pp = PdfPages(JobID + 'DriftLogReportFigs.pdf')
#pp.savefig(plot1)
#pp.savefig(plot2)
#pp.savefig(plot3)
#pp.savefig(plot4)
#pp.savefig(plot5)
#pp.savefig(plot6)
#pp.savefig(plot7)
#pp.close()
#
#os.chdir(CodeDir)

#DLPFL.Plot3DReconstruction(Depths, fPathArray, JobID)
#DLPFL.PlotTopViewRadial(Depths, fPathArray, JobID)
#DLPFL.PlotProjections(Depths, fPathArray, JobID)
#DLPFL.PlotEffectiveDiameter(Depths, 12*d_eff, 12*d_casing, JobID)
#DLPFL.PlotDoglegTrace(Depths, AngleOver100ft, JobID)
#DLPFL.ClearanceDiagram(Depths, 12*d_eff, 12*d_casing, JobID)