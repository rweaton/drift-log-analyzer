import sys
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.scatter as scatter
import matplotlib.patches as patches
import matplotlib.transforms as mtrans
from matplotlib.transforms import offset_copy
from mpl_toolkits.mplot3d import Axes3D

# Global parameters
SCALEINC = 5
DEPTHPLOTINC = 50
LABELOFFSET=0.05

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

def FindPlotBound(fPathArray):
    
    PlotBound = max(np.max(np.abs(fPathArray[0,:])), np.max(np.abs(fPathArray[1,:])))
    PlotBound = np.ceil(PlotBound/SCALEINC)*SCALEINC
    
    return PlotBound

def FindDepthValIndices(Depths):
    
    DepthsToPlot = np.arange(0, Depths[-1], DEPTHPLOTINC)
    DepthValIndices = np.nan*np.ones_like(DepthsToPlot)
    i = 0
    # Determine indices corresponding to depth increments
    for d in DepthsToPlot:
        DepthVal, DepthValIndices[i] = minfinder(np.abs(Depths - d))
        i += 1
        
    return DepthValIndices.astype(int)
    
def CalcRadialDrift(fPathArray):
    
    RadialDrift = np.linalg.norm(fPathArray[0:2,-1])
        
    return RadialDrift
        
def Plot3DReconstruction(WellArcLength, fPathArray, JobID):
    # Perform 3D plot of well path
    ASPECTRATIO = 1.5
    LABELDIR = (-fPathArray[1,-1], -fPathArray[0,-1], 0)
    FONTSIZE = 16
    FONTWEIGHT = 'bold'
    
    (nComponents, nElements) = fPathArray.shape

    PlotBound = FindPlotBound(fPathArray)

    fig = plt.figure(figsize=(8,10.5))
    fig.suptitle(JobID + '\nThree Dimensional Plot of Well Geometry', fontsize=18)
        
    ax = fig.add_subplot(111, projection='3d')

    trans_offset = mtrans.offset_copy(ax.transData, fig=fig, 
        x=LABELOFFSET, y=LABELOFFSET, units='inches')
    
    # Plot well path 
    ax.plot(fPathArray[0,:], fPathArray[1,:], fPathArray[2,:], 
        linewidth=2, color='b', label='well path')

    # Plot plumb line
    ax.plot(np.array([0,0]), np.array([0,0]), np.array([0,fPathArray[2,-1]]), 
        'k-', label='plumb line')

    # Plot N-S and E-W axes
    ax.plot([-PlotBound, PlotBound], [0, 0], [0, 0], 'k--')
    ax.text(PlotBound, 0, 0, 'N', fontsize=FONTSIZE, fontweight=FONTWEIGHT)
    ax.text(-PlotBound, 0, 0, 'S', fontsize=FONTSIZE, fontweight=FONTWEIGHT)

    ax.plot([0, 0], [-PlotBound, PlotBound], [0, 0], 'k--')
    ax.text(0, PlotBound, 0, 'E', fontsize=FONTSIZE, fontweight=FONTWEIGHT)
    ax.text(0, -PlotBound, 0, 'W', fontsize=FONTSIZE, fontweight=FONTWEIGHT)
    
    # Set plot bounds
    ax.set_xlim(-PlotBound, PlotBound)
    ax.set_ylim(-PlotBound, PlotBound)

    # Add axes labels
    ax.set_xlabel('Northward drift (ft.)')
    ax.set_ylabel('Eastward drift (ft.)')
    ax.set_zlabel('True Vertical Depth (ft.)')
    
    DepthValIndices = FindDepthValIndices(fPathArray[2,:])
    
    # Plot labels and vector components       
    for i in DepthValIndices:
    
        # Add i label
        ax.text(fPathArray[0,i], fPathArray[1,i], fPathArray[2,i], 
            str(WellArcLength[i].round(3)), LABELDIR, color='cyan', 
            transform=trans_offset)
            
        # Add i datapoint
        ax.scatter(fPathArray[0,i], fPathArray[1,i], fPathArray[2,i], 
        '.', color='cyan')
        
        # Add i radial vector
        ax.plot([0,fPathArray[0,i]],[0, fPathArray[1,i]],[fPathArray[2,i],fPathArray[2,i]], 'k-')
        ax.plot([0,fPathArray[0,i]],[0, 0],[fPathArray[2,i],fPathArray[2,i]], 'k--')
        ax.plot([0,fPathArray[0,i]],[fPathArray[1,i], fPathArray[1,i]],[fPathArray[2,i],fPathArray[2,i]], 'k--')
        ax.plot([0, 0],[0, fPathArray[1,i]],[fPathArray[2,i],fPathArray[2,i]], 'k--')
        ax.plot([fPathArray[0,i],fPathArray[0,i]],[0, fPathArray[1,i]],[fPathArray[2,i],fPathArray[2,i]], 'k--')
                
    # Set up label for well depth datapoints to show up in legend.
    ax.scatter(np.nan, np.nan, np.nan, '.', color='cyan', label='well depth')
    
    # Plot bottom arc length
    ax.text(fPathArray[0,-1], fPathArray[1,-1], fPathArray[2,-1], 
        str(WellArcLength[-1].round(2)), LABELDIR, color='red', transform=trans_offset)

    # Plot drift vector at bottom
    ax.plot(np.array([0, fPathArray[0,-1]]), 
        np.array([0, fPathArray[1,-1]]), 
        np.array([fPathArray[2,-1], fPathArray[2,-1]]), 'r-', label='bottom drift')
        
    ax.scatter(fPathArray[0,-1], fPathArray[1,-1], fPathArray[2,-1], '.', color='red')
    
    # Calculate magnitude of bottom drift length
    #RadialDrift = np.linalg.norm(fPathArray[0:2,-1])
    RadialDrift = CalcRadialDrift(fPathArray)
    ax.text(0.5*fPathArray[0,-1],0.5*fPathArray[1,-1], fPathArray[2,-1], 
        str(np.round(RadialDrift, 2)), (fPathArray[0,-1],fPathArray[1,-1],0), 
        color='red', transform=trans_offset)

    #ax.set_aspect('auto')
    plt.axes(ax)
    #plt.legend(loc='lower left', bbox_to_anchor=(-0.25, -0.10, 1.25, 0.102), ncol=4, 
    #    mode='expand', fontsize=10)
    #plt.legend(loc='best', fontsize=10)
    #plt.gca().set_aspect(ASPECTRATIO)
    plt.gca().invert_zaxis()
    plt.gca().invert_yaxis()
    plt.show()
    
    return fig
    
