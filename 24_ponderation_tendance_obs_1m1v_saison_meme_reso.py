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

var='tmoy'
stat1='30x4_1971_2000_'#référence
b_pt='posttraite'
s=3
saison=['DJF','JJA','MAM','SON']
rcp='rcp45'
path_obs=('/tank/begin/weighting/E_1/traite/obs_tous/'+var)

files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j]))

files_totale=files_obs
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
                   'data':pd.DataFrame(da_obs[i])})

#faire dataframe avec dictionnaire
df_obs=pd.DataFrame.from_dict(dictio)
df_obs['reso']=df_obs.gcm+'_'+df_obs.rcm+'_'+df_obs.resolution

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
    da_all.append(xr.open_dataarray(path_all+'/'+files_all[j])-273.15)

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
df_all['reso']=df_all.gcm+'_'+df_all.rcm+'_'+df_all.resolution
df_all['iden']=df_all['groupe']+'_'+df_all['gcm']+'_'+df_all['rcm']+'_'+df_all['membre']+'_'+df_all['resolution']+'_'+df_all['rcp']
df_all['combine']=df_all['groupe']+'_'+df_all['gcm']+'_'+df_all['rcm']
df_unique=np.unique(df_all['combine'])

#saison[0] 3 nan saison[123] 2 nan
if s==0:
    x=np.arange(1973,2000)
     
else:
    x=np.arange(1972,2000)
fit_da_obs=[]
for i in range(len(df_obs)):    
    df_obs_sans_nan = [x for x in df_obs.data[i][s] if np.isnan(x) == False]
    fit_da_obs.append(np.polyfit(x,df_obs_sans_nan,1)[0])#[0]pour obtenir la pente)

#calcul pente tendance tous l'ensemble selon rcp
fit_da_all=[]
identifiant=[]

for i in range(len(df_all)):
    
    sans_nan=[x for x in df_all.data[i][s] if np.isnan(x) == False]
    fit_da_all.append(np.polyfit(x,sans_nan,1)[0])#[0]pour obtenir la pente
    identifiant.append(df_all['combine'][i])

diff_moy_all=[]
identifiant=[]
for i in range(len(df_all)):
    for j in range(len(df_obs)):
        if df_all.rcp[i]==rcp:
            if df_all['reso'][i]==df_obs['reso'][j]:
                print(i,j)
                diff_moy_all.append(abs(fit_da_all[i]-fit_da_obs[j]))
                identifiant.append(df_all['combine'][i])


#calcul de 1/différence (poids) simulation
w_all=[]
for k in range(len(diff_moy_all)):
    if diff_moy_all[k]==0:
        w_all.append(0)
    else:
        w_all.append(1/diff_moy_all[k])

#calcul somme des poids
sum_diff=np.sum(w_all)

#calcul des poids normalisés
w_all_norm=[]
for k in range(len(diff_moy_all)):
    w_all_norm.append(w_all[k]/sum_diff)
 
#dataframe avec poids normalisés
df_w_all_norm=pd.DataFrame(w_all_norm)
df_w_all_norm['iden']=identifiant
#df_w_all_norm['g']=df_all['groupe']

#enregistrer poids normalisés
if b_pt=='brute':
    df_w_all_norm.to_csv('/tank/begin/weighting/resultats/pond_diff_pente_obs_b_'+var+'_'+saison[s]+'_'+rcp+'.csv')
else:
    df_w_all_norm.to_csv('/tank/begin/weighting/resultats/pond_diff_pente_obs_pt_'+var+'_'+saison[s]+'_'+rcp+'.csv')
   

#identifier gcm-RCM unique
combine=[[]for k in range(len(df_unique))]
combine_iden=[[]for k in range(len(df_unique))]

for k in range(len(df_w_all_norm)):  
    for i in range(len(df_unique)):
        if df_unique[i]==identifiant[k]:
            combine[i].append(df_w_all_norm[0][k])
            combine_iden[i].append(df_w_all_norm['iden'][k])
 
#plot            
plt.figure(figsize=(9,5))
axe=plt.axes()
axe.set_yscale('log')
axe.set_ylim(0.00001,1)
plt.grid()
plt.ylabel('Poids')
plt.xticks(rotation=270)

for i in range(len(df_unique)):
    for j in range(len(combine[i])):
        plt.plot(df_unique[i],combine[i][j],'.',color='b')
        if df_unique[i]=='ClimEx_CanESM2_CRCM5-Ouranos':
            plt.plot(df_unique[i],combine[i][j],'.',color='grey')
        if 'CORDEX'in df_unique[i]:
            plt.plot(df_unique[i],combine[i][j],'.',color='r')
        if 'Ouranos_'in df_unique[i]:
            plt.plot(df_unique[i],combine[i][j],'.',color='r')

if b_pt == 'brute':
    plt.title('Poids référence NRcan\n'+var+' pente tendance (E_1) 1971-2000_'+saison[s]+'_'+rcp+'\nBrutes',fontsize=15)
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_E_1_b_pond_diff_pente_obs_1971-2000_'+saison[s]+'_'+rcp,bbox_inches='tight')
else:
    plt.title('Poids référence NRcan\n'+var+' pente tendance (E_1) 1971-2000_'+saison[s]+'_'+rcp+'\nPost-traitées',fontsize=15)
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_E_1_pt_pond_diff_pente_obs_1971-2000_'+saison[s]+'_'+rcp,bbox_inches='tight')
