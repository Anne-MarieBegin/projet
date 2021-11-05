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
stat1='an_1971_2000_'#référence
b_pt='posttraite'


path_obs=('/tank/begin/weighting/E_1/traite/obs/'+var)

files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j])*86400)



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
                   'data':da_all[i]})

#faire dataframe avec dictionnaire
df_all=pd.DataFrame.from_dict(dictio)
df_all['iden']=df_all['groupe']+'_'+df_all['gcm']+'_'+df_all['rcm']+'_'+df_all['membre']+'_'+df_all['resolution']+'_'+df_all['rcp']

#calcul std observation
std_da_obs=np.std(da_obs[0])

#calcul std groupe climex
std_climex=[]
climex=[]
for i in range(len(da_all)):
    if df_all.groupe[i]=='ClimEx':
        std_climex.append(np.std(da_all[i]))
        climex.append(df_all.iden[i][-16:-13])

#calcul std tous l'ensemble
std_da_all=[]
for i in range(len(da_all)):
    std_da_all.append(np.std(da_all[i]))

#c sélectionne le membre de climex
c=0
#calcul la différence entre les écarts types
diff_std_all=[]
for j in range(len(da_all)):
    diff_std_all.append(abs(std_da_all[j]-std_climex[c]))

#gere le zéro créer par l'utilisation d'un membre de climex
#calcul 1 sur la différence (le poid)
w_all=[]
for k in range(len(da_all)):
    if diff_std_all[k]==0:
        w_all.append(0)
    else:
        w_all.append(1/diff_std_all[k])
sum_diff=np.sum(w_all)

#calcul les poids normalisés
w_all_norm=[]
for k in range(len(da_all)):
    w_all_norm.append(w_all[k]/sum_diff)

#dataframe avec les poids normalisés ajout de la colonne identifiant    
df_w_all_norm=pd.DataFrame(w_all_norm)
df_w_all_norm['iden']=df_all['iden']

#enregistrer dataframe pour traitement ultérieur
df_w_all_norm.to_csv('/tank/begin/weighting/resultats/pond_diff_'+climex[c]+'_'+var+'.csv')

plt.figure(figsize=(35,5))
plt.xticks(rotation=270)
plt.plot(df_all['iden'],w_all_norm,'.')
#plt.ylabel('poids')
plt.grid()
if b_pt == 'brute':
    plt.title('Poids référence '+climex[c]+'\n'+var+' (E_1) 1971-2000\nBrutes',fontsize=34)
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_E_1_b_pond_diff_'+climex[c]+'_1971-2000',bbox_inches='tight')
else:
    plt.title('Poids référence '+climex[c]+'\n'+var+' (E_1)1971-2000\nPost-traitées',fontsize=34)
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_E_1_pt_pond_diff_'+climex[c]+'_1971-2000',bbox_inches='tight')