def PlotTopViewRadial(WellArcLength, fPathArray, JobID):

    #LABELDIR = (-fPathArray[1,-1], -fPathArray[0,-1])
    FONTPOINTS = 20
    VERTICALOFFSET = -0.05
     
    fig = plt.figure(figsize=(8,10.5))
    fig.suptitle(JobID + '\nRadial Plot of Well Geometry (top-view)', fontsize=18)
    ax = plt.subplot(111, projection='polar')
    pos1 = ax.get_position() # get the original position 
    pos2 = [pos1.x0, pos1.y0 + VERTICALOFFSET,  pos1.width, pos1.height] 
    ax.set_position(pos2) # set a new position
    
    trans_offset = mtrans.offset_copy(ax.transData, fig=fig, 
        x=LABELOFFSET, y=LABELOFFSET, units='inches')
    
    trans_offset2 = mtrans.offset_copy(ax.transData, fig=fig,
        x=-0.5*FONTPOINTS, y=-0.5*FONTPOINTS, units='points')
        
    angles = np.arctan2(fPathArray[1,:], fPathArray[0,:])
    radii = np.linalg.norm(fPathArray[0:2,:], axis=0)
    
    PlotBound = FindPlotBound(fPathArray)
    ax.plot(angles, radii, linewidth=2.0, label='well path')
    ax.set_rmax(PlotBound)
    
    DepthValIndices = FindDepthValIndices(fPathArray[2,:])
    
    for i in DepthValIndices:
    
        # Add i label
        ax.text(angles[i], radii[i], 
            str(WellArcLength[i].round(2)), color='cyan', transform=trans_offset)
        
        # Add i radial vector
        #ax.plot([0,angles[i]],[0, radii[i]], 'k-')
        ax.plot(angles[i], radii[i], '.', color='cyan')
    
    ax.plot(np.nan, np.nan, '.', color='cyan', label='well depth')
        
    ax.plot([0, angles[-1]], [0, radii[-1]], color='red', label='bottom drift')
    ax.text(angles[-1], 0.5*radii[-1], str(np.round(radii[-1], 2)), 
        rotation=str(angles[-1]), color='red', transform=trans_offset)
    
    ax.set_aspect(1)
    TickList = np.arange(0,PlotBound,1)[1:]
    ax.set_rticks(TickList)
    ax.text(np.radians(0), 1.1*PlotBound, str('N'), fontsize=FONTPOINTS, 
        fontweight='bold', transform=trans_offset2)
    ax.text(np.radians(90), 1.1*PlotBound, str('E'), fontsize=FONTPOINTS, 
        fontweight='bold', transform=trans_offset2)
    ax.text(np.radians(180), 1.1*PlotBound, str('S'), fontsize=FONTPOINTS, 
        fontweight='bold', transform=trans_offset2)
    ax.text(np.radians(270), 1.1*PlotBound, str('W'), fontsize=FONTPOINTS, 
        fontweight='bold', transform=trans_offset2)
    
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    
    plt.axes(ax)
    #plt.legend(loc='lower left', bbox_to_anchor=(-0.25, -0.10, 1.25, 0.102), ncol=4, 
    #    mode='expand', fontsize=10)
    plt.legend(loc='best', fontsize=10)
    plt.show()
    
    return fig
    
