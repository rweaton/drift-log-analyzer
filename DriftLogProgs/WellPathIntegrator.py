import numpy as np

def WellPathIntegrator(DevVecs):
    # This routine uses the balanced tangential method (the vector analog of 
    # the trapazoidal method for numerical integration) to integrate a series
    # deviations vectors for plotting well path.  
    
    (nDevVecs, nElements) = DevVecs.shape
    
    # Initialize output vector
    PosVecs = np.nan*np.ones([nDevVecs,nElements])
    PosVecs[0,:] = np.zeros([1,3])
    
    # Run through series of deviation vectors, average neighbors and add to 
    # cumulative sum.
    for i in np.arange(1,nDevVecs):
        PosVecs[i,:] = (DevVecs[i,:] + DevVecs[i-1,:])/2. + PosVecs[i-1,:]
              
    return PosVecs