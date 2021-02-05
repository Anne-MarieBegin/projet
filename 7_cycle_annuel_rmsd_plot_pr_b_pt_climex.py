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
import skill_metrics as sm
var='pr'
stat='moy_men_30_'
#b_pt='brute'
b_pt='brute'

#open files begin by stat
path=('/tank/begin/weighting/SE_1/'+b_pt+'/traite/'+var)
files = []
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and stat in i:
        files.append(i)
#trier ordre
files.sort()

#open file obsevation begin by stat        
path_obs=('/tank/begin/weighting/SE_1/brute/traite/obs/'+var)
files_obs = []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat in i:
        files_obs.append(i)
        
#open file climex begin by stat        
path_c=('/tank/begin/weighting/SE_1_climex/'+b_pt+'/traite/'+var)
files_c = []
for i in os.listdir(path_c):
    if os.path.isfile(os.path.join(path_c,i)) and stat in i:
        files_c.append(i)

#open datarray SE_1
da=[]
for j in range(0,(len(files))):
    da.append(xr.open_dataarray(path+'/'+files[j])*86400)
    
#enlever le deux membres de climex dans SE_1
del da[8:10] 
 
#open dataarray observation
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j])*86400)

#open dataarray climex      
da_c=[]
for j in range(0,(len(files_c))):
    da_c.append(xr.open_dataarray(path_c+'/'+files_c[j])*86400)

#insérer climex en deuxième position et observation en première position
da.insert(0,da_c[:])
da.insert(0,da_obs[0])        

#calcul centered RMSD annual cycle
crmsd_c=[]
for i in range(0,50):
    crmsd_c.append(sm.centered_rms_dev(da[1][i],da[0]))
crmsd=[]
for j in range(2,12):
    crmsd.append(sm.centered_rms_dev(da[j],da[0]))
    
mois=['Janvier','Février','Mars','Avril','Mai','juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
sim=['Observations',
     'ClimEx (50)',
     'CMIP5_CanESM2_r1i1p1_rcp85',
     'CMIP5_MPI-ESM-LR_r1i1p1_rcp85',
     'CORDEX_CanESM2_CanRCM4_r1i1p1_NAM-22_rcp45',
     'CORDEX_CanESM2_CanRCM4_r1i1p1_NAM-44_rcp45',   
     'CORDEX_CanESM2_RCA4_r1i1p1_NAM-44_rcp85',
     'CORDEX_MPI-ESM-LR_CRCM5-UQAM_r1i1p1_NAM-44_rcp45',
     'CORDEX_MPI-ESM-LR_RegCM4_r1i1p1_NAM-22_rcp85',
     'CORDEX_MPI-ESM-LR_RegCM4_r1i1p1_NAM-44_rcp85',
     'Ouranos_CanESM2_CRCM5-Ouranos_r1i1p1_NAM-22_rcp85',
     'Ouranos_MPI-ESM-LR_CRCM5-Ouranos_r1i1p1_NAM-22_rcp45'
     ]

#plot rapport écart type
plt.figure(1)
for j in range(0,50): 
    plt.plot(sim[1], crmsd_c[j], '.m',markersize=12)
    plt.plot(sim[2],crmsd[0], '.m',markersize=12)
    plt.plot(sim[3],crmsd[1], '.m',markersize=12)
    plt.plot(sim[4],crmsd[2], '.m',markersize=12)
    plt.plot(sim[5],crmsd[3], '.m',markersize=12)
    plt.plot(sim[6],crmsd[4], '.m',markersize=12)
    plt.plot(sim[7],crmsd[5], '.m',markersize=12)
    plt.plot(sim[8],crmsd[6], '.m',markersize=12)
    plt.plot(sim[9],crmsd[7], '.m',markersize=12)
    plt.plot(sim[10],crmsd[8], '.m',markersize=12)
    plt.plot(sim[11],crmsd[9], '.m',markersize=12)
plt.xticks(rotation=90)
plt.ylabel('Centered RMSD', color='m')
plt.ylim(0,0.8)
if b_pt == 'brute':
    plt.title('Précipitation cycle annuel\n1971_2000*\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_1_b_crmsd_climex_1971_2000',bbox_inches='tight')
else:
    plt.title('Précipitation cycle annuel\n1971_2000*\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_crmsd_climex_1971_2000',bbox_inches='tight')