def PlotProjections(WellArcLength, fPathArray, JobID):
    FONTPOINTS = 10

    PlotBound = FindPlotBound(fPathArray)

    fig = plt.figure(figsize=(10.5,8))
    fig.suptitle(JobID + '\nWell Geometry Projected on N-S & E-W Planes', fontsize=18)
    ax1 = fig.add_subplot(121)
    ax1.grid(True)
    ax2 = fig.add_subplot(122)
    ax2.grid(True)

    trans_offset1 = mtrans.offset_copy(ax1.transData, fig=fig, 
        x=5, y=-FONTPOINTS, units='points')
    
    trans_offset2 = mtrans.offset_copy(ax2.transData, fig=fig, 
        x=5, y=-FONTPOINTS, units='points')
        
    trans_offset3 = mtrans.offset_copy(ax1.transData, fig=fig, 
        x=0, y=FONTPOINTS, units='points')
        
    trans_offset4 = mtrans.offset_copy(ax2.transData, fig=fig, 
        x=0, y=FONTPOINTS, units='points')     
    
    # Plot well path 
    ax1.plot(fPathArray[0,:], fPathArray[2,:], linewidth=2, color='b', label='well path')
    ax2.plot(fPathArray[1,:], fPathArray[2,:], linewidth=2, color='b')

    # Plot plumb line
    ax1.plot(np.array([0,0]), np.array([0,fPathArray[2,-1]]), 'k-', label='plumb line')
    ax2.plot(np.array([0,0]), np.array([0,fPathArray[2,-1]]), 'k-')
    
    # Set plot bounds
    ax1.set_xlim(-PlotBound, PlotBound)
    #ax1.set_ylim(-0.05*, )
    ax2.set_xlim(-PlotBound, PlotBound)
    #ax2.set_ylim(-PlotBound, PlotBound)

    # Add axes labels
    ax1.set_xlabel('Northward drift (ft.)')
    ax1.set_ylabel('True Vertical Depth (ft.)')

    ax2.set_xlabel('Eastward drift (ft.)')
    ax2.set_ylabel('True Vertical Depth (ft.)')
    
    DepthValIndices = FindDepthValIndices(fPathArray[2,:])
    
    for i in DepthValIndices:
    
        # Add i label
        ax1.text(fPathArray[0,i], fPathArray[2,i], 
            str(WellArcLength[i].round(2)), color='cyan', transform=trans_offset1)
        ax2.text(fPathArray[1,i], fPathArray[2,i], 
            str(WellArcLength[i].round(2)), color='cyan', transform=trans_offset2)
    
        ax1.plot(fPathArray[0,i], fPathArray[2,i], '.', color='cyan')
        ax2.plot(fPathArray[1,i], fPathArray[2,i], '.', color='cyan')
    
    ax1.plot(np.nan, np.nan, '.', color='cyan', label='well depth')
        
    ax1.plot(fPathArray[0,-1], fPathArray[2,-1], '.', color='red')
    ax2.plot(fPathArray[1,-1], fPathArray[2,-1], '.', color='red')
       
    ax1.text(fPathArray[0,-1], fPathArray[2,-1], 
        str(WellArcLength[-1].round(2)), color='red', transform=trans_offset1)
    ax2.text(fPathArray[1,-1], fPathArray[2,-1], 
        str(WellArcLength[-1].round(2)), color='red', transform=trans_offset2)
              
    ax1.plot([0, fPathArray[0,-1]], [fPathArray[2,-1], fPathArray[2,-1]], 
        color='red', label='bottom drift')
    (ymin, ymax) = ax1.get_ylim()
    ax1.text(0, ymax, 'N at bottom: ' + str(np.round(fPathArray[0,-1], 2)) + ' ft.', 
        color='red', transform=trans_offset3)
        
    ax2.plot([0, fPathArray[1,-1]], [fPathArray[2,-1], fPathArray[2,-1]], 
        color='red')
    (ymin, ymax) = ax2.get_ylim()
    ax2.text(0, ymax, 'E at bottom: ' + str(np.round(fPathArray[1,-1], 2)) + ' ft.', 
        color='red', transform=trans_offset4)
    
    #ax.set_aspect('auto')
    #ax1.set_aspect(ASPECTRATIO)
    ax1.invert_yaxis()
    #ax2.set_aspect(ASPECTRATIO)
    ax2.invert_yaxis()
    
    plt.axes(ax1)
    plt.legend(loc='lower left', bbox_to_anchor=(0, -0.12, 2.12, 0.102), ncol=4, 
        mode='expand', fontsize=10)
    plt.show()
    
    return fig
          
