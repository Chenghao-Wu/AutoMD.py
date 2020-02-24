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
import shutil
from .system import logger


class Analysis(object):
    def __init__(self,System):
        self.System=System
        self.SystemPath =   System.get_SystemPath
        self.AnalysisPath  =   Path(self.SystemPath)
        self.NumNodes=0
        self.NumTasks=0
        self.Vars={}
        self.JobId     =   "analysis"+"_"+self.System.ProjectName+"_"+self.System.Usic
        self.created_Folder = False


    def prepare_InputFile(self,Filename=None,Automated=False):
        if self.created_Folder:
            if not Automated:
                if type(Filename)==list:
                    for filename in Filename:
                        self.copy_AnalysisInputs(InputFolder=self.System.InputFolder,Filename=filename)
                elif type(Filename)==str:
                    self.copy_AnalysisInputs(InputFolder=self.System.InputFolder,Filename=Filename)
                else:
                    logger.error(' '.join(["type of Filename is not correct"]))
            elif Automated:
                #self.copy_SimulationInputs(InputFolder=InputFolder,PhaseName=PhaseName)
                pass
        else:
            logger.error(' '.join(["Analysis Folder has not been created"]))
            logger.warning(' '.join(["Please make sure Prapare_InputFile is set behind Create"]))

    def copy_AnalysisInputs(self,InputFolder=None,Filename=None):
        cp_from=InputFolder+"/"+Filename
        if not os.path.isfile(cp_from):
            logger.error(' '.join(["input file: "+cp_from+" does not exist"]))
            sys.exit()
        cp_to=self.SystemPath+"/analysis/analysis_inputs/"+Filename
        shutil.copy2(cp_from,cp_to)

    def set_NumNode(self,NumNode):
        self.NumNodes=NumNode
    
    def set_NumTasks(self,NumTasks):
        self.NumTasks=NumTasks
    
    def define(self,VarName,Var=None):
        self.Vars[VarName]=Var

    def create_Folder(self):
        if self.System.MadeFolder:
            analysis_inputs         =   self.AnalysisPath.joinpath("analysis/"+"analysis_inputs/")
            log         =   self.AnalysisPath.joinpath("analysis/"+"log/")
            screen      =   self.AnalysisPath.joinpath("analysis/"+"screen/")
            cluster_out =   self.AnalysisPath.joinpath("analysis/"+"submission_files/cluster_out/")
            data  =   self.AnalysisPath.joinpath("analysis/"+"data/")
            post_analysis     =   self.AnalysisPath.joinpath("analysis/"+"post_analysis/")
            visualization     =   self.AnalysisPath.joinpath("analysis/"+"visualization/")
            submission_scripts         =   self.AnalysisPath.joinpath("analysis/"+"submission_scripts/")
            
            analysis_inputs.mkdir(parents=True,exist_ok=True)
            log.mkdir(parents=True,exist_ok=True)
            screen.mkdir(parents=True,exist_ok=True)
            cluster_out.mkdir(parents=True,exist_ok=True)
            data.mkdir(parents=True,exist_ok=True)
            post_analysis.mkdir(parents=True,exist_ok=True)
            visualization.mkdir(parents=True,exist_ok=True)
            submission_scripts.mkdir(parents=True,exist_ok=True)
        else:
            logger.error(' '.join(["System Project Folders are not Created"]))
            sys.exit()

    def create(self,Cluster=None,Coder=None):
        self.create_Folder()
        self.create_SubmissionFile(Cluster,Coder)
        self.created_Folder=True

    def create_SubmissionFile(self,Cluster,Coder):
        SubmissionFileDirectory=self.SystemPath+"/analysis/"+"submission_files"

        SubmissionFile=open(SubmissionFileDirectory+"/"+"analysis"+"_"+self.System.ProjectName+"_"+self.System.Usic+".sub","w")
        SubmissionFile.write("#!/bin/bash -x"+"\n")
        
        assert self.NumNodes>0, "  ERROR : Please Check Cluster Number of Nodes "+str(self.NumNodes)
        SubmissionFile.write("#SBATCH --nodes "+str(self.NumNodes)+"\n")
        
        assert self.NumTasks>0, "  ERROR : Please Check Cluster Number of Tasks"
        SubmissionFile.write("#SBATCH --ntasks "+str(self.NumTasks)+"\n")

        assert type(Cluster.Partition)==str, "  ERROR : Please Check Cluster Partition Name"

        SubmissionFile.write("#SBATCH --partition="+str(Cluster.Partition)+"\n")
        SubmissionFile.write("#SBATCH --output "+"./submission_files/cluster_out/out_"+"analysis"+"_"+self.System.ProjectName+"_"+self.System.Usic+".o"+'\n')
        SubmissionFile.write("#SBATCH --job-name "+"analysis"+"_"+self.System.ProjectName+"_"+self.System.Usic+"\n")
        
        SubmissionFile.write("\n")
        SubmissionFile.write("module purge"+'\n')
        for moduleii in Coder.Modules:
            SubmissionFile.write("module load "+moduleii+"\n")
        SubmissionFile.write("\n")
        VarStr=""
        for varii in self.Vars.keys():
            VarStr=VarStr+" "+varii+" "+self.Vars[varii]

        ScreenPath="./"+"screen"+"/"+"analysis"+"_"+self.System.ProjectName+"_"+self.System.Usic+".screen"


        Excute_str=Coder.Excutable+" ./analysis_inputs/"+"analysis"+".inp"

        SubmissionFile.write(Excute_str+" "+VarStr+" > "+ScreenPath)

        SubmissionFile.close()

    def create_SubmissionScript(self,Dependence):
        SubmissionScriptDirectory=self.SystemPath+"/analysis/"+"submission_scripts"
        SubmissionScript=open(SubmissionScriptDirectory+"/"+"analysis"+"_"+self.System.ProjectName+"_"+self.System.Usic+".sh","w")
        SubmissionScript.write("#!/bin/bash -x"+"\n")
        SubmissionScript.write("cd "+self.SystemPath+"/analysis\n")
        
        SubFile=  "./"+"submission_files"+"/"+"analysis"+"_"+self.System.ProjectName+"_"+self.System.Usic+".sub"

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

        SubmissionFileDirectory =   self.SystemPath+"/analysis"+"/"+"submission_scripts"
        SubFile                 =   "analysis"+"_"+self.System.ProjectName+"_"+self.System.Usic+".sh"
        cmd="sh "+SubmissionFileDirectory+"/"+SubFile
        if Bool==True:
            os.system(cmd)
        else:
            pass