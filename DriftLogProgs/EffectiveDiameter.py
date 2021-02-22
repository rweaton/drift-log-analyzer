import numpy as np

def EffectiveDiameter(Gamma, d_casing):
    
    (nElements, nVecs) = Gamma.shape
    
    r_top = Gamma[:,0]
    r_bot = Gamma[:,-1]
    scriptr = r_bot - r_top
    scriptr_unit = scriptr/np.linalg.norm(scriptr)
    
    r_delta = Gamma - np.transpose(np.tile(r_top, (nVecs,1)))
    
    projs = np.dot(np.transpose(r_delta), scriptr_unit)
    
    r_eff = r_delta - np.outer(scriptr_unit, projs)   
    
    d_eff = d_casing*np.ones_like(projs) - np.linalg.norm(r_eff, axis=0)
    
    return d_eff