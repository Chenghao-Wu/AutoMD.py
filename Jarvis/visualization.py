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
from .system import logger


class Visualization(object):
    def __init__(self,Analysis):
        self.Analysis=Analysis
        self.Vars={}
        self.created_Folder = False


    