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

var='tasmin'
#moyenne annuel 1971-2000
stat='moy_an_30_'
#b_pt='posttraite'
b_pt='posttraite'


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

#combiner liste des noms de fichier avec trois listes
files_totale = files_climex + files_cordex + files_cmip5

#combiner données dans la même liste
da_totale = da_climex + da_cordex + da_cmip5


#split files, construire dictionnaire
files_split=[]
dictio=[]
for i in range(0,len(files_totale)):
    files_split.append(files_totale[i].split('_'))
    dictio.append({'groupe':files_split[i][3],
                   'gcm':files_split[i][4],
                   'rcm':files_split[i][5],
                   'membre':files_split[i][6],
                   'resolution':files_split[i][7],
                   'rcp':files_split[i][8]}
                    )

#faire dataframe avec dictionnaire
df=pd.DataFrame.from_dict(dictio) 
#ajouter colonne avec nomentlature DEH
DEH=[]
for n in range(0,len(df)):
    real=(code_rcp[df.rcp[n]]+code_membre[df.membre[n]])[-3:]
    DEH.append(code_groupe[df.groupe[n]]+'_'+code_gcm[df.gcm[n]]+'_'+code_rcm[df.rcm[n]]+code_resolution[df.resolution[n]]+'_'+real)
df['DEH']=DEH

#créer dataframe avec rcp4.5
rcp=df['rcp']=='rcp45'
d45=df[rcp]
#ajouter indice 0 à ...
d45 = d45.reset_index()
#trier datatframe par membre
df45=d45.sort_values(['membre','resolution'],axis=0)
#creer colonne avec gcm_rcm
df45['gcm_rcm']=df45['gcm']+'_'+df45['rcm']#+'_'+df['membre']+'_'+df['resolution']                   
#sélectionner éléments uniques
dff45=(~df45['gcm_rcm'].duplicated()).astype(int)
#combiner colonne dff45 avec df45
frames=[df45,dff45]
frame=pd.concat(frames,axis=1)
#trier par gcm
df45_=frame.sort_values(['gcm','rcm','membre'],axis=0)
#enregistrer dataframe en csv
df45_.to_csv('/tank/begin/weighting/resultats/df_rcp45_1m1v_binaire.csv')

#créer dataframe avec rcp8.5
rcp=df['rcp']=='rcp85'
d85=df[rcp]
##ajouter indice 0 à ...
d85 = d85.reset_index()
#trier datatframe par membre
df85=d85.sort_values(['membre','resolution'],axis=0)
#creer colonne avec gcm_rcm
df85['gcm_rcm']=df85['gcm']+'_'+df85['rcm']
#sélectionner éléments uniques
dff85=(~df85['gcm_rcm'].duplicated()).astype(int)
#combiner colonne dff45 avec df45
frames=[df85,dff85]
frame=pd.concat(frames,axis=1)
#trier par gcm
df85_=frame.sort_values(['gcm','rcm','membre'],axis=0)
#enregistrer dataframe en csv
df85_.to_csv('/tank/begin/weighting/resultats/df_rcp85_1m1v_binaire.csv')



