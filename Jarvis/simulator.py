#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:19:08 2018

@author: zwu
"""


class Simulator(object):
    def __init__(self,Name=None):
        self.Name=Name
        self.Modules=[]

    def load_Module(self,Module):
        self.Modules.append(Module)
    
    def set_Excutable(self,Excutable):
        self.Excutable=Excutable
   