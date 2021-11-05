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
stat1='30x4_1971_2000_'#référence
b_pt='brute'


path_obs=('/tank/begin/weighting/E_1/traite/obs/'+var)

files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j])*86400)

df_obs=pd.DataFrame(da_obs[0])

##ouvrir tous les fichiers qui commence par stat1 
path_all=('/tank/begin/weighting/E_1/traite/'+b_pt+'/'+var)

files_all= []
for i in os.listdir(path_all):
    if os.path.isfile(os.path.join(path_all,i)) and stat1 in i:
        files_all.append(i)
        files_all.sort()

#ouvrir dataarray des fichiers qui commence par stat1
da_all=[]
for j in range(0,(len(files_all))):
    da_all.append(xr.open_dataarray(path_all+'/'+files_all[j])*86400)


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
                   'data':pd.DataFrame(da_all[i])})

#faire dataframe avec dictionnaire
df_all=pd.DataFrame.from_dict(dictio) 
df_all['combine']=df_all['gcm']+'_'+df_all['rcm']+'_'+df_all['membre']+'_'+df_all['resolution']

#déterminer liste des simulations uniques
l=[]
for i in range(0,len(files_split)):
    l.append(df_all['combine'][i])
l_unique=np.unique(l)

#déterminer position simulation unique
position= [ list(df_all['combine']).index(i) for i in list(l_unique)]
#selectionner position dans df
df_sel=df_all.iloc[position]



#écart type pour chaque saison des observations
std_DJF_obs=np.nanstd(df_obs[0])
std_JJA_obs=np.nanstd(df_obs[1])
std_MAM_obs=np.nanstd(df_obs[2])
std_SON_obs=np.nanstd(df_obs[3])

#écart type pour chaque saison pour simulations uniques
std_DJF_climex=[]
std_MAM_climex=[]
std_JJA_climex=[]
std_SON_climex=[]
#ordre des saisons dans fichier(DJF,JJA,MAM,SON)
for i in position:
    if df_all.groupe[i]=='ClimEx':
        std_DJF_climex.append(np.nanstd(df_all['data'][i][0]))
        std_JJA_climex.append(np.nanstd(df_all['data'][i][1]))
        std_MAM_climex.append(np.nanstd(df_all['data'][i][2]))
        std_SON_climex.append(np.nanstd(df_all['data'][i][3]))

std_DJF_cordex=[]
std_MAM_cordex=[]
std_JJA_cordex=[]
std_SON_cordex=[]
groupe=['CORDEX','Ouranos']
for i in position:
    for j in range(0,2):
        if df_all.groupe[i]==groupe[j]:
            std_DJF_cordex.append(np.nanstd(df_all['data'][i][0]))
            std_JJA_cordex.append(np.nanstd(df_all['data'][i][1]))
            std_MAM_cordex.append(np.nanstd(df_all['data'][i][2]))
            std_SON_cordex.append(np.nanstd(df_all['data'][i][3]))

std_DJF_cmip5=[]
std_MAM_cmip5=[]
std_JJA_cmip5=[]
std_SON_cmip5=[]
#ordre des saisons dans fichier(DJF,JJA,MAM,SON)
for i in position:
    if df_all.groupe[i]=='CMIP5':
        std_DJF_cmip5.append(np.nanstd(df_all['data'][i][0]))
        std_JJA_cmip5.append(np.nanstd(df_all['data'][i][1]))
        std_MAM_cmip5.append(np.nanstd(df_all['data'][i][2]))
        std_SON_cmip5.append(np.nanstd(df_all['data'][i][3]))






r_std_DJF_climex=[]
r_std_JJA_climex=[]
r_std_MAM_climex=[]
r_std_SON_climex=[]
for j in range(len(std_DJF_climex)):
    r_std_DJF_climex.append(std_DJF_climex[j]/std_DJF_obs)
    r_std_JJA_climex.append(std_JJA_climex[j]/std_JJA_obs)
    r_std_MAM_climex.append(std_MAM_climex[j]/std_MAM_obs)
    r_std_SON_climex.append(std_SON_climex[j]/std_SON_obs)

r_std_DJF_cordex=[]
r_std_JJA_cordex=[]
r_std_MAM_cordex=[]
r_std_SON_cordex=[]
for j in range(len(std_DJF_cordex)):
    r_std_DJF_cordex.append(std_DJF_cordex[j]/std_DJF_obs)
    r_std_JJA_cordex.append(std_JJA_cordex[j]/std_JJA_obs)
    r_std_MAM_cordex.append(std_MAM_cordex[j]/std_MAM_obs)
    r_std_SON_cordex.append(std_SON_cordex[j]/std_SON_obs)

r_std_DJF_cmip5=[]
r_std_JJA_cmip5=[]
r_std_MAM_cmip5=[]
r_std_SON_cmip5=[]
for j in range(len(std_DJF_cmip5)):
    r_std_DJF_cmip5.append(std_DJF_cmip5[j]/std_DJF_obs)
    r_std_JJA_cmip5.append(std_JJA_cmip5[j]/std_JJA_obs)
    r_std_MAM_cmip5.append(std_MAM_cmip5[j]/std_MAM_obs)
    r_std_SON_cmip5.append(std_SON_cmip5[j]/std_SON_obs)

plt.figure(1)
r_std_DJF=[r_std_DJF_climex,r_std_DJF_cordex,r_std_DJF_cmip5]
plt.ylabel('Rapport écart type')
plt.ylim(0.6,2.3)
labels=['ClimEX (50)','CORDEX (20)','CMIP5 (53)']
plt.boxplot(r_std_DJF,
            labels=labels,
            patch_artist=True,
            boxprops=dict(facecolor='darkgrey',color='k'),
            medianprops= dict(color='k'))

if b_pt == 'brute':
    plt.title(var+' (E_1)\nVariabilité interannuelle\n 1971-2000 DJF\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_E_1_b_variabilite_interannuelle_DJF_rstd_123_1971-2000',bbox_inches='tight')
else:
    plt.title(var+' (E_1)\nVariabilité interannuelle\n1971-2000 DJF\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_E_1_pt_variabilite_interannuelle_DJF_rstd_123_1971-2000',bbox_inches='tight')

plt.figure(2)
r_std_MAM=[r_std_MAM_climex,r_std_MAM_cordex,r_std_MAM_cmip5]
plt.ylabel('Rapport écart type')
plt.ylim(0.6,2.3)
labels=['ClimEX (50)','CORDEX (20)','CMIP5 (53)']
plt.boxplot(r_std_MAM,
            labels=labels,
            patch_artist=True,
            boxprops=dict(facecolor='darkgrey',color='k'),
            medianprops= dict(color='k'))

if b_pt == 'brute':
    plt.title(var+' (E_1)\nVariabilité interannuelle\n 1971-2000 MAM\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_E_1_b_variabilite_interannuelle_MAM_rstd_123_1971-2000',bbox_inches='tight')
else:
    plt.title(var+' (E_1)\nVariabilité interannuelle\n1971-2000 MAM\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_E_1_pt_variabilite_interannuelle_MAM_rstd_123_1971-2000',bbox_inches='tight')

plt.figure(3)
r_std_JJA=[r_std_JJA_climex,r_std_JJA_cordex,r_std_JJA_cmip5]
plt.ylabel('Rapport écart type')
plt.ylim(0.6,2.3)
labels=['ClimEX (50)','CORDEX (20)','CMIP5 (53)']
plt.boxplot(r_std_JJA,
            labels=labels,
            patch_artist=True,
            boxprops=dict(facecolor='darkgrey',color='k'),
            medianprops= dict(color='k'))

if b_pt == 'brute':
    plt.title(var+' (E_1)\nVariabilité interannuelle\n 1971-2000 JJA\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_E_1_b_variabilite_interannuelle_JJA_rstd_123_1971-2000',bbox_inches='tight')
else:
    plt.title(var+' (E_1)\nVariabilité interannuelle\n1971-2000 JJA\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_E_1_pt_variabilite_interannuelle_JJA_rstd_123_1971-2000',bbox_inches='tight')

plt.figure(4)
r_std_SON=[r_std_SON_climex,r_std_SON_cordex,r_std_SON_cmip5]
plt.ylabel('Rapport écart type')
plt.ylim(0.6,2.3)
labels=['ClimEX (50)','CORDEX (20)','CMIP5 (53)']
plt.boxplot(r_std_SON,
            labels=labels,
            patch_artist=True,
            boxprops=dict(facecolor='darkgrey',color='k'),
            medianprops= dict(color='k'))

if b_pt == 'brute':
    plt.title(var+' (E_1)\nVariabilité interannuelle\n 1971-2000 SON\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_E_1_b_variabilite_interannuelle_SON_rstd_123_1971-2000',bbox_inches='tight')
else:
    plt.title(var+' (E_1)\nVariabilité interannuelle\n1971-2000 SON\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_E_1_pt_variabilite_interannuelle_SON_rstd_123_1971-2000',bbox_inches='tight')
