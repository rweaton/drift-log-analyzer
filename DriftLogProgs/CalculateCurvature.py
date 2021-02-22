import numpy as np
import SymmetricDifferenceDifferentiator as SDD

def CalculateCurvature(Depths, Gamma):
    # Depths must be a 1 X N array (row vector, each column-entry a depth)
    # Gamma must be a 3 X N array (each column is a 3D position vector at the
    # depth correspondinding to the element in "Depths" with the same index).
    
    # Get array size.
    (nComps, nVecs) = Gamma.shape
    
    # Tile the Depths array into a 2D array with the same size as Gamma. The 
    # differentiation function used subsequently requires arrays representing 
    # dependent and independent variables to be the same size.
    d = np.tile(Depths, [nComps,1])
    
    # Indicate the dimension across which to differentiate Gamma
    DiffDim = 1
    
    # Calculate GammaPrime
    GammaPrime = SDD.SymmetricDifferenceDifferentiator(d, Gamma, DiffDim)
    
    # Calculate GammaPrimePrime
    GammaPrimePrime = SDD.SymmetricDifferenceDifferentiator(d, GammaPrime, DiffDim)
    
    # Calculate magnitudes of first-derivative vectors
    GammaPrimeMags = np.linalg.norm(GammaPrime, 1, 0)
    
    # Calculate the cross-product of first- and second-derivative vectors
    CP = np.cross(GammaPrime.transpose(), GammaPrimePrime.transpose())
    
    # Calculate curvature
    Curvature = np.linalg.norm(CP.transpose(), 1, 0)/(GammaPrimeMags)**3
    
    return Curvature