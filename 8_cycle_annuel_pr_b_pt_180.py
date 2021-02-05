#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 14:34:30 2020

@author: begin

"""
import xarray as xr
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

var='pr'
#moyenne annuel 1971-2000
stat='moy_men_30_'
#b_pt='posttraite'
b_pt='brute'


#open observation file begin with stat        
path_obs=('/tank/begin/weighting/SE_1/brute/traite/obs/'+var)
files_obs = []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat in i:
        files_obs.append(i)
#open files climex
path_climex=('/tank/begin/weighting/SE_1_climex/'+b_pt+'/traite/'+var)
files_climex= []
for i in os.listdir(path_climex):
    if os.path.isfile(os.path.join(path_climex,i)) and stat in i:
        files_climex.append(i)
#open files cordex
path_cordex=('/tank/begin/weighting/SE_1_CORDEX/'+b_pt+'/traite/'+var)
files_cordex= []
for i in os.listdir(path_cordex):
    if os.path.isfile(os.path.join(path_cordex,i)) and stat in i:
        files_cordex.append(i)
#open files cmip5
path_cmip5=('/tank/begin/weighting/SE_1_CMIP5/'+b_pt+'/traite/'+var)
files_cmip5= []
for i in os.listdir(path_cmip5):
    if os.path.isfile(os.path.join(path_cmip5,i)) and stat in i:
        files_cmip5.append(i)

#open dataarray observation
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j])*86400)

#open dataarray 50 membres climex 
da_climex=[]
for j in range(0,(len(files_climex))):
    da_climex.append(xr.open_dataarray(path_climex+'/'+files_climex[j])*86400)

#open dataarray CORDEX
da_cordex=[]
for j in range(0,(len(files_cordex))):
    da_cordex.append(xr.open_dataarray(path_cordex+'/'+files_cordex[j])*86400)

#open dataarray CMIP5
da_cmip5=[]
for j in range(0,(len(files_cmip5))):
    da_cmip5.append(xr.open_dataarray(path_cmip5+'/'+files_cmip5[j])*86400)

##calcul rapport écart type cycle annuel
rstd_climex=[]
for g in range(0,len(files_climex)):
    rstd_climex.append(np.std(da_climex[g])/np.std(da_obs[0]))
rstd_cordex=[]
for g in range(0,len(files_cordex)):
    rstd_cordex.append(np.std(da_cordex[g])/np.std(da_obs[0]))
rstd_cmip5=[]
for g in range(0,len(files_cmip5)):
    rstd_cmip5.append(np.std(da_cmip5[g])/np.std(da_obs[0]))



plt.figure(1)
rstd=[rstd_climex,rstd_cordex,rstd_cmip5]
labels=(['ClimEx','CORDEX','CMIP5'])
plt.boxplot(rstd,labels=labels)

plt.ylabel('Rapport écart type')

plt.ylim(0,2)
if b_pt == 'brute':
    plt.title(var+'\nCycle annuel 1971-2000*\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_1_b_cycle_annuel_rstd_180_1971-2000',bbox_inches='tight')
else:
    plt.title(var+'\nCycle annuel 1971-2000*\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cycle_annuel_rstd_180_1971-2000',bbox_inches='tight')

