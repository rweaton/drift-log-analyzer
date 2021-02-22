#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 13:27:59 2018

@author: ryaneaton
"""

import numpy as np
import ImportLogDataScript_Gyro3 as ILGS_G

NFITS = 1e3


def db_daf(bz):

    out = (bz - bz[0]*np.ones_like(bz))/(bz[-1] - bz[0])

    return out


def db_da0(bz):

    out = - (bz - bz[0]*np.ones_like(bz))/(bz[-1] - bz[0]) + np.ones_like(bz)

    return out


def b(bz, a0, af):

    out = ((af - a0)/(bz[-1] - bz[0]))*(bz - bz[0]*np.ones_like(bz)) + a0*np.ones_like(bz)

    return out


def CalcGradF(p, aVec):

    bz = p[:, -1]

    [a0x, afx, a0y, afy] = aVec

    #a0x = ax[0]; afx = ax[1]
    #a0y = ay[0]; afy = ay[1]

    dF_da0x = -2*np.sum((p[:, 0] - b(bz, a0x, afx))*db_da0(bz))

    dF_dafx = -2*np.sum((p[:, 0] - b(bz, a0x, afx))*db_daf(bz))

    dF_da0y = -2*np.sum((p[:, 1] - b(bz, a0y, afy))*db_da0(bz))

    dF_dafy = -2*np.sum((p[:, 1] - b(bz, a0y, afy))*db_daf(bz))

    return np.array([dF_da0x, dF_dafx, dF_da0y, dF_dafy])


def CalcF(p, aVec):

    bz = p[:, -1]

    [a0x, afx, a0y, afy] = aVec

    #a0x = ax[0]; afx = ax[1]
    #a0y = ay[0]; afy = ay[1]

    out = np.sum((p[:, 0] - b(bz, a0x, afx))**2 + (p[:, 1] - b(bz, a0y, afy))**2)

    RMSE = np.sqrt(out/len(bz))

    return out, RMSE


def LineGen(bz, aVec):

    [a0x, afx, a0y, afy] = aVec

    return np.array([b(bz, a0x, afx), b(bz, a0y, afy), bz])


# Import borepath
LogDataTable = ILGS_G.ImportData()

# Initialized fit parameter vector
aVec = np.array([0, 0, 0, 0])
delta_aVec = np.array([0, 0, 0, 0])
gamma = 1

# Assemble array to be fitted from relevant DataFrame columns
p = np.array([LogDataTable['DevComp_North'],
              LogDataTable['DevComp_East'],
              LogDataTable['DevComp_Down']]).transpose()

# Begin Gradient descent
for i in np.arange(0, NFITS):

    delta_aVec_old = delta_aVec
    aVec_old = aVec

    delta_aVec = CalcGradF(p, aVec)
    F, RMSE = CalcF(p, aVec)
    delta_aVec_u = delta_aVec/np.linalg.norm(delta_aVec)
    aVec = aVec - gamma*delta_aVec_u

    #gamma = np.inner(aVec - aVec_old,
    #                 delta_aVec - delta_aVec_old)/(np.linalg.norm(delta_aVec -
    #                                                    delta_aVec_old)**2)
