#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:19:08 2018

@author: zwu
"""

import Jarvis
from random import randint

import time

number_cores=24

system=Jarvis.System(ProjectName='test_Box_UA',
                     Year=2019,
                     Usic='L_8')


cluster=Jarvis.Cluster(Name="sniffa")
cluster.set_Partition("batch")

lammps=Jarvis.Simulator(Name="lammps")
lammps.load_Module("gcc/7.3.1")
lammps.load_Module("openmpi/gcc/3.1.1")
lammps.load_Module("fftw/gcc/single/avx/3.3.8")
lammps.set_Excutable("mpirun -np "+str(number_cores)+" /home/zwu/cpulammps/build/lmp -i")
 
gen=Jarvis.SimulationPhase(system,PhaseName="generation")
gen.set_NumNode(1)
gen.set_NumTasks(number_cores)
gen.define("-var trial",            Var=  "000")
gen.define("-var Temp",            Var=  "600000") # real unit 600 K
gen.define("-var usic",            Var=  system.Usic)
gen.define("-var vseed",            Var=  str(randint(100000,999999)))
gen.define("-var steps_gen",            Var=  str(1000000))
gen.define("-var ts",            Var=  str(1))


#while True:
#    time.sleep(5)
#    status=system.detect_JobState(gen)
#    print(status)
#    if status==1:
#        break


equ=Jarvis.SimulationPhase(system,PhaseName="equilibration")
equ.set_NumNode(1)
equ.set_NumTasks(number_cores)
equ.define("-var read_res",Var=  "./generation/restart/restart_"+system.Usic+"_000.gen.restart")
equ.define("-var restartf",Var=str(1000000))
equ.define("-var set_CheckPoint",Var="1")
equ.define("-var Temp", Var=  "600000")
equ.define("-var run_phase", Var=  "1")
equ.define("-var usic",     Var=  system.Usic)
equ.define("-var trial",            Var=  "000")
equ.define("-var vseed",            Var=  str(randint(100000,999999)))
equ.define("-var steps_equ",            Var=  str(2000000))
equ.define("-var ts",            Var=  str(1))
equ.define("-var write_res",            Var=  "./equilibration/restart/restart_"+system.Usic+"_000.equ.restart")

equ_nemd=Jarvis.SimulationPhase(system,PhaseName="equilibration_nemd")
equ_nemd.set_NumNode(1)
equ_nemd.set_NumTasks(number_cores)
equ_nemd.define("-var read_res",Var=  "./equilibration/restart/restart_"+system.Usic+"_000.equ.restart")
equ_nemd.define("-var restartf",Var=str(1000000))
equ_nemd.define("-var set_CheckPoint",Var="1")
equ_nemd.define("-var Temp", Var=  "600000")
equ_nemd.define("-var run_phase", Var=  "1")
equ_nemd.define("-var phase", Var=  "equ_nemd")
equ_nemd.define("-var usic",     Var=  system.Usic)
equ_nemd.define("-var trial",            Var=  "000")
equ_nemd.define("-var vseed",            Var=  str(randint(100000,999999)))
equ_nemd.define("-var steps_equ",            Var=  str(2000000))
equ_nemd.define("-var ts",            Var=  str(1))
equ_nemd.define("-var write_res",   Var=  "./equilibration_nemd/restart/restart_"+system.Usic+"_000.equ_nemd.restart")
equ_nemd.define("-var delta_T", Var="20")


prd_nemd=Jarvis.SimulationPhase(system,PhaseName="production_nemd")
prd_nemd.set_NumNode(1)
prd_nemd.set_NumTasks(number_cores)
prd_nemd.define("-var read_res",Var=  "./equilibration_nemd/restart/restart_"+system.Usic+"_000.equ_nemd.restart")
prd_nemd.define("-var restartf",Var=str(1000000))
prd_nemd.define("-var set_CheckPoint",Var="1")
prd_nemd.define("-var Temp", Var=  "600000")
prd_nemd.define("-var run_phase", Var=  "1")
prd_nemd.define("-var usic",     Var=  system.Usic)
equ_nemd.define("-var phase", Var=  "equ_nemd")
prd_nemd.define("-var trial",            Var=  "000")
prd_nemd.define("-var vseed",            Var=  str(randint(100000,999999)))
prd_nemd.define("-var steps_equ",            Var=  str(2000000))
prd_nemd.define("-var ts",            Var=  str(1))
equ_nemd.define("-var write_res",   Var=  "./production_nemd/restart/restart_"+system.Usic+"_000.prd_nemd.restart")
prd_nemd.define("-var delta_T", Var="20")

system.create_SystemPath()
system.set_InputFolder('./input_scripts/lammps')
system.prepare_SimulationInputs(Filename=['generation.inp','equilibration.inp','equilibration_nemd.inp','production_nemd.inp'])

moltemplate=Jarvis.Moltemplate(system=system)
moltemplate.set_ChainNum(310)
moltemplate.set_Sequence(["S001"]*50)
#moltemplate.make_LmpDataFilebyMoltemplate()

gen.create(Cluster=cluster,Simulator=lammps)
gen.sub(False,dependence=None)

equ.create(Cluster=cluster,Simulator=lammps)
equ.sub(False,dependence=gen)

equ_nemd.create(Cluster=cluster,Simulator=lammps)
equ_nemd.sub(False,dependence=equ)

prd_nemd.create(Cluster=cluster,Simulator=lammps)
prd_nemd.sub(False,dependence=equ_nemd)

cluster_pmdat=Jarvis.Cluster(Name="sniffa")
cluster_pmdat.set_Partition("serial")

pdmat=Jarvis.Simulator(Name="pdmat")
pdmat.load_Module("gcc/6.3.1")
pdmat.set_Excutable("python2")

analysis=Jarvis.Analysis(system)
analysis.set_NumNode(1)
analysis.set_NumTasks(1)

analysis.create(Cluster=cluster_pmdat,Coder=pdmat)
analysis.prepare_InputFile(Filename='generation.inp')
analysis.sub(False)
