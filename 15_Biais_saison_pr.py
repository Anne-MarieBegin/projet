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
stat1='sai_1981_2010_'#référence
b_pt='posttraite'

#saison n=position dans saison 0=DJF 1-JJA
n=3
saison=['DJF','JJA','MAM','SON']

path_obs=('/tank/begin/weighting/E_1/obs/'+var)
files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j])*86400)


#ouvrir tous les fichiers qui commence par stat1 
path_all=('/tank/begin/weighting/E_1/'+b_pt+'/'+var)
files_all= []
for i in os.listdir(path_all):
    if os.path.isfile(os.path.join(path_all,i)) and stat1 in i:
        files_all.append(i)
        files_all.sort()

#ouvrir dataarray des fichiers qui commence par stat1
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
df=pd.DataFrame.from_dict(dictio) 
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
groupe='ClimEx'
b_climex=[]
for i in position:
    if df_sel['groupe'][i]==groupe:
        b_climex.append((df_sel['data'][i][n]-da_obs[0][n]))

groupe=['Ouranos','CORDEX'] #Ouranos inclus dans cordex
b_cordex=[]
for j in range(0,2):
    for i in position:
        if df_sel['groupe'][i]==groupe[j]:
            b_cordex.append((df_sel['data'][i][n]-da_obs[0][n]))

groupe='CMIP5'
b_cmip5=[]
for i in position:
    if df_sel['groupe'][i]==groupe:
        b_cmip5.append((df_sel['data'][i][n]-da_obs[0][n]))
  
biais=[b_climex,b_cordex,b_cmip5]
labels=['ClimEx (50)','CORDEX (20)','CMIP5 (53)']
plt.boxplot(biais,labels=labels)
plt.ylabel('biais (mm/jour)')
plt.ylim(-2,2)
if b_pt=='brute':
    plt.title(var+'\n'+stat1[4::]+saison[n]+'\nBrutes')
    #plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_E_1_biais'+stat1[3::]+'_'+saison[n],bbox_inches='tight')   
else:
    plt.title(var+'\n'+stat1[4::]+saison[n]+'\nPost-traitées')
   #plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_E_1_biais'+stat1[3::]+'_'+saison[n],bbox_inches='tight') 
