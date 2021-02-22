import pandas as pd
import numpy as np
import MonteCarloMethods as MCM

nReps = 1000
alpha = 0.05

DrillPipeThickness = pd.read_csv('/mnt/storage/DrillpipeThicknessAnalysis/DrillPipeMeasurements_2017-02-10.csv',header=1)

badFilt = (DrillPipeThickness['Classification']=='bad')
newFilt = (DrillPipeThickness['Classification']=='new')

dataCols = DrillPipeThickness.columns[2:23]
thBad = DrillPipeThickness[dataCols][badFilt]
thNew = DrillPipeThickness[dataCols][newFilt]

thBadArray = np.reshape(thBad.values, -1)
thNewArray = np.reshape(thNew.values, -1)

thBadArray = thBadArray[~np.isnan(thBadArray)]
thNewArray = thNewArray[~np.isnan(thNewArray)]

DiffOfMeans_PermTest = MCM.PermutationTest(nReps, alpha, MCM.DiffOfMeans, thBadArray, thNewArray)

thBad_MeanBootstrap = MCM.Bootstrapper(nReps, alpha, np.mean, thBadArray)
thNew_MeanBootstrap = MCM.Bootstrapper(nReps, alpha, np.mean, thNewArray)

thBad_StdBootstrap = MCM.Bootstrapper(nReps, alpha, np.std, thBadArray)
thNew_StdBootstrap = MCM.Bootstrapper(nReps, alpha, np.std, thNewArray)
