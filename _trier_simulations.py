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
                   'rcp':files_split[i][8],
                   'variable':files_split[i][9],
                   'files':files_totale[i],
                   'data':da_totale[i]})

#faire dataframe avec dictionnaire
df=pd.DataFrame.from_dict(dictio) 

#compter combien de simulation selon conditions   
df.value_counts((df['gcm']=='CanESM2')&(df['rcp']=='rcp85'))

dff=df.groupby(['gcm','rcp']).count()
n=df.groupby('gcm').size()
n.shape

#ajouter colonne dans dataframe avec variables combinés
#pour sélectionner les simulations uniques
df['combine']=df['gcm']+'_'+df['rcm']+'_'+df['membre']+'_'+df['resolution'] 

#déterminer liste des simulations uniques dans df.combine
l=[]
for i in range(0,len(files_split)):
    l.append(df['combine'][i])
l_unique=np.unique(l)

#déterminer position dans df  des simulations uniques (enregistrer indice de position)
position= [list(df['combine']).index(i) for i in list(l_unique)]

#faire un dataframe avec la sélection des rangées qui correspondent avec l'indice position dans df
df_sel=df.iloc[position]

groupe='CMIP5'
moy=[]
for i in position:
    if (df_sel['groupe'][i]==groupe) and (df_sel['gcm'][i]=='CanESM2'):
        moy.append(np.mean(df_sel['data'][i])-np.mean(da_obs))

moy_pond=[]
for j in range(0,len(moy)):
    moy_pond.append((moy[j]/len(moy)))
somme=np.sum(moy_pond)

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

#calculer rapport écart type sur les trois ensembles
rstd_cmip5=[]
for j in range(0,len(std_cmip5)):
    rstd_cmip5.append(std_cmip5[j]/np.std(da_obs))
rstd_climex=[]
for j in range(0,len(std_climex)):
    rstd_climex.append(std_climex[j]/np.std(da_obs))       
rstd_cordex=[]
for j in range(0,len(std_cordex)):
    rstd_cordex.append(std_cordex[j]/np.std(da_obs))



#obtenir la liste des gcms dans l_gcm
l=[]
for i in range(0,len(files_split)):
    l.append(files_split[i][4])
l_gcm=np.unique(l) 
#obtenir la liste des rcms dans g_rcm
l=[]
for i in range(0,len(files_split)):
    l.append(files_split[i][5])
l_rcm=np.unique(l)

#déterminer le nombre de simulation par gcm selon conditions
#créer liste multimembre selon condition (multi)
groupe='CMIP5'
rcp='rcp85'

multi=[]
simple=[]
for i in range(0,len(l_gcm)):
    print(l_gcm[i],len(df[(df.groupe==groupe)&(df.gcm ==l_gcm[i])&(df.rcp==rcp)]))   
    
    if len(df[(df.groupe==groupe)&(df.gcm ==l_gcm[i])&(df.rcp==rcp)]) >1:
        multi.append(l_gcm[i])
        print(multi)
    #enregistrer data modèles une seul réalisation
    if len(df[(df.groupe==groupe)&(df.gcm ==l_gcm[i])&(df.rcp==rcp)]) ==1:
        simple.append(df['data'][i])
        

#enregistrer data provenant multi modèle
gcm=multi
data_load=[]
for t in range(0,len(multi)):
    data=[]
    for i in range(0,len(files_split)):
        if (df['groupe'][i]==groupe and df['gcm'][i] == gcm[t] and df['rcp'][i] == rcp):
            data.append(df['data'][i])
          #calcul rapport écart type data
            rstd=[]
            for x in range(0,len(data)):
                rstd.append(np.std(data[x])/np.std(da_obs))
               # np.save('/tank/begin/weighting/SE_1_multi/rstd_multi_'+groupe+'_'+gcm[t]+'_'+rcp,rstd)
     #open all data save  
    #data_load.append(np.load('/tank/begin/weighting/SE_1_multi/rstd_multi_'+groupe+'_'+gcm[t]+'_'+rcp+'.npy'))

rstd_simple=[]
for y in range(0,len(simple)):
    rstd_simple.append(np.std(simple[y])/np.std(da_obs))

rstd_cmip5=[]
for y in range(0,len(da_cmip5)):
    rstd_cmip5.append(np.std(da_cmip5[y])/np.std(da_obs))      




#retourne indice selon condition  
df[(df.gcm=='MPI-ESM-LR')&(df.rcp=='rcp85')]['rcm']

   