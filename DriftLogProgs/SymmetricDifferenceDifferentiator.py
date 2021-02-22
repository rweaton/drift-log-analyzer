import numpy as np

def SymmetricDifferenceDifferentiator(x, f_x, DiffDim):
    
    fShapeTuple = f_x.shape
    xShapeTuple = x.shape
    
    if fShapeTuple != xShapeTuple:
        print('Error: Arrays of independent and dependent variables are not the same size. Exiting...')
        return None    
    else:
        nDims = len(fShapeTuple)
        DimList = np.arange(0,nDims)
    
        fPrime_x = np.nan*np.ones_like(f_x)   
    
        for n in DimList:
            if n == DiffDim:
                if n == 0:
                    writeSlice = slice(1,-1)
                    plusSlice = slice(2,None)
                    negSlice = slice(0,-2)
                else:
                    writeSlice = writeSlice,slice(1,-1)
                    plusSlice = plusSlice,slice(2,None)
                    negSlice = negSlice,slice(0,-2)
            else:
                if n == 0:
                    writeSlice = slice(None,None)
                    plusSlice = slice(None,None)
                    negSlice = slice(None,None)
                else:
                    writeSlice = writeSlice,slice(None,None)
                    plusSlice = plusSlice,slice(None,None)
                    negSlice = negSlice,slice(None,None)
            
        fPrime_x[writeSlice] = (f_x[plusSlice] - f_x[negSlice])/(x[plusSlice] - x[negSlice])
    
        return fPrime_x