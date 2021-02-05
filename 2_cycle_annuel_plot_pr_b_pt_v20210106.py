#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 14:34:30 2020

@author: begin

v20201218 cycle annuel(couleur courbes),erreur absolue(couleur courbes),rapport variance+coefficient corrélation
v20201222 cycle annuel retour (retour ligne de couleur), ajustement de l'échelle des axes (corrigé rapport variance)
v20210106 (brute et post-traite)cycle annuel,biais, rapport std et coefficient corrélation
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

#calcul moy std annual cycle
moy=[]
std=[]
for k in range(0,(len(files)+1)):
    moy.append(np.mean(da[k]))
    std.append(np.std(da[k]))
    
#calcul variance ratio
rapport_std=[]
for i in range(0,len(files)+1):
    rapport_std.append(std[i]/std[0])
    
#calcul coefficeint corrélation
cc=[]
for l in range(0,len(files)+1):
    cc.append(np.corrcoef(da[0],da[l]))

#calcul bias over year
da_diff=[]
for d in range(0,len(files)+1):
    da_diff.append((da[d]-da[0]))
    
#calcul RMSE annual cycle
#rmse_val=[]
#def rmse(obs,data):
#     return np.sqrt(((obs - data) ** 2).mean())
#for t in range(0,(len(files)+1)):
#    rmse_val.append(rmse(np.array(da[0]), np.array(da[t])))
#print(rmse_val)

mois=['Janvier','Février','Mars','Avril','Mai','juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
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


#plot annual cycle
plt.figure(1)
plt.plot(mois,da[0],'--k',lw=3,zorder=13)
plt.plot(mois,da[1],'r')
plt.plot(mois,da[2],'b')
plt.plot(mois,da[3],'g')
plt.plot(mois,da[4],'c')
plt.plot(mois,da[5],'m')
plt.plot(mois,da[6],'y')
plt.plot(mois,da[7],'grey')
plt.plot(mois,da[8],'hotpink')
plt.plot(mois,da[9],'orange')
plt.plot(mois,da[10],'dimgrey')
plt.plot(mois,da[11],'brown')
plt.plot(mois,da[12],'olive')
plt.legend(sim[:],bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=90)
plt.ylabel('Précipiation (mm/jour)')
plt.ylim(1.5,5.5)
#if b_pt == 'brute':
#    plt.title('Précipitation cycle annuel\n1971_2000*\nBrutes')
#    plt.savefig('/exec/begin/weighting/plots/brute/'+var+'_SE_1_b_cycle_annuel_1971_2000',bbox_inches='tight')
#else:
#    plt.title('Précipitation cycle annuel\n1971_2000*\nPost-traitées')
#    plt.savefig('/exec/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cycle_annuel_1971_2000',bbox_inches='tight')
#    
#
##plot biais over year
#plt.figure(2)
#plt.plot(mois,da_diff[1],'r')
#plt.plot(mois,da_diff[2],'b')
#plt.plot(mois,da_diff[3],'g')
#plt.plot(mois,da_diff[4],'c')
#plt.plot(mois,da_diff[5],'m')
#plt.plot(mois,da_diff[6],'y')
#plt.plot(mois,da_diff[7],'grey')
#plt.plot(mois,da_diff[8],'hotpink')
#plt.plot(mois,da_diff[9],'orange')
#plt.plot(mois,da_diff[10],'dimgrey')
#plt.plot(mois,da_diff[11],'brown')
#plt.plot(mois,da_diff[12],'olive')
#plt.legend(sim[1:13],bbox_to_anchor=(1.05, 1), loc='upper left')
#plt.xticks(rotation=90)
#plt.ylabel('Biais (mm/jour)')
#plt.ylim(-2,2)
#if b_pt == 'brute':
#    plt.title('Précipitation cycle annuel\n1971_2000*\nBrutes')
#    plt.savefig('/exec/begin/weighting/plots/brute/'+var+'_SE_1_b_biais_1971_2000',bbox_inches='tight')
#else:
#    plt.title('Précipitation cycle annuel\n1971_2000*\nPost-traitées')
#    plt.savefig('/exec/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_biais_1971_2000',bbox_inches='tight')
#    
##plot 2 axes ratio variance et cefficient correlation
#fig, ax1 = plt.subplots()   
#ax1.plot(sim[1], rapport_std[1], 'xg',markersize=12)
#ax1.plot(sim[2], rapport_std[2], 'xg',markersize=12)
#ax1.plot(sim[3], rapport_std[3], 'xg',markersize=12)
#ax1.plot(sim[4], rapport_std[4], 'xg',markersize=12)
#ax1.plot(sim[5], rapport_std[5], 'xg',markersize=12)
#ax1.plot(sim[6], rapport_std[6], 'xg',markersize=12)
#ax1.plot(sim[7], rapport_std[7], 'xg',markersize=12)
#ax1.plot(sim[8], rapport_std[8], 'xg',markersize=12)
#ax1.plot(sim[9], rapport_std[9], 'xg',markersize=12)
#ax1.plot(sim[10], rapport_std[10], 'xg',markersize=12)
#ax1.plot(sim[11], rapport_std[11], 'xg',markersize=12)
#ax1.plot(sim[12], rapport_std[12], 'xg',markersize=12)
#ax2 = ax1.twinx()
#ax2.plot(sim[1], cc[1][0][1], '.b',markersize=12)
#ax2.plot(sim[2], cc[2][0][1], '.b',markersize=12)
#ax2.plot(sim[3], cc[3][0][1], '.b',markersize=12)
#ax2.plot(sim[4], cc[4][0][1], '.b',markersize=12)
#ax2.plot(sim[5], cc[5][0][1], '.b',markersize=12)
#ax2.plot(sim[6], cc[6][0][1], '.b',markersize=12)
#ax2.plot(sim[7], cc[7][0][1], '.b',markersize=12)
#ax2.plot(sim[8], cc[8][0][1], '.b',markersize=12)
#ax2.plot(sim[9], cc[9][0][1], '.b',markersize=12)
#ax2.plot(sim[10], cc[10][0][1], '.b',markersize=12)
#ax2.plot(sim[11], cc[11][0][1], '.b',markersize=12)
#ax2.plot(sim[12], cc[12][0][1], '.b',markersize=12)
#ax1.set_ylabel('Rapport écart type', color='g')
#ax2.set_ylabel('Coefficient corrélation', color='b')
#ax1.set_ylim(0.25,1.75)
#ax2.set_ylim(0,1)
#plt.setp(ax1.get_xticklabels(), rotation=270, ha='left')
#if b_pt == 'brute':
#    plt.title('Précipitation cycle annuel\n1971_2000*\nBrutes')
#    plt.savefig('/exec/begin/weighting/plots/brute/'+var+'_SE_1_b_cc_rstd_1971_2000',bbox_inches='tight')
#else:
#    plt.title('Précipitation cycle annuel\n1971_2000*\nPosttraitées')
#    plt.savefig('/exec/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cc_rstd_1971_2000',bbox_inches='tight')
#    