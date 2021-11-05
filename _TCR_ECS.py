#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 16:33:35 2021

@author: begin
"""

import xarray as xr
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pylab as plb

gcm=['ACCESS1-0','bcc-csm1-1','bcc-csm1-1-m','CanESM2','CCSM4','CNRM-CM5',
     'CSIRO-Mk3-6-0','FGOALS-s2','GFDL-CM3','GFDL-ESM2G','GFDL-ESM2M',
     'GISS-E2-H','GISS-E2-R','HadGEM2-ES','inmcm4','IPSL-CM5A-LR','IPSL-CM5B-LR',
     'MIROC5','MIROC-ESM','MPI-ESM-LR','MPI-ESM-P','MRI-CGCM3','NorESM1-M']
ecs=[3.83,2.82,2.87,3.69,2.89,3.25,4.08,4.17,3.97,2.39,2.44,2.31,2.11,
     4.59,2.08,4.13,2.61,2.72,4.67,3.63,3.45,2.60,2.80]
tcr=[2.0,1.7,2.1,2.4,1.8,2.1,1.8,2.4,2.0,1.10,1.30,1.7,1.5,2.5,1.3,
     2.0,1.5,1.5,2.2,2.0,2.0,1.6,1.4]

for i,z in enumerate(gcm):
    x=ecs[i]
    y=tcr[i]
    plt.scatter(x,y)
    plt.text(x+0.03,y+0.03,z) 
cc=np.corrcoef(ecs,tcr)  
z = np.polyfit(ecs, tcr, 1)
p = np.poly1d(z)
plb.plot(ecs, p(ecs), '--k',linewidth=0.5)
plt.title('CMIP5\nCoefficient corrélation ='+str(round(cc[0][1],3)))
plt.xlabel('Equilibrium climate sensitivity (ECS) (K)')
plt.ylabel('Transient climate response (TCR) (K)')
plt.savefig('/tank/begin/weighting/plots/ECS_vs_TCR')