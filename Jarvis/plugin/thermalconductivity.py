#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:19:08 2018

@author: zwu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.optimize import curve_fit


class ThermalConductivity(object):
    
    def __init__(self,  Temp=None,
                        Flux=None,
                        PhaseName=None,
                        ProjectName=None,
                        Usic=None):
        self.ProjectName=ProjectName
        self.Usic=Usic
        self.PhaseName=PhaseName
        self.Temp=Temp
        self.Flux=Flux
        self.num_Atom=self.read_NumAtoms()
        self.CrossArea=self.read_CrossArea()

    
    def read_TempGradient(self):
        with open(self.Temp) as f:
            lines = (line.strip() for line in f if not line.startswith('#') and line.strip().split()[2]!=str(self.num_Atom))
            data = np.loadtxt(lines, delimiter=' ',dtype={'names': ('index', 'pos', 'temp','temp_gradient','density'),'formats': ('i4', 'f4', 'f4','f4','f4')})
            df=pd.DataFrame(data)
            #print(df.groupby('index').mean())
            return df.groupby('index').mean()

    
    def read_Flux(self):
        with open(self.Flux) as f:
            lines = (line.strip() for line in f if not line.startswith('#'))
            data = np.loadtxt(lines, delimiter=' ',dtype={'names': ('time', 'f_hot_rescale', 'f_cold_rescale1','f_cold_rescale2'),'formats': ('i4', 'f4', 'f4','f4')})
            df=pd.DataFrame(data)
            #print(df.groupby('index').mean())
            return df

    def fit_Linear(self,x,y):
        
        def func_Linear(x,k,b):
            return k*x+b

        coeff,pcov=curve_fit(func_Linear,x,y)
        return coeff


    def convert_Unit(self,tc,length=None,time=None,energy=None):
        NA=6.02214086*1e23
        scaling_length=0
        scaling_time=0
        scaling_energy=0
        if length=='A':
            scaling_length=1e-10 # m
        else:
            print("ERROR: length unit is not correct, only \"A\" is allowed")
        if time=='fs':
            scaling_time=1e-15 # s
        else:
            print("ERROR: time unit is not correct, only \"fs\" is allowed")
        if energy=='kcal/mole':
            scaling_energy=4.184 #kj/mol
            scaling_energy=4.184*1000/NA #j
        else:
            print("ERROR: energy unit is not correct, only \"kcal/mole\" is allowed")
        
        tc=tc*(scaling_energy/scaling_time/scaling_length) # w/(m k)
        return tc

    def calc_thermalconductivity(self):
        Flux=self.read_Flux()
        TG=self.read_TempGradient()
        
        slope_Flux=self.fit_Linear(Flux[10:]["time"].values,(np.abs(Flux[10:]["f_hot_rescale"].values)+np.abs(Flux[10:]["f_cold_rescale1"].values)+np.abs(Flux[10:]["f_cold_rescale2"].values))/4)
        heatflux=slope_Flux[0]/self.CrossArea

        slope_TG_1=self.fit_Linear(TG[10:50]['pos'].values,TG[10:50]['temp_gradient'].values)
        slope_TG_2=self.fit_Linear(TG[-50:-10]['pos'].values,TG[-50:-10]['temp_gradient'].values)
        #print(TG[10:70]['pos'],TG[10:70]['temp_gradient'])
        slope_TG_avg=(np.abs(slope_TG_1[0])+np.abs(slope_TG_2[0]))/2

        thermalconductivity=heatflux/slope_TG_avg

        thermalconductivity=self.convert_Unit(thermalconductivity,length='A',time='fs',energy='kcal/mole')


        self.thermalconductivity=thermalconductivity

    def read_NumAtoms(self):
        in_="../simulations/"+self.PhaseName+"/screen/"+self.PhaseName+"_"+self.ProjectName+"_"+self.Usic+".screen"
        with open(in_,'r') as read_f:
            in_path=Path(in_)
            if in_path.is_file():
                while True:
                    line = read_f.readline() 
                    if line.strip().split()[1]=="atoms":
                        numatom=line.strip().split()[0]
                        return numatom

    def read_CrossArea(self):
        in_="../simulations/"+self.PhaseName+"/screen/"+self.PhaseName+"_"+self.ProjectName+"_"+self.Usic+".screen"
        with open(in_,'r') as read_f:
            in_path=Path(in_)
            if in_path.is_file():
                while True:
                    line = read_f.readline()
                    
                    if line.strip().split()[0]=="Step":
                        line = read_f.readline() 
                        volume=line.strip().split()[2]
                        edge=float(volume)**0.33333
                        CrossArea=edge**2
                        return CrossArea

    def out_Info(self):
        pass

    def out_Plot(self):
        pass

#tc=ThermalConductivity(Flux='flux_equ_nemd.out',Temp='temp_equ_nemd_2.profile',num_Atom=16000,CrossArea=82*82)

#print(tc.calc_thermalconductivity())

#dd=tc._read('temp_equ_nemd.profile',16000)
#dd2=tc._read('temp_equ_nemd_2.profile',16000)
#plt.plot(dd2['pos'],dd2['temp_gradient'],"*")
#plt.plot(dd['pos'],dd['temp_gradient'],"*")

#plt.show()