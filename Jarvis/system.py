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

import subprocess


from .logger import setup_logger
logger = setup_logger()

class System(object):
    def __init__(self,ProjectName=None,Year=None,Usic=None):
        self.ProjectName    =   ProjectName
        self.Year           =   str(Year)
        self.start_date     =   '-S 2020-01-01'
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

    def set_MadeFolder(self,MadeFolder=False):
        self.MadeFolder=MadeFolder

    def prepare_SimulationInputs(self,Filename=None,Automated=False):
        if not Automated:
            if type(Filename)==list:
                for filename in Filename:
                    self.copy_SimulationInputs(InputFolder=self.InputFolder,Filename=filename)
            elif type(Filename)==str:
                self.copy_SimulationInputs(InputFolder=self.InputFolder,Filename=Filename)
            else:
                logger.error(' '.join(["type of Filename is not correct"]))
        elif Automated:
            #self.copy_SimulationInputs(InputFolder=InputFolder,PhaseName=PhaseName)
            pass

    def copy_SimulationInputs(self,InputFolder=None,Filename=None):
        SystemPath=self.get_SystemPath
        cp_from=InputFolder+"/"+Filename
        if not os.path.isfile(cp_from):
            logger.error(' '.join(["input file: "+cp_from+" does not exist"]))
            sys.exit()
        cp_to=SystemPath+"/simulations/simulation_inputs/"+Filename
        shutil.copy2(cp_from,cp_to)

    def create_SystemPath(self):
        self.MadeFolder=True

        SystemPath=self.get_SystemPath
        path=Path(SystemPath)
        if path.exists():
            response = input(SystemPath+" folder exist, delete and make new?(y/n)")
            if response == "y" or response == "yes":
                proc = subprocess.Popen(['/bin/bash'], shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                stdout = proc.communicate(("rm -r "+ SystemPath).encode())
                logger.info(' '.join(["removing "+SystemPath]))
                time.sleep(3)
                path.mkdir(parents=True, exist_ok=True)
                simulation_inputs = path.joinpath("simulations/simulation_inputs")
                simulation_inputs.mkdir(parents=True, exist_ok=True)
                submission_scripts = path.joinpath("simulations/submission_scripts")
                submission_scripts.mkdir(parents=True, exist_ok=True)
            elif response == "n" or response == "no":
                logger.info(' '.join(["EXIT : "+SystemPath+" has already existed"]))
                sys.exit()
            else:
                logger.info(' '.join(["EXIT : Please Specify the right input value!"]))
                sys.exit()
        else:
            path.mkdir(parents=True, exist_ok=True)
            simulation_inputs = path.joinpath("simulations/simulation_inputs")
            simulation_inputs.mkdir(parents=True, exist_ok=True)
            submission_scripts = path.joinpath("simulations/submission_scripts")
            submission_scripts.mkdir(parents=True, exist_ok=True)

        
    def detect_JobState(self,Phase):
        JobName=Phase.JobId
        #JobName='equ_2_4_PI_CG_192'
        #print(JobName)
        process = subprocess.Popen(["sacct "+self.start_date+" --name "+JobName+" --format State"], stdout=subprocess.PIPE,encoding='utf-8',shell=True)
        status=process.communicate()[0].split()[2]
        
        if status=="RUNNING":
            return 0
        elif status=="COMPLETED":
            return 1
        elif status=="PENDING":
            return 2
        elif status=="FAILED":
            logger.error(' '.join(["Job ID ",JobName," FAILED!!!"]))
            sys.exit()