def PlotEffectiveDiameter(WellArcLength, d_eff, d_casing, JobID):
    FONTPOINTS = 10
    MARKERSIZE = 12
    
    fig = plt.figure(figsize=(8,10.5))
    ax = plt.subplot(111)
    ax.grid(True)
    fig.suptitle(JobID + '\nEffective Diameter as a Function of Well Depth', fontsize=18)
    
    PlotBound = np.ceil(d_casing/2)
    
    trans_offset = mtrans.offset_copy(ax.transData, fig=fig, 
        x=5, y=-FONTPOINTS, units='points')
        
    ax.set_xlim(-PlotBound, PlotBound)
    
    ax.set_xlabel('Effective radius (in.)')
    ax.set_ylabel('Well depth (ft.)')    
    
    # Plot effective radius trace and its mirror image over x=0
    ax.plot(d_eff/2, WellArcLength, 'b--', linewidth=2.0)
    ax.plot(-d_eff/2, WellArcLength, 'b--', linewidth=2.0)
    
    # Plot plumb line
    ax.plot(np.array([0,0]), np.array([0,WellArcLength[-1]]), 'k-')
    
    DepthValIndices = FindDepthValIndices(WellArcLength)
    
    # Plot labels and vector components       
    for i in DepthValIndices:
    
        # Add i label
        ax.text(0, WellArcLength[i], str(d_eff[i].round(2)), color='green', transform=trans_offset)
        
        # Add i diameters
        ax.plot([-d_eff[i]/2,d_eff[i]/2],[WellArcLength[i], WellArcLength[i]], 'g-')
        ax.plot(-d_eff[i]/2, WellArcLength[i], 'g.', markersize=MARKERSIZE)
        ax.plot(d_eff[i]/2, WellArcLength[i], 'g.', markersize=MARKERSIZE)
        
    MinVal, MinIndex = minfinder(d_eff)
    ax.text(0, WellArcLength[MinIndex], str(d_eff[MinIndex].round(2)), color='red', transform=trans_offset)
    ax.plot([-d_eff[MinIndex]/2,d_eff[MinIndex]/2],[WellArcLength[MinIndex], WellArcLength[MinIndex]], 'r-')
    ax.plot(-d_eff[MinIndex]/2, WellArcLength[MinIndex], 'r.', markersize=MARKERSIZE)
    ax.plot(d_eff[MinIndex]/2, WellArcLength[MinIndex], 'r.', markersize=MARKERSIZE)    
    
    ax.invert_yaxis()
    
    plt.show()

    return fig
            
def PlotDoglegTrace(WellArcLength, Curvature, JobID):
    #FONTPOINTS = 10
    
    fig = plt.figure(figsize=(8,10.5))
    ax = plt.subplot(111)
    ax.grid(True)
    fig.suptitle(JobID + '\nWell Curvature as a Function of Well Depth (Dogleg Plot)', fontsize=18)

    #trans_offset = mtrans.offset_copy(ax.transData, fig=fig, 
    #    x=5, y=-FONTPOINTS, units='points')
    
    # Determine plot bound for x-axis.
    (nElements,) = Curvature.shape
    DomainToConsider = slice(np.round(0.05*nElements).astype(int),np.round(0.95*nElements).astype(int)) 
    PlotBound = np.ceil(np.max(Curvature[DomainToConsider])*5)/5
    
    # Set plot bounds
    ax.set_xlim(0, PlotBound)
    
    ax.plot(Curvature, WellArcLength, 'g-', linewidth=2.0)
    
    ax.set_xlabel('Curvature (degrees over 100 ft. arc)')
    ax.set_ylabel('Well depth (ft.)')
    
    ax.invert_yaxis()
    
    plt.show()

    return fig
            
def ClearanceDiagram(WellArcLength, d_eff, d_casing, JobID):
    FONTPOINTS = 10
    
    fig = plt.figure(figsize=(8,10.5))
    ax = plt.subplot(111)
    ax.grid(True)
    fig.suptitle(JobID + '\nDownhole Clearance Diagram', fontsize=18)

    trans_offset = mtrans.offset_copy(ax.transData, fig=fig, 
        x=5, y=0, units='points')
    
    trans_offset2 = mtrans.offset_copy(ax.transData, fig=fig, 
        x=5, y=FONTPOINTS, units='points')
            
    # Set axes labels.
    ax.set_xlabel('horizontal (inches)')
    ax.set_ylabel('vertical (inches)')
    
    # Find minimum effective diameter.
    MinVal, MinIndex = minfinder(d_eff)
    
    r_eff = d_casing - d_eff[MinIndex]
    circ1 = patches.Ellipse(xy=(0, 0), 
        width=d_casing, height=d_casing, angle=360, edgecolor='g', 
        fill=False, label='casing (top)')
    circ2 = patches.Ellipse(xy=(0, r_eff), 
        width=d_casing, height=d_casing, edgecolor='r', 
        fill=False, label='casing (max. deviation)')
    circ3 = patches.Ellipse(xy=(0, r_eff/2), 
        width=d_eff[MinIndex], height=d_eff[MinIndex], edgecolor='b', 
        fill=False, label='max. diameter of pump')
    
    # Add circles and center markers
    ax.add_patch(circ1)
    ax.plot(0, 0, 'gx', markersize=6.0)
    ax.add_patch(circ2)
    ax.plot(0, r_eff, 'rx', markersize=6.0)
    ax.add_patch(circ3)
    ax.plot(0, r_eff/2, 'bx', markersize=6.0)
    
    # Add dimension arrow for r_eff
    ax.plot(np.array([-1.1*(d_casing/2),-1.1*(d_casing/2)]), 
        np.array([0, r_eff]), linewidth=1.5, color='red')
    ax.text(-1.1*(d_casing/2), r_eff/2, str(r_eff.round(2)), 
        color='red', transform=trans_offset)
    
    # Add dimension arrow for d_eff
    ax.plot(np.array([1.1*(d_casing/2), 1.1*(d_casing/2)]), 
        np.array([(r_eff - d_eff[MinIndex])/2, (r_eff + d_eff[MinIndex])/2]), 
        linewidth=1.5, color='blue')
    ax.text(1.1*(d_casing/2), r_eff/2, str(d_eff[MinIndex].round(2)), 
        color='blue', transform=trans_offset)
    
    # Add depth of maximum restriction
    (ymin, ymax) = ax.get_ylim()
    ax.text(0, ymin, 'max. deviation depth: ' + str(WellArcLength[MinIndex].round(1)) + ' ft.', 
        color='red', transform=trans_offset2)
    
    ax.set_aspect(1)
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    #       ncol=1, mode="expand", borderaxespad=0.)
    plt.legend(loc=2, ncol=2, mode="expand", borderaxespad=0., fontsize=10)
    plt.show()
    
    return fig
    
def WellStandardComparisonPlot(WellArcLength, d_casing, fPathArray, JobID):
    
    SCALEINC = 2 # in feet
    FONTPOINTS = 12
    STANDARD='AWWA'
    #STANDARD='RoscoeMoss'
    #STANDARD='SPT'
    
    if STANDARD == 'AWWA':
        slope = 0.0067*d_casing*12.  # Unsure of units for casing diameter
        #slope = 0.067*d_casing
        
    elif STANDARD == 'RoscoeMoss':
        slope = d_casing
        
    elif STANDARD == 'SPT':
        slope = d_casing
        
    DriftVec = 12*np.linalg.norm(fPathArray[:2,:], axis=0) #changed to units of inches
    #StandardVec = slope*fPathArray[2,:]
    #StandardVec = slope*WellArcLength
    StandardVec = slope*(WellArcLength - WellArcLength[0]*np.ones_like(WellArcLength))
    
    fig = plt.figure(figsize=(8,10.5))
    ax = plt.subplot(111)
    ax.grid(True)
    fig.suptitle(JobID + '\nWell Drift Compared to Standard', fontsize=18)
    
    PlotBound = max(np.max(DriftVec), np.max(StandardVec))
    PlotBound = np.ceil(PlotBound/SCALEINC)*SCALEINC

    trans_offset1 = mtrans.offset_copy(ax.transData, fig=fig, 
        x=5, y=-FONTPOINTS, units='points')
        
    trans_offset2 = mtrans.offset_copy(ax.transData, fig=fig, 
        x=5, y=FONTPOINTS, units='points')
        
    ax.set_xlabel('Drift from plumb (inches)')
    ax.set_ylabel('Well depth (feet)')
        
    ax.plot(DriftVec, WellArcLength, 'r-', linewidth=2.0, label='well drift')
    ax.plot(StandardVec, WellArcLength, 'b--', linewidth=1.5, label=STANDARD +' standard')
    
    DepthValIndices = FindDepthValIndices(WellArcLength)
    
    for i in DepthValIndices:
    
        # Add i label
        ax.text(DriftVec[i], WellArcLength[i], 
            str(DriftVec[i].round(2)), color='red', transform=trans_offset2)
        # Add data point
        ax.plot(DriftVec[i], WellArcLength[i], '.', color='red', markersize=8.0)
        
        ax.text(StandardVec[i], WellArcLength[i], 
            str(StandardVec[i].round(2)), color='blue', transform=trans_offset1)
            
        ax.plot(StandardVec[i], WellArcLength[i], '.', color='blue', markersize=8.0)
    
    #ax.plot(np.nan, np.nan, '.', color='cyan', label='well depth')    
    
    ax.invert_yaxis()
    plt.axes(ax)
    plt.legend(loc='lower left', bbox_to_anchor=(0, -0.12, 1, 0.102), ncol=2, 
        mode='expand', fontsize=10)
    plt.show()
    
    return fig