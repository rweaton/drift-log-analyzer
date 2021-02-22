import numpy as np

def CalcDevVecs(Length, Azimuth, Inclination):
    
    (nElements, junk) = Length.shape
    
    # Initialize output vector: 
    #(1st column x-coord., 2nd column: y-coord., 3rd column: z-coord.)
    DevVecs = np.nan*np.ones([nElements, 3])
    
    dL = np.diff(Length)
    dPhi = np.diff(np.radians(Azimuth))
    dTheta = np.diff(np.radians(Inclination))
    
    DevVecs[:,0] = dL*(np.sin(dTheta)*np.cos(dPhi))
    DevVecs[:,1] = dL*(np.sin(dTheta)*np.sin(dPhi))
    DevVecs[:,2] = dL*np.cos(dTheta)
    
    return DevVecs