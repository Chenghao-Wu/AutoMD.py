#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:19:08 2018

@author: zwu
"""

import Jarvis

system=Jarvis.System(ProjectName='Test',
                     Year=2019,
                     Usic='test')



cluster=Jarvis.Cluster(Name="sniffa")
cluster.set_Partition("batchgpu")

galamost=Jarvis.Simulator(Name="galamost")
galamost.load_Module("gcc/6.3.1")
galamost.load_Module("boost/mpi/gcc/1.67.0")
galamost.load_Module("cuda/9.2")
galamost.set_Excutable("python2")

gen=Jarvis.SimulationPhase(system,PhaseName="generation")
gen.set_NumNode(1)
gen.set_NumTasks(48)
gen.set_NumGPU(1)
gen.define("-EXEPATH",            Var=  "/home/zwu/galamost-3.1.1")
gen.define("-input_data",         Var=  "./simulation_inputs/input_000.xml")
gen.define("-dt",                 Var=  "0.005")
gen.define("-temp",               Var=  "400")
gen.define("-BoxSize",            Var=  "10.894")
gen.define("-GridSize",           Var=  "0.51")
gen.define("-Kappa",              Var=  "0.05")
gen.define("-FrictionCoeffcient", Var=  "200")
gen.define("-thermo_period",      Var=  "10000")
gen.define("-savefreq",           Var=  "0.1")
gen.define("-run",                Var=  "10000")

equ=Jarvis.SimulationPhase(system,PhaseName="equilibration")
equ.set_NumNode(1)
equ.set_NumTasks(48)
equ.set_NumGPU(1)
equ.define("-EXEPATH",            Var=  "/home/zwu/galamost-3.1.1")
equ.define("-input_data",         Var=  "./generation/restart/gen_restart.0000010000.xml")
equ.define("-dt",                 Var=  "0.005")
equ.define("-temp",               Var=  "400")
equ.define("-BoxSize",            Var=  "10.894")
equ.define("-GridSize",           Var=  "0.51")
equ.define("-Kappa",              Var=  "0.05")
equ.define("-FrictionCoeffcient", Var=  "200")
equ.define("-thermo_period",      Var=  "10000")
equ.define("-savefreq",           Var=  "0.1")
equ.define("-run",                Var=  "10000")


system.create_SystemPath()
system.set_InputFolder('./input_scripts/galamost')
system.prepare_SimulationInputs(Filename=['generation.inp','equilibration.inp','input_000.xml'])

gen.create(Cluster=cluster,Simulator=galamost)
gen.sub(True,dependence=None)

equ.create(Cluster=cluster,Simulator=galamost)
equ.sub(True,dependence=gen)


