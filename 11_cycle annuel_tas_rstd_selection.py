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
import pandas as pd
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
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j]))

#open dataarray 50 membres climex 
da_climex=[]
for j in range(0,(len(files_climex))):
    da_climex.append(xr.open_dataarray(path_climex+'/'+files_climex[j])-273.15)

#open dataarray CORDEX
da_cordex=[]
for j in range(0,(len(files_cordex))):
    da_cordex.append(xr.open_dataarray(path_cordex+'/'+files_cordex[j])-273.15)

#open dataarray CMIP5
da_cmip5=[]
for j in range(0,(len(files_cmip5))):
    da_cmip5.append(xr.open_dataarray(path_cmip5+'/'+files_cmip5[j])-273.15)

files_totale = files_climex + files_cordex + files_cmip5

da_totale = da_climex + da_cordex + da_cmip5


#split files, construire dictionnaire, pour faire dataframe
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
                   'data':da_totale[i]})
df=pd.DataFrame.from_dict(dictio)    
df.value_counts(df['gcm']) 
#creer colonne avec variables combinés
df['combine']=df['gcm']+'_'+df['rcm']+'_'+df['membre']+'_'+df['resolution'] 

#déterminer liste des simulations uniques
l=[]
for i in range(0,len(files_split)):
    l.append(df['combine'][i])
l_unique=np.unique(l)

#déterminer position simulation unique
position= [ list(df['combine']).index(i) for i in list(l_unique)]

#selectionner position dans df
df_sel=df.iloc[position]

#sélectionner les données des différents groupe dans df_sel
#calculer std des données
groupe='CMIP5'
std_cmip5=[]
for i in position:
    if df_sel['groupe'][i]==groupe:
        std_cmip5.append(np.std(df_sel['data'][i]))

groupe='ClimEx'
std_climex=[]
for i in position:
    if df_sel['groupe'][i]==groupe:
        std_climex.append(np.std(df_sel['data'][i]))

groupe=['Ouranos','CORDEX'] #Ouranos inclus dans cordex
std_cordex=[]
for j in range(0,2):
    for i in position:
        if df_sel['groupe'][i]==groupe[j]:
            std_cordex.append(np.std(df_sel['data'][i]))

rstd_cmip5=[]
for j in range(0,len(std_cmip5)):
    rstd_cmip5.append(std_cmip5[j]/np.std(da_obs))
rstd_climex=[]
for j in range(0,len(std_climex)):
    rstd_climex.append(std_climex[j]/np.std(da_obs))       
rstd_cordex=[]
for j in range(0,len(std_cordex)):
    rstd_cordex.append(std_cordex[j]/np.std(da_obs))

datas=[rstd_climex,rstd_cordex,rstd_cmip5]
labels=['ClimEx (50)','Cordex (20)','CMIP5 (53)']
plt.boxplot(datas,labels=labels)
plt.ylabel('Rapport écart type')
if var == 'tasmax':
    plt.ylim(0.7,1.2)
else:
    plt.ylim(0.7,1.2)
if b_pt == 'brute':
    plt.title(var+'\nCycle annuel 1971-2000*\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_1_b_cycle_annuel_rstd_123_1971-2000',bbox_inches='tight')
else:
    plt.title(var+'\nCycle annuel 1971-2000*\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cycle_annuel_rstd_123_1971-2000',bbox_inches='tight')




