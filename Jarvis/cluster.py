#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 12:19:08 2018

@author: zwu
"""


class Cluster(object):
    def __init__(self,Name=None):
        self.Name=Name
        self.AccountSwitch=False
        self.Partition=0

    def set_Account(self,Account):
        self.AccountSwitch=True
        self.Account=Account
    
    def set_Partition(self,Partition):
        self.Partition=Partition
        