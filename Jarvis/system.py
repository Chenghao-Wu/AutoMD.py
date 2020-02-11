#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:19:08 2018

@author: zwu
"""
import os
import sys
from pathlib import Path 
import subprocess
import time
import shutil

class System(object):
    def __init__(self,ProjectName=None,Year=None,Usic=None):
        self.ProjectName    =   ProjectName
        self.Year           =   str(Year)
        self.Usic           =   Usic
        self.MadeFolder     =   False
    
    @property
    def get_ProjectName(self):
        return self.ProjectName
    
    @property
    def get_Year(self):
        return self.Year

    @property
    def get_Usic(self):
        return self.Usic
    
    @property
    def get_SystemPath(self):
        ProjectName =   self.get_ProjectName
        Year        =   self.get_Year
        Usic        =   self.Usic
        SystemPath   =   os.getcwd()+"/"+ProjectName+"/"+Year+"/"+Usic
        return SystemPath

    def set_InputFolder(self,InputFolder):
        self.InputFolder=InputFolder

    def prepare_SimulationInputs(self,Filename=None,Automated=False):
        if not Automated:
            if type(Filename)==list:
                for filename in Filename:
                    self.copy_SimulationInputs(InputFolder=self.InputFolder,Filename=filename)
            elif type(Filename)==str:
                self.copy_SimulationInputs(InputFolder=self.InputFolder,Filename=Filename)
            else:
                print("ERROR: type of Filename is not correct")
        elif Automated:
            #self.copy_SimulationInputs(InputFolder=InputFolder,PhaseName=PhaseName)
            pass

    def copy_SimulationInputs(self,InputFolder=None,Filename=None):
        SystemPath=self.get_SystemPath
        cp_from=InputFolder+"/"+Filename
        if not os.path.isfile(cp_from):
            print("  ERROR : input file: "+cp_from+" does not exist")
            sys.exit()
        cp_to=SystemPath+"/simulations/simulation_inputs/"+Filename
        shutil.copy2(cp_from,cp_to)

    def create_SystemPath(self):
        self.MadeFolder=True

        SystemPath=self.get_SystemPath
        path=Path(SystemPath)
        if path.exists():
            response = input(SystemPath+" folder exist, delete and make new?(y/n) ")
            if response == "y" or "yes":
                proc = subprocess.Popen(['/bin/bash'], shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                stdout = proc.communicate(("rm -r "+ SystemPath).encode())
                print("removing "+SystemPath)
                time.sleep(3)
                path.mkdir(parents=True, exist_ok=True)
                simulation_inputs = path.joinpath("simulations/simulation_inputs")
                simulation_inputs.mkdir(parents=True, exist_ok=True)
                submission_scripts = path.joinpath("simulations/submission_scripts")
                submission_scripts.mkdir(parents=True, exist_ok=True)

            elif response == "n" or "no":
                print("  EXIT : "+SystemPath+" has already existed")
                sys.exit()
        else:
            path.mkdir(parents=True, exist_ok=True)
            simulation_inputs = path.joinpath("simulations/simulation_inputs")
            simulation_inputs.mkdir(parents=True, exist_ok=True)
            submission_scripts = path.joinpath("simulations/submission_scripts")
            submission_scripts.mkdir(parents=True, exist_ok=True)

        
    