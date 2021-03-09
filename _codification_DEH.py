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
import _code

var='tasmin'
stat1='sai_1981_2010_'#référence
b_pt='posttraite'

#saison n=position dans saison 0=DJF 1-JJA
n=0
saison=['DJF','JJA','MAM','SON']

path_obs=('/tank/begin/weighting/E_1/obs/'+var)
files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j]))


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
    da_all.append(xr.open_dataarray(path_all+'/'+files_all[j])-273.15)

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
#n=56
save=('/tank/begin/weighting/test/')
for n in range(0,len(df)):
    real=(code_rcp[df.rcp[n]]+code_membre[df.membre[n]])[-3:]
    np.save(save+code_groupe[df.groupe[n]]+'_'+code_gcm[df.gcm[n]]+'_'+code_rcm[df.rcm[n]]+code_resolution[df.resolution[n]]+'_'+real,df)
    np.save(save+df.groupe[n]+'_'+df.gcm[n]+'_'+df.rcm[n]+'_'+df.resolution[n]+'_'+df.rcp[n]+'_'+df.membre[n],df)