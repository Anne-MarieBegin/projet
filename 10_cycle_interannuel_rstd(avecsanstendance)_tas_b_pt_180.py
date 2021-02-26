#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 14:34:30 2020

@author: begin

"""
from xclim import ensembles as ens
import xarray as xr
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from pathlib import Path

var='tasmin'
#moyenne annuel 1971-2000
stat='moy_an_30_*'
#b_pt='posttraite'
b_pt='brute'

base=Path('/tank/begin/weighting')

path_obs=base/'SE_1/brute/traite/obs'/var
da_obs=[xr.open_dataarray (fichier) for fichier in path_obs.glob(stat)]   
#open files climex
path_climex=base/'SE_1_climex'/b_pt/'traite'/var
da_climex=[xr.open_dataarray (fichier) for fichier in path_climex.glob(stat)]
#open files cordex
path_cordex=base/'SE_1_CORDEX'/b_pt/'traite'/var
da_cordex=[xr.open_dataarray (fichier) for fichier in path_cordex.glob(stat)]
#open files cmip5
path_cmip5=base/'SE_1_CMIP5'/b_pt/'traite'/var
da_cmip5=[xr.open_dataarray (fichier) for fichier in path_cmip5.glob(stat)]

#conversion en C
for i in range(0,len(da_climex)):
    da_climex[i]=da_climex[i]-273.15
for i in range(0,len(da_cordex)):
    da_cordex[i]=da_cordex[i]-273.15
for i in range(0,len(da_cmip5)):
    da_cmip5[i]=da_cmip5[i]-273.15

#calcul serie annuel detrended
x_detrended_obs=[]
for f in range(0,len(da_obs)):
    x_detrended_obs.append(signal.detrend(da_obs[f]))
x_detrended_climex=[]
for f in range(0,len(da_climex)):
    x_detrended_climex.append(signal.detrend(da_climex[f]))
x_detrended_cordex=[]
for f in range(0,len(da_cordex)):
    x_detrended_cordex.append(signal.detrend(da_cordex[f]))
x_detrended_cmip5=[]
for f in range(0,len(da_cmip5)):
    x_detrended_cmip5.append(signal.detrend(da_cmip5[f]))

#rapport écart type sans tendance
rstd_sans_climex=[]
for i in range(0,len(da_climex)):
    rstd_sans_climex.append(np.std(x_detrended_climex[i])/np.std(x_detrended_obs))
rstd_sans_cordex=[]
for i in range(0,len(da_cordex)):
    rstd_sans_cordex.append(np.std(x_detrended_cordex[i])/np.std(x_detrended_obs))
rstd_sans_cmip5=[]
for i in range(0,len(da_cmip5)):
    rstd_sans_cmip5.append(np.std(x_detrended_cmip5[i])/np.std(x_detrended_obs))

#rapport écart type avec tendance
rstd_avec_climex=[]
for j in range(0,len(da_climex)):
    rstd_avec_climex.append(np.std(da_climex[j])/np.std(da_obs))
rstd_avec_cordex=[]
for j in range(0,len(da_cordex)):
    rstd_avec_cordex.append(np.std(da_cordex[j])/np.std(da_obs))
rstd_avec_cmip5=[]
for j in range(0,len(da_cmip5)):
    rstd_avec_cmip5.append(np.std(da_cmip5[j])/np.std(da_obs))

plt.figure(1)
rstd_avec=[rstd_avec_climex,rstd_avec_cordex,rstd_avec_cmip5]
labels=(['ClimEx','CORDEX','CMIP5'])
plt.boxplot(rstd_avec,labels=labels)
plt.ylabel('Rapport écart type')
plt.ylim(0.4,1.5)
if b_pt == 'brute':
    plt.title(var+'\nSérie annuel avec tendance 1971-2000*\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_1_b_cycle_interannuel_rstd_avec_tendance_180_1971-2000',bbox_inches='tight')
else:
    plt.title(var+'\nSérie annuel avec tendance 1971-2000*\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cycle_interannuel_rstd_avec_tendance_180_1971-2000',bbox_inches='tight')

plt.figure(2)
rstd_sans=[rstd_sans_climex,rstd_sans_cordex,rstd_sans_cmip5]
labels=(['ClimEx','CORDEX','CMIP5'])
plt.boxplot(rstd_sans,labels=labels)
plt.ylabel('Rapport écart type')
plt.ylim(0.4,1.5)
if b_pt == 'brute':
    plt.title(var+'\nSérie annuel sans tendance 1971-2000*\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_1_b_cycle_interannuel_rstd_sans_tendance_180_1971-2000',bbox_inches='tight')
else:
    plt.title(var+'\nSérie annuel sans tendance 1971-2000*\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cycle_interannuel_rstd_sans_tendance_180_1971-2000',bbox_inches='tight')
