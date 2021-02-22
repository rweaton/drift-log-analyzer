import numpy as np

def NormalDistn(x, mu, sigma):
    
    OnesVec = np.ones_like(x)
    NormConst = 1./(sigma*np.sqrt(2.*np.pi))
    Output = NormConst*np.exp((-(x - mu*OnesVec) ** 2)/(2*(sigma ** 2)))
    
    return(Output) 