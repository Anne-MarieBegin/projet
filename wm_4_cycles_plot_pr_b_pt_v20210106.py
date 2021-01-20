#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 14:34:30 2020

@author: begin

v20201221 ouverture cycle annuel et cycle interannuel graphique 3 axes(erreur relative moyenne,erreur relative variance,erreur relative tendance)
v20210106 (brute et post-traite)
"""

import xarray as xr
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

var='pr'
stat='moy_men_30_'
stat2='moy_an_30_'

b_pt='brute'
#b_pt='posttraite'
###########################################################################
#open files begin by stat
path=('/exec/begin/weighting/SE_1/'+b_pt+'/traite/'+var)
files = []
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and stat in i:
        files.append(i)
files.sort()

#open file obsevation begin by stat        
path_obs=('/exec/begin/weighting/SE_1/brute/traite/obs/'+var)
files_obs = []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat in i:
        files_obs.append(i)

#open datarray
da=[]
da_obs=[]
for j in range(0,(len(files))):
    da.append(xr.open_dataarray(path+'/'+files[j])*86400)
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j])*86400)

#insert obs at the first position
da.insert(0,da_obs[0])    
    
#################################################################
#open files begin by stat2
path2=('/exec/begin/weighting/SE_1/'+b_pt+'/traite/'+var)
files2 = []
for i in os.listdir(path2):
    if os.path.isfile(os.path.join(path2,i)) and stat2 in i:
        files2.append(i)
files2.sort()

#open file obsevation begin by stat2        
path_obs2=('/exec/begin/weighting/SE_1/brute/traite/obs/'+var)
files_obs2 = []
for i in os.listdir(path_obs2):
    if os.path.isfile(os.path.join(path_obs2,i)) and stat2 in i:
        files_obs2.append(i)

#open datarray stat2
da2=[]
da_obs2=[]
for j in range(0,(len(files2))):
    da2.append(xr.open_dataarray(path2+'/'+files2[j])*86400)
for j in range(0,(len(files_obs2))):
    da_obs2.append(xr.open_dataarray(path_obs2+'/'+files_obs2[j])*86400)

#insert obs at the first position
da2.insert(0,da_obs2[0])        
######################################################################
#calcul moyenne du cycle annuel
moy=[]
for i in range(0,len(files)+1):
    moy.append(np.mean(da[i]))

#calcul erreur relative sur la moyenne cycle annuel
erreur_moy=[]
for i in range(0,len(files)+1):
    erreur_moy.append(((moy[i]-moy[0])/moy[0]*100))

#calcul variance cycle annuel
varr=[]
for j in range(0,len(files)+1):
    varr.append(np.var(da[j]))

#calcul erreur relative sur la variance cycle annuel
erreur_var=[]
for j in range(0,len(files)+1):
    erreur_var.append(((varr[j]-varr[0])/varr[0]*100))

#calcul équation pente
pente=[]  
oo=[]    
for i in range(0,len(files2)+1):
    x=np.arange(1971,1999)
    y=da2[i]
    m,b=np.polyfit(x,y,1)
    pente.append(m*10)#pente sur 10 ans
    oo.append(b)
      
#calcul de y pour chaque x avec equation pente
yy=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
for p in range(0,len(files2)+1):
    for t in range(0,28):
        yy[p].append((pente[p]/10)*x[t]+oo[p])#(/10 pour compenser ligne 103)
        
#calcul de la courbe moins la tendance
detrend=[]
for g in range(0,len(files2)+1):
    detrend.append(da2[g]-yy[g])

#calcul de l'erreur relative sur la pente cycle interannuel
erreur_pente=[]
for k in range(0,len(files2)+1):
    erreur_pente.append(((pente[k]-pente[0])/pente[0]*100))

sim=['Observations',
     'CMIP5_CanESM2_r1i1p1_rcp85',
     'CMIP5_MPI-ESM-LR_r1i1p1_rcp85',
     'CORDEX_CanESM2_CanRCM4_r1i1p1_NAM-22_rcp45',
     'CORDEX_CanESM2_CanRCM4_r1i1p1_NAM-44_rcp45',   
     'CORDEX_CanESM2_RCA4_r1i1p1_NAM-44_rcp85',
     'CORDEX_MPI-ESM-LR_CRCM5-UQAM_r1i1p1_NAM-44_rcp45',
     'CORDEX_MPI-ESM-LR_RegCM4_r1i1p1_NAM-22_rcp85',
     'CORDEX_MPI-ESM-LR_RegCM4_r1i1p1_NAM-44_rcp85',
     'ClimEx_CanESM2_CRCM5-Ouranos_kda_NAM-11_rcp85',
     'ClimEx_CanESM2_CRCM5-Ouranos_kex_NAM-11_rcp85',
     'Ouranos_CanESM2_CRCM5-Ouranos_r1i1p1_NAM-22_rcp85',
     'Ouranos_MPI-ESM-LR_CRCM5-Ouranos_r1i1p1_NAM-22_rcp45'
     ]
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax3 = ax1.twinx() 
ax1.plot(sim[1],erreur_moy[1],color='r',marker='.',markersize=12)
ax2.plot(sim[1],erreur_var[1],color='b',marker='x',markersize=12)
ax3.plot(sim[1],erreur_pente[1],color='g',marker='s',markersize=10)
ax1.plot(sim[2],erreur_moy[2],color='r',marker='.',markersize=12)
ax2.plot(sim[2],erreur_var[2],color='b',marker='x',markersize=12)
ax3.plot(sim[2],erreur_pente[2],color='g',marker='s',markersize=10)
ax1.plot(sim[3],erreur_moy[3],color='r',marker='.',markersize=12)
ax2.plot(sim[3],erreur_var[3],color='b',marker='x',markersize=12)
ax3.plot(sim[3],erreur_pente[3],color='g',marker='s',markersize=10)
ax1.plot(sim[4],erreur_moy[4],color='r',marker='.',markersize=12)
ax2.plot(sim[4],erreur_var[4],color='b',marker='x',markersize=12)
ax3.plot(sim[4],erreur_pente[4],color='g',marker='s',markersize=10)
ax1.plot(sim[5],erreur_moy[5],color='r',marker='.',markersize=12)
ax2.plot(sim[5],erreur_var[5],color='b',marker='x',markersize=12)
ax3.plot(sim[5],erreur_pente[5],color='g',marker='s',markersize=10)
ax1.plot(sim[6],erreur_moy[6],color='r',marker='.',markersize=12)
ax2.plot(sim[6],erreur_var[6],color='b',marker='x',markersize=12)
ax3.plot(sim[6],erreur_pente[6],color='g',marker='s',markersize=10)
ax1.plot(sim[7],erreur_moy[7],color='r',marker='.',markersize=12)
ax2.plot(sim[7],erreur_var[7],color='b',marker='x',markersize=12)
ax3.plot(sim[7],erreur_pente[7],color='g',marker='s',markersize=10)
ax1.plot(sim[8],erreur_moy[8],color='r',marker='.',markersize=12)
ax2.plot(sim[8],erreur_var[8],color='b',marker='x',markersize=12)
ax3.plot(sim[8],erreur_pente[8],color='g',marker='s',markersize=10)
ax1.plot(sim[9],erreur_moy[9],color='r',marker='.',markersize=12)
ax2.plot(sim[9],erreur_var[9],color='b',marker='x',markersize=12)
ax3.plot(sim[9],erreur_pente[9],color='g',marker='s',markersize=10)
ax1.plot(sim[10],erreur_moy[10],color='r',marker='.',markersize=12)
ax2.plot(sim[10],erreur_var[10],color='b',marker='x',markersize=12)
ax3.plot(sim[10],erreur_pente[10],color='g',marker='s',markersize=10)
ax1.plot(sim[11],erreur_moy[11],color='r',marker='.',markersize=12)
ax2.plot(sim[11],erreur_var[11],color='b',marker='x',markersize=12)
ax3.plot(sim[11],erreur_pente[11],color='g',marker='s',markersize=10)
ax1.plot(sim[12],erreur_moy[12],color='r',marker='.',markersize=12)
ax2.plot(sim[12],erreur_var[12],color='b',marker='x',markersize=12)
ax3.plot(sim[12],erreur_pente[12],color='g',marker='s',markersize=10)
ax3.spines["right"].set_position(("axes", 1.2))
ax1.set_ylabel('Erreur relative sur la moyenne (%) \nCycle annuel',color='r')
ax2.set_ylabel('Erreur relative sur la variance (%)\nCycle annuel',color='b')
ax3.set_ylabel('Erreur relative sur la tendance (%)\nSérie annuelle',color='g')
ax1.set_ylim(-20,50)
ax2.set_ylim(-100,100)
ax3.set_ylim(-500,1100)
plt.setp(ax1.get_xticklabels(), rotation=270, ha='left')

if b_pt=='brute':
    plt.title('Précipitation \n1971-2000*\nBrutes')
    plt.savefig('/exec/begin/weighting/plots/brute/pr_SE_1_b_erreur_moy_var_tendance_1971-2000',bbox_inches='tight')
else:
    plt.title('Précipitation \n1971-2000*\nPost-traitées')
    plt.savefig('/exec/begin/weighting/plots/posttraite/pr_SE_1_pt_erreur_moy_var_tendance_1971-2000',bbox_inches='tight')
