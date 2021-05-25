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
import pandas as pd
var='pr'
stat='men_1971_2000'
#b_pt='brute'
b_pt='brute'

#open files begin by stat
path=('/tank/begin/weighting/SE_2/traite/'+b_pt+'/'+var)
files = []
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and stat in i:
        files.append(i)
#trier ordre
files.sort()

#open file obsevation begin by stat        
path_obs=('/tank/begin/weighting/E_2/traite/obs/'+var)
files_obs = []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat in i:
        files_obs.append(i)
        
#open file obsevation begin by stat        
path_all=('/tank/begin/weighting/E_2/traite/'+b_pt+'/'+var)
files_all = []
for i in os.listdir(path_all):
    if os.path.isfile(os.path.join(path_all,i)) and stat in i:
        files_all.append(i)

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
da_all=[]
for j in range(0,(len(files_all))):
    da_all.append(xr.open_dataarray(path_all+'/'+files_all[j])*86400)
#créer un dictionnaire avec dataarray       
files_totale=files_all
files_split=[]
dictio=[]
for i in range(0,len(files_totale)):
    files_split.append(files_totale[i].split('_'))
    dictio.append({'groupe':files_split[i][3],
                   'gcm':files_split[i][4],
                   'rcm':files_split[i][5],
                   'membre':files_split[i][6],
                   'resolution':files_split[i][7],
                   'rcp':files_split[i][8],
                   'variable':files_split[i][9],
                   'files':files_totale[i],
                   'data':da_all[i]})

#faire dataframe avec dictionnaire
df1=pd.DataFrame.from_dict(dictio)
da_c=[]
for i in range (len(df1)):
    if df1['groupe'][i]=='ClimEx':
        da_c.append(df1['data'][i])
#insérer climex en deuxième position et observation en première position
da.insert(0,da_c[:])
da.insert(0,da_obs[0])        


#calcul rapport écat type cycle annuel
std_obs=np.std(da[0])
#climex
std_c=[]
for k in range(0,50):
    std_c.append(np.std(da[1][k])/std_obs)
#SE_1
std=[]
for k in range(2,12):
    std.append(np.std(da[k])/std_obs)  
 
##calcul coefficeint corrélation
#climex
cc_c=[]
for l in range(0,50):
    cc_c.append(np.corrcoef(da[0],da[1][l]))
#SE_1
cc=[]
for l in range(2,12):
    cc.append(np.corrcoef(da[0],da[l]))

#calcul du biais
#climex
biais_c=[]
for m in range(0,50):
    biais_c.append(da[1][m]-da[0])
#SE_1
biais=[]
for m in range(2,12):
    biais.append(da[m]-da[0])
    
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
#plot cycle annuel
plt.figure(1)
for i in range(0,50):
    plt.plot(mois,da[0],'--k',zorder=52)
    plt.plot(mois,da[1][i],'silver')
    plt.plot(mois,da[2],'r')
    plt.plot(mois,da[3],'b')
    plt.plot(mois,da[4],'g')
    plt.plot(mois,da[5],'c')
    plt.plot(mois,da[6],'m')
    plt.plot(mois,da[7],'y')
    plt.plot(mois,da[8],'grey')
    plt.plot(mois,da[9],'hotpink')
    plt.plot(mois,da[10],'brown')
    plt.plot(mois,da[11],'olive')
plt.xticks(rotation=90)
plt.legend(sim[:],bbox_to_anchor=(1.05, 1), loc='upper left')
plt.ylim(1.5,6)
plt.ylabel('Précipiation (mm/jour)')
if b_pt == 'brute':
    plt.title('Précipitation cycle annuel (E_2)\n1971_2000\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_2_b_cycle_annuel_climex_1971_2000',bbox_inches='tight')
else:
    plt.title('Précipitation cycle annuel (E_2)\n1971_2000\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_2_pt_cycle_annuel_climex_1971_2000',bbox_inches='tight')

