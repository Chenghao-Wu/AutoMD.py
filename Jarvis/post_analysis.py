#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:19:08 2018

@author: zwu
"""
import os
from pathlib import Path 
import subprocess
import sys
from .system import logger


class PostAnalysis(object):
    def __init__(self,Analysis):
        self.Analysis=Analysis
        self.AnalysisPath=Analysis.SystemPath+"/analysis"
        self.RawDataPath=Analysis.SystemPath+"/analysis/data"
        self.Vars={}
        self.created_Folder = False

    def calc_DiffusionCoefficient(self):
        pass
    
    def calc_DistributionSlipSpringLength(self):
        pass
    
    def calc_DistributionSlipSpringLocation(self):
        pass

    def calc_RadisGyration(self,TimeAveraged=True):
        pass
    
    def calc_EndtoEndDistance(self,TimeAveraged=True):
        pass
    
    def calc_MeanSquareInternalDistance(self,TimeAveraged=True):
        pass
    
    def calc_RelaxationTime(self,Fitting=None,Target=None):
        pass

    def FittingData(self,type_=None,x=None,y=None,boundary='natural',initial_guess=None):
        if type_=="CubicSpline":
            from scipy.interpolate import CubicSpline
            cs = CubicSpline(x, y,bc_type=boundary)
            return cs
        elif type_=="SingleExponential":
            from scipy.optimize import curve_fit 
            def func(x,a,b):
                return a*np.exp(b*x)
            coeff,cov=curve_fit(func,x,y,)
    



    