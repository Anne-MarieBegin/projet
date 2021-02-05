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
var='pr'
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

#conversion en mm / jour
for i in range(0,len(da_obs)):
    da_obs[i]=da_obs[i]*86400
for i in range(0,len(da_climex)):
    da_climex[i]=da_climex[i]*86400
for i in range(0,len(da_cordex)):
    da_cordex[i]=da_cordex[i]*86400
for i in range(0,len(da_cmip5)):
    da_cmip5[i]=da_cmip5[i]*86400


#
#calcul pente
#climex
pente_climex=[]  
oo=[]    
for i in range(0,len(da_climex)):
    x=np.arange(1971,1999)
    y=da_climex[i]
    m,b=np.polyfit(x,y,1)
    pente_climex.append(m*10)#pente sur 10 ans
    oo.append(b)
#cordex
pente_cordex=[]  
oo=[]    
for i in range(0,len(da_cordex)):
    x=np.arange(1971,1999)
    y=da_cordex[i]
    m,b=np.polyfit(x,y,1)
    pente_cordex.append(m*10)#pente sur 10 ans
    oo.append(b)
#cordex
pente_cmip5=[]  
oo=[]    
for i in range(0,len(da_cmip5)):
    x=np.arange(1971,1999)
    y=da_cmip5[i]
    m,b=np.polyfit(x,y,1)
    pente_cmip5.append(m*10)#pente sur 10 ans
    oo.append(b)

plt.figure(1)
pente=[pente_climex,pente_cordex,pente_cmip5]
labels=(['ClimEx','CORDEX','CMIP5'])
plt.boxplot(pente,labels=labels)

plt.ylabel('Pente (mm/jour / 10 ans)')

plt.ylim(-0.25,0.25)
if b_pt == 'brute':
    plt.title(var+'\nSérie annuelle 1971-2000*\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_1_b_cycle_interannuel_pente_180_1971-2000',bbox_inches='tight')
else:
    plt.title(var+'\nSérie annuelle 1971-2000*\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cycle_interannuel_pente_180_1971-2000',bbox_inches='tight')

