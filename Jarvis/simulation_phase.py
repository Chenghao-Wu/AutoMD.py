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

from .system import System


class SimulationPhase(object):
    def __init__(self,System,PhaseName=None):
        self.System     =   System
        self.PhaseName  =   PhaseName
        self.SystemPath =   System.get_SystemPath
        self.PhasePath  =   Path(self.SystemPath)
        self.JobId     =   self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic
        self.GPUSwitch=False
        self.NumNodes=0
        self.NumTasks=0
        self.Vars={}

    def set_NumNode(self,NumNodes):
        self.NumNodes=NumNodes

    def set_NumTasks(self,NumTasks):
        self.NumTasks=NumTasks
    
    def set_NumGPU(self,NumGPUs):
        self.GPUSwitch=True
        self.NumGPUs=NumGPUs

    def define(self,VarName,Var=None):
        self.Vars[VarName]=Var

    def create(self,Cluster=None,Simulator=None):
        self.create_Folder()
        self.create_SubmissionFile(Cluster,Simulator)

    def create_Folder(self):
        if self.System.MadeFolder:
            log         =   self.PhasePath.joinpath("simulations/"+self.PhaseName+"/log/")
            restart     =   self.PhasePath.joinpath("simulations/"+self.PhaseName+"/restart/")
            screen      =   self.PhasePath.joinpath("simulations/"+self.PhaseName+"/screen/")
            cluster_out =   self.PhasePath.joinpath("simulations/"+self.PhaseName+"/submission_files/cluster_out/")
            trajectory  =   self.PhasePath.joinpath("simulations/"+self.PhaseName+"/trajectory/")
            
            log.mkdir(parents=True,exist_ok=True)
            restart.mkdir(parents=True,exist_ok=True)
            screen.mkdir(parents=True,exist_ok=True)
            cluster_out.mkdir(parents=True,exist_ok=True)
            trajectory.mkdir(parents=True,exist_ok=True)
        else:
            print("  ERROR : System Project Folders are not Created")
            sys.exit()

    
    def create_SubmissionFile(self,Cluster,Simulator):
        SubmissionFileDirectory=self.SystemPath+"/simulations/"+self.PhaseName+"/"+"submission_files"

        SubmissionFile=open(SubmissionFileDirectory+"/"+self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic+".sub","w")
        SubmissionFile.write("#!/bin/bash -x"+"\n")
        
        assert self.NumNodes>0, "  ERROR : Please Check Cluster Number of Nodes"
        SubmissionFile.write("#SBATCH --nodes "+str(self.NumNodes)+"\n")
        
        assert self.NumTasks>0, "  ERROR : Please Check Cluster Number of Tasks"
        SubmissionFile.write("#SBATCH --ntasks "+str(self.NumTasks)+"\n")

        assert type(Cluster.Partition)==str, "  ERROR : Please Check Cluster Partition Name"
        SubmissionFile.write("#SBATCH --partition="+str(Cluster.Partition)+"\n")
        SubmissionFile.write("#SBATCH --output "+"./"+self.PhaseName+"/submission_files/cluster_out/out_"+self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic+".o"+'\n')
        SubmissionFile.write("#SBATCH --job-name "+self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic+"\n")
        if self.GPUSwitch:
            SubmissionFile.write("#SBATCH --gres=gpu "+str(self.NumGPUs)+"\n")
        
        
        
        SubmissionFile.write("\n")
        SubmissionFile.write("module purge"+'\n')
        for moduleii in Simulator.Modules:
            SubmissionFile.write("module load "+moduleii+"\n")
        SubmissionFile.write("\n")
        VarStr=""
        for varii in self.Vars.keys():
            VarStr=VarStr+" "+varii+" "+self.Vars[varii]

        ScreenPath="./"+self.PhaseName+"/screen"+"/"+self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic+".screen"

        Excute_str=Simulator.Excutable+" ./simulation_inputs/"+self.PhaseName+".inp"

        SubmissionFile.write(Excute_str+" "+VarStr+" > "+ScreenPath)

        SubmissionFile.close()
    
        

    def create_SubmissionScript(self,Dependence):
        SubmissionScriptDirectory=self.SystemPath+"/simulations/"+"submission_scripts"
        SubmissionScript=open(SubmissionScriptDirectory+"/"+self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic+".sh","w")
        SubmissionScript.write("#!/bin/bash -x"+"\n")
        SubmissionScript.write("cd "+self.SystemPath+"/simulations\n")
        
        SubFile=  "./"+self.PhaseName+"/"+"submission_files"+"/"+self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic+".sub"

        SubmissionScript.write("SubFile="+SubFile+"\n")
        SubmissionScript.write("test -e ${SubFile}"+"\n")
        SubmissionScript.write('if [ \"$?\" -eq \"0\" ]; then'+"\n")
        if not Dependence == None:
            SubmissionScript.write("    sbatch --dependency=$(squeue --noheader --format %i --name "+Dependence.JobId+") ${SubFile}"+"\n")
        else:
            SubmissionScript.write("    sbatch ${SubFile}"+"\n")
        SubmissionScript.write("else"+"\n")
        SubmissionScript.write("    continue"+"\n")
        SubmissionScript.write("fi"+"\n")

    def sub(self,Bool,dependence=None):
        '''
        dependence: (object) simulation phase
        '''

        self.create_SubmissionScript(dependence)

        SubmissionFileDirectory =   self.SystemPath+"/simulations"+"/"+"submission_scripts"
        SubFile                 =   self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic+".sh"
        cmd="sh "+SubmissionFileDirectory+"/"+SubFile
        if Bool==True:
            os.system(cmd)
        else:
            pass
        #print(os.getcwd())
        #status = subprocess.call(cmd,shell=True)
        #if (status == 0 ):
        #    print("Submitting Job %s" % SubFile)
        #else:
        #    print("Error submitting Job "+SubFile)
        

        """
        SubFile                 =   SubmissionFileDirectory+"/"+self.PhaseName+"_"+self.System.ProjectName+"_"+self.System.Usic+".sub"
        
        if not os.path.isfile(SubFile):
            print("  ERROR : "+SubFile+" does not exist!!!\n")
            sys.exit()
        if dependence==None:
            cmd="sbatch "+SubFile
            status = subprocess.call(cmd)
            if (status == 0 ):
                print("Submitting Job %s" % SubFile)
            else:
                print("Error submitting Job "+SubFile)
        else:
            dependence_sub=0
            if isinstance(dependence,str):
                dependence_sub=dependence
            else:
                dependence_sub=dependence.JobId
            
            if dependence_sub==0:
                print("  ERROR : dependence can not be 0")
                sys.exit()

            cmd = "sbatch --dependency=$(squeue --noheader --format %i --name "+dependence_sub+") "+SubFile
            status = subprocess.call(cmd)
            print("Submitting Job with dependece: %s" % dependence_sub)
            if (status == 0 ):
                print("Submitting Job %s" % SubFile)
            else:
                print("Error submitting Job "+SubFile)
        """
        
        
    
        

