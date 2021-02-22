import numpy as np

# Remember to comment these out after debugging.
# import ImportLogDataScript as ids
# Read into a dataframe, values stored in a user-selected LAS file
# ProcessedDataTable = ids.ImportData()

# Filter parameters
#KernelBounds = np.array([-50., 50.]);


def NormalDistn(x, mu, sigma):
    
    OnesVec = np.ones_like(x)
    NormConst = 1./(sigma*np.sqrt(2.*np.pi))
    Output = NormConst*np.exp((-(x - mu*OnesVec) ** 2)/(2*(sigma ** 2)))
    return(Output) 


def FilterSignal(Signal, SampFreq, KernelHalfWidth):
    
    KernelBounds = np.array([-5*KernelHalfWidth, 5*KernelHalfWidth]);
    
    Kernel = NormalDistn(
        np.arange(KernelBounds[0,]*SampFreq, KernelBounds[1,]*SampFreq), 
        0., KernelHalfWidth*SampFreq)
    Output = np.convolve(Signal, Kernel, 'same')
    return(Output)

# Comment this out after debugging.    
# Filter DET signal
# SampFreq = 0.25
# KernelHalfWidth = 15.
# FilteredSignal = FilterSignal(ProcessedDataTable['DET'], 
#    SampFreq, KernelHalfWidth)