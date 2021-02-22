#import scipy.stats as stats
import numpy as np
#import os

def DiffOfMeans(dist1, dist2):
    mean1 = np.mean(dist1)
    mean2 = np.mean(dist2)
    return mean2 - mean1
    
def DiffOfVars(dist1, dist2):
    var1 = np.var(dist1)
    var2 = np.var(dist2)
    return var2 - var1
    
def Scaler(dist1, dist2, scale, offset):
    var1 = np.var(dist1)
    var2 = np.var(dist2)
        
    return scale*(var2 - var1) + offset
    
def Bootstrapper(nReps, alpha, statfunc, *dists, **fParams):
    # General bootstrapping routine. [RE: 2017-02-15]
    #
    # ARGUMENT DEFINITIONS:
    # nReps:    the number of times that the emperical distribution(s) are 
    #           resampled and processed by the estimator function to produce
    #           a distribution of (simulated) test statistics.
    #
    # alpha:    the significance level.
    #
    # statfunc: name of the estimator function that takes the resampled 
    #           distribution(s) as input and produces one instance of the test
    #           statistic as output.
    #
    # dists:    the distribution, or distributions, to be resampled.  Either a
    #           single distribution may be named in a single argument, or
    #           multiple distributions can be listed as multiple arguments--
    #           whatever is appropriate for the estimator function being used.
    #
    # params:   additional parameters required by statfunc.  Parameter
    #           names are specific to statfunc and must be passed in keyword
    #           (e.g. scale=2.5)
    #
    # OUTPUT
    # A dictionary with the following key-value pairs:
    # 'BootstrapDist':  A list of the test statistics used in the bootstrap.  
    #                   Values are sorted in ascending order.
    #
    # 'LowerBound':
    #
    # 'UpperBound':
    

    # Count number of elements in *dists
    nDists = np.size(dists)
             
    # Initialize bootstrapping outcome distribution array
    testStats = np.nan*np.ones((nReps,))
    
    # Run bootstrapping procedure
    repIndices = np.arange(0, nReps, 1)
    
    for i in repIndices:
        resampledDists = []
        for d in dists:
            resampledDists.append(np.random.choice(d, d.shape, True))
            
        testStats[i] = statfunc(*resampledDists, **fParams)
        
    testStats.sort()
    lowbound = testStats[np.floor((alpha/2)*nReps - 1)]
    highbound = testStats[np.ceil((1 - alpha/2)*nReps - 1)]
    median = testStats[np.round(nReps/2 - 1)]
    mean = np.mean(testStats)
    
    bootDict = {'BootstrapDist': testStats,               
                'MedianValue': median,
                'MeanValue': mean,
                'CI_LowerBound': lowbound,
                'CI_UpperBound': highbound}
    
    return bootDict
    
def PermutationTest(nReps, alpha, statfunc, *dists, **fParams):
    
    nElementsPerDist = np.empty((0,))
    pooledDist = np.empty((0,))
    nDists = np.size(dists)
    
    obsVal = statfunc(*dists, **fParams)
    
    for d in dists:
        (nElements,) = d.shape
        nElementsPerDist = np.append(nElementsPerDist, nElements)
        pooledDist = np.append(pooledDist, d)
    
    (nTotalElements,) = pooledDist.shape
    indices = np.arange(0,nTotalElements,1)
    
    startIndices = np.cumsum(np.insert(nElementsPerDist, 0, 0)[0:-1])
    endIndices = np.cumsum(nElementsPerDist)
    
    # Generate list of slices for extracting shuffled data
    SliceList = []
    for i in np.arange(0, nDists, 1):
        SliceList.append(slice(startIndices[i], endIndices[i]))
    
    # Initialize bootstrapping outcome distribution array
    testStats = np.nan*np.ones((nReps,))
    
    # Run Monte Carlo resampling procedure
    repIndices = np.arange(0, nReps, 1)
    
    for i in repIndices:
        np.random.shuffle(indices[:])
        
        # Reset list of resampled distributions
        resampledDists = []
        
        for j in np.arange(0, nDists):
            resampledDists.append(pooledDist[indices[SliceList[j]]])
            
        testStats[i] = statfunc(*resampledDists, **fParams)
        
    testStats.sort()
    
    #lowbound = testStats[np.floor((alpha/2)*nReps - 1)]
    #highbound = testStats[np.ceil((1 - alpha/2)*nReps - 1)]
    #median = testStats[np.round(nReps-1)]
    #mean = np.mean(testStats)
    p_val = np.sum([testStats >= obsVal])/(nReps + 1)
    
    permDict = {
        'PermutationTestDist': testStats,
        'val_obs' : obsVal,
        'p-value': p_val
        }
    
    return permDict