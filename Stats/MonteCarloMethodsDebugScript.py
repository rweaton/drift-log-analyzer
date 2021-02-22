import numpy as np
import MonteCarloMethods as MCM

dist1 = np.random.normal(0.3, 0.2, (500,))
dist2 = np.random.normal(0.0, 0.2, (300,))
dist3 = np.random.normal(0.4, 0.36, (750,))

permDict1 = MCM.PermutationTest(1000, 0.05, MCM.Scaler, dist1, dist2, scale=2.5, offset=1.3)
permDict2 = MCM.PermutationTest(1000, 0.05, MCM.DiffOfVars, dist1, dist2)
permDict3 = MCM.Bootstrapper(1000, 0.025, np.var, dist3)
permDict4 = MCM.Bootstrapper(1000, 0.10, MCM.Scaler, dist1, dist2, scale=2.5, offset=1.3)