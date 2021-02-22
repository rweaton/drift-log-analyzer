import numpy as np

def WellArcLengthCalculator(Depths, Gamma):
    # This is a simple routine that takes the collection of vectors that define 
    # the well path, calculates the difference vectors between them,
    # calculates the magnitudes of the difference vectors and finally cumulatively 
    # sums them into a running arc length of the well.
    
    # Get array size.
    (nComps, nVecs) = Gamma.shape
    
    # Calculate difference vectors.
    DiffVecs = np.diff(Gamma, 1, -1)
    
    # Calculate magnitudes of difference vectors.
    DiffVecMags = np.linalg.norm(DiffVecs, 1, 0)
    
    # Append a 0 to the first element of the DiffVecMags array.
    DiffVecMags = np.concatenate((np.array([0]), DiffVecMags),0)
    
    # Cumulatively sum elements of DiffVecMags to calculate arc length.
    WellArcLength = np.cumsum(DiffVecMags)
    
    return WellArcLength