#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 10:09:46 2018

@author: ryaneaton
"""
import numpy as np


def KronDelta(A, B):

    filter = np.sqrt((A - B)*(A - B)) == 0.

    return filter + 0.


def AverageAngleMethod(MD, Inc, Azim, **kwargs):

    # If angles are listed in units of degree then change to radians
    if "AngleUnits" in kwargs.keys():
        if kwargs["AngleUnits"]  == 'degrees':
            Inc = (np.pi/180.)*Inc
            Azim = (np.pi/180.)*Azim

    NextMD = np.append(MD[1:], np.nan)
    NextInc = np.append(Inc[1:], np.nan)
    NextAzim = np.append(Azim[1:], np.nan)

    DelMD = NextMD - MD
    AvgInc = (Inc + NextInc)/2
    AvgAzim = (Azim + NextAzim)/2

    DelNorth = DelMD * np.sin(AvgInc) * np.cos(AvgAzim)
    DelEast = DelMD * np.sin(AvgInc) * np.sin(AvgAzim)
    DelTVD = DelMD * np.cos(AvgInc)

    return DelNorth, DelEast, DelTVD


def BalancedTangentialMethod(MD, Inc, Azim, **kwargs):

    # If angles are listed in units of degree then change to radians
    if "AngleUnits" in kwargs.keys():
        if kwargs["AngleUnits"]  == 'degrees':
            Inc = (np.pi/180.)*Inc
            Azim = (np.pi/180.)*Azim

    NextMD = np.append(MD[1:], np.nan)
    NextInc = np.append(Inc[1:], np.nan)
    NextAzim = np.append(Azim[1:], np.nan)

    DelMD = NextMD - MD

    DelTVD = (DelMD/2.) * (np.cos(Inc) + np.cos(NextInc))
    DelNorth = (DelMD/2.) * (np.sin(Inc) * np.cos(Azim) +
                np.sin(NextInc) * np.cos(NextAzim))
    DelEast = (DelMD/2.) * (np.sin(Inc) * np.sin(Azim) +
               np.sin(NextInc) * np.sin(NextAzim))

    return DelNorth, DelEast, DelTVD


def RadiusOfCurvatureMethod(MD, Inc, Azim, **kwargs):

    # If angles are listed in units of degree then change to radians
    if "AngleUnits" in kwargs.keys():
        if kwargs["AngleUnits"]  == 'degrees':
            Inc = (np.pi/180.)*Inc
            Azim = (np.pi/180.)*Azim

    NextMD = np.append(MD[1:], np.nan)
    NextInc = np.append(Inc[1:], np.nan)
    NextAzim = np.append(Azim[1:], np.nan)

    DelMD = NextMD - MD

    Inc_plus = (NextInc + Inc)/2.
    Inc_minus = (NextInc - Inc)/2.
    
    Azim_plus = (NextAzim + Azim)/2.
    Azim_minus = (NextAzim - Azim)/2.

    DelTVD = DelMD * np.cos(Inc_plus) * (np.sin(Inc_minus)/(Inc_minus + 
                            KronDelta(Inc_minus, 0.))+KronDelta(Inc_minus, 0.))

    rho = DelMD * np.sin(Inc_plus) * (np.sin(Inc_minus)/(Inc_minus + 
                            KronDelta(Inc_minus, 0.))+KronDelta(Inc_minus, 0.))

    DelNorth = rho * np.cos(Azim_plus) * (np.sin(Azim_minus)/(Azim_minus + 
                            KronDelta(Azim_minus, 0.))+KronDelta(Azim_minus, 0.))

    DelEast = rho * np.sin(Azim_plus) * (np.sin(Azim_minus)/(Azim_minus + 
                            KronDelta(Azim_minus, 0.))+KronDelta(Azim_minus, 0.))

    return DelNorth, DelEast, DelTVD


def MinimumCurvatureMethod(MD, Inc, Azim, **kwargs):

    # If angles are listed in units of degree then change to radians
    #if(kwargs['AngleUnits'] == 'degrees'):
    if "AngleUnits" in kwargs.keys():
        if kwargs["AngleUnits"]  == 'degrees':
            Inc = (np.pi/180.)*Inc
            Azim = (np.pi/180.)*Azim

    NextMD = np.append(MD[1:], np.nan)
    NextInc = np.append(Inc[1:], np.nan)
    NextAzim = np.append(Azim[1:], np.nan)

    DelMD = NextMD - MD

    beta = np.arccos(np.cos(NextInc - Inc) - (np.sin(Inc)*np.sin(NextInc)*(1 -
                            np.cos(NextAzim - Azim))))

    FC = (2./beta)*np.tan(beta/2)

    DelTVD = (DelMD/2.) * (np.cos(Inc) + np.cos(NextInc)) * FC

    DelNorth = (DelMD/2.) * (np.sin(Inc) * np.cos(Azim) +
                np.sin(NextInc) * np.cos(NextAzim)) * FC

    DelEast = (DelMD/2.) * (np.sin(Inc) * np.sin(Azim) +
               np.sin(NextInc) * np.sin(NextAzim)) * FC

    return DelNorth, DelEast, DelTVD
