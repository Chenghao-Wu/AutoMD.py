#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:19:08 2018

@author: zwu
"""

import sys
from pathlib import Path
sys.path.append('/home/zwu/Jarvis')

import Jarvis

parser = argparse.ArgumentParser(description='obtain the namestring and usic name.')
parser.add_argument('-ProjectName', type=str,nargs=1,
                   help='directory for the simulation')
parser.add_argument('-Year', type=int,nargs=1,
                   help='directory for the simulation')
parser.add_argument('-Usic', type=str,nargs=1,
                   help='directory for the simulation')
parser.add_argument('-Phase', type=str,nargs=1,
                   help='directory for the simulation')
args = parser.parse_args()

Temp="./simulations/"+args.Phase[0]+"/screen/"+"temp_"+args.Phase[0]+".profile"
Flux="./simulations/"+args.Phase[0]+"/screen/"+"flux_"+args.Phase[0]+".out"
tc=Jarvis.ThermalConductivity(  Temp=Temp,Flux=Flux,
                                PhaseName=args.Phase[0],
                                ProjectName=args.ProjectName[0],
                                Usic=args.Usic[0]
                                )
tc.calc_thermalconductivity()
print(tc.thermalconductivity)