#plot rapport écart type
plt.figure(2)
for j in range(0,50): 
    plt.plot(sim[1], std_c[j], 'xg',markersize=12)
    plt.plot(sim[2],std[0], 'xg',markersize=12)
    plt.plot(sim[3],std[1], 'xg',markersize=12)
    plt.plot(sim[4],std[2], 'xg',markersize=12)
    plt.plot(sim[5],std[3], 'xg',markersize=12)
    plt.plot(sim[6],std[4], 'xg',markersize=12)
    plt.plot(sim[7],std[5], 'xg',markersize=12)
    plt.plot(sim[8],std[6], 'xg',markersize=12)
    plt.plot(sim[9],std[7], 'xg',markersize=12)
    plt.plot(sim[10],std[8], 'xg',markersize=12)
    plt.plot(sim[11],std[9], 'xg',markersize=12)
plt.xticks(rotation=90)
plt.ylabel('Rapport écart type', color='g')
plt.ylim(0.3,1.5)
if b_pt == 'brute':
    plt.title('Précipitation cycle annuel\n1971_2000\nBrutes')
   # plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_2_b_rstd_climex_1971_2000',bbox_inches='tight')
else:
    plt.title('Précipitation cycle annuel\n1971_2000\nPost-traitées')
   # plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_2_pt_rstd_climex_1971_2000',bbox_inches='tight')

#plot coefficient corrélation
plt.figure(3)
for k in range(0,50):
    plt.plot(sim[1],cc_c[k][0][1], '.b',markersize=12)
    plt.plot(sim[2],cc[0][0][1], '.b',markersize=12)
    plt.plot(sim[3],cc[1][0][1], '.b',markersize=12)
    plt.plot(sim[4],cc[2][0][1], '.b',markersize=12)
    plt.plot(sim[5],cc[3][0][1], '.b',markersize=12)
    plt.plot(sim[6],cc[4][0][1], '.b',markersize=12)
    plt.plot(sim[7],cc[5][0][1], '.b',markersize=12)
    plt.plot(sim[8],cc[6][0][1], '.b',markersize=12)
    plt.plot(sim[9],cc[7][0][1], '.b',markersize=12)
    plt.plot(sim[10],cc[8][0][1], '.b',markersize=12)
    plt.plot(sim[11],cc[9][0][1], '.b',markersize=12)
plt.xticks(rotation=90)
plt.ylabel('Coefficient corrélation', color='b')
plt.ylim(0,1)  
if b_pt == 'brute':
    plt.title('Précipitation cycle annuel\n1971_2000\nBrutes')
   # plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_2_b_cc_climex_1971_2000',bbox_inches='tight')
else:
    plt.title('Précipitation cycle annuel\n1971_2000\nPost-traitées')
   # plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_2_pt_cc_climex_1971_2000',bbox_inches='tight')

plt.figure(4)
for m in range(0,50):
    plt.plot(mois,biais_c[m],'silver')
    plt.plot(mois,biais[0],'r')
    plt.plot(mois,biais[1],'b')
    plt.plot(mois,biais[2],'g')
    plt.plot(mois,biais[3],'c')
    plt.plot(mois,biais[4],'m')
    plt.plot(mois,biais[5],'y')
    plt.plot(mois,biais[6],'grey')
    plt.plot(mois,biais[7],'hotpink')
    plt.plot(mois,biais[8],'brown')
    plt.plot(mois,biais[9],'olive')
plt.xticks(rotation=90)
plt.legend(sim[1:],bbox_to_anchor=(1.05, 1), loc='upper left')
plt.ylabel('Biais (mm/jour)')
plt.ylim(-2,2)
if b_pt == 'brute':
    plt.title('Précipitation cycle annuel\n1971_2000\nBrutes')
   # plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_2_b_biais_climex_1971_2000',bbox_inches='tight')
else:
    plt.title('Précipitation cycle annuel\n1971_2000\nPost-traitées')
   # plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_2_pt_biais_climex_1971_2000',bbox_inches='tight')
