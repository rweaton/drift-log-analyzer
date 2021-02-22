import numpy as np

def CalcRadiusOfCurvature(PathVecs, nSpanIncs):
    
    # Count number of vectors comprising path
    (nVecs, nComps) = PathVecs.shape
    
    # Generate set of indices to process
    Indices = np.arange(0,nVecs)
    IndicesFilter = (Indices > (nSpanIncs - 1)) & (Indices < (nVecs - nSpanIncs))
    
    # Initialize output arrays 
    radii = np.nan*np.ones_like(Indices)
    angles = np.nan*np.ones_like(Indices)
    
    # For each selected vector in PathVecs, fit an arc using it and two 
    # surrounding neighbors, and then measure the angle spanned by the arc as 
    # well as its radius.  Save measurements to output variables.
    for i in Indices[IndicesFilter]:
        
           # Calculate vectors spanning plane of arc to be fitted at index i         
           v_minus = PathVecs[i, :] - PathVecs[i - nSpanIncs, :]
           v_plus = PathVecs[i + nSpanIncs, :] - PathVecs[i, :]
           
           # Calculate the unit-vector normal to the plane
           PlaneNormal = np.cross(v_minus, v_plus)
           PlaneNormal = PlaneNormal/np.linalg.norm(PlaneNormal)
           
           # Calculate the vector sum that spans the triangle in the plane
           v_sum = v_minus + v_plus
           v_s = v_sum/np.linalg.norm(v_sum)
           
           # Calculate the vector between the spanning vector and the triangle tip
           v_x = v_minus - np.vdot(v_minus, v_s)*v_s
           
           # Calculate v_minus for arc: v_minPrime
           v_minPrime = (1./2.)*v_sum + v_x
           v_minPrimeMag = np.linalg.norm(v_minPrime)
           v_minPrimeUnit = v_minPrime/v_minPrimeMag
           
           # Calculate angle between v_s and v_minPrimeUnit
           alpha = np.arccos(np.vdot(v_minPrimeUnit, v_x/np.linalg.norm(v_x)))
           beta = np.pi - 2*alpha
           
           radii[i] = v_minPrimeMag*(np.sin(alpha)/np.sin(beta))
           angles[i] = 2*beta
           
           ## Calculate the two unit vectors pointing inward to the center of arc
           #r_minus = np.cross(v_minus, PlaneNormal)
           #r_minus = r_minus/np.linalg.norm(r_minus)
           #
           #r_plus = np.cross(v_plus, PlaneNormal)
           #r_plus = r_plus/np.linalg.norm(r_plus)
           #
           ## Calculate the angular span, in radians, of the fitted arc
           #angles[i] = np.arccos(np.vdot(r_plus, r_minus))
           #
           ## Calculate the radius of the fitted arc
           #radii[i] = np.linalg.norm(v_minus + v_plus)/np.linalg.norm(r_plus + r_minus)
           
    return angles, radii