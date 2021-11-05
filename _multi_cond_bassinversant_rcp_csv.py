#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:34:36 2019

@author: begin

"""
import xclim as xc
from xclim import subset
import xarray as xr
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
var = 'pr' #changer ligne 58
b_pt='brute'# brute ou posttraite
SE='SE_1_complet'#sous-ensemble

#open all files in repertory
dd=[]
path=('/tank/begin/weighting/'+SE+'/'+b_pt+'/'+var)  
#path=('/tank/begin/weighting/SE_1/brute/'+var)  #observations
files=os.listdir(path)
files.sort()
for i in files:
    dd.append(path+'/'+i)
    
#Make dataset with all files
ds=[]
for j in range(0,len(files)):    
    ds.append(xr.open_mfdataset(dd[j]))

#construire dictionnaire avec nom  de fichier pour faire dataframe
files_split=[]
dictio=[]
for i in range(0,len(files)):
    files_split.append(files[i].split('_'))
    dictio.append({'groupe':files_split[i][0],
                   'gcm':files_split[i][1],
                   'rcm':files_split[i][2],
                   'membre':files_split[i][3],
                   'resolution':files_split[i][4],
                   'rcp':files_split[i][5]}
                )

#faire dataframe avec dictionnaire
df=pd.DataFrame.from_dict(dictio)

#ajouter nomentlature DEH dans dataframe
DEH=[]
for n in range(0,len(df)):
    real = (code_rcp[df.rcp[n]]+code_membre[df.membre[n]])[-3:]
    DEH.append(code_groupe[df.groupe[n]]+'_'+code_gcm[df.gcm[n]]+'_'+code_rcm[df.rcm[n]]+code_resolution[df.resolution[n]]+'_'+real)
df['DEH']=DEH

#calcul distance en degre entre deux points de latitude
#avec exception pour valeur manquante
diff_lat=[]
for i in range(0,len(ds)):
    try:
        diff_lat.append(float(np.mean(ds[i].lat[1]-ds[i].lat[0])))
    except Exception as err:
        diff_lat.append(None)
        print(err)

#calcul distance en degre entre deux points de longitude
#avec exception grille NAM pas bonne valeur avec lon
        # a partir de 110 lon en 2D alors [:,1]
diff_lon=[]
for i in range(0,110):
    try:
        diff_lon.append(float(np.mean(ds[i].rlon[1]-ds[i].rlon[0])))
    except Exception as err:
        diff_lon.append(float(np.mean(ds[i].lon[1]-ds[i].lon[0])))
        print(err)
for i in range(110,len(ds)):
    try:
        diff_lon.append(float(np.mean(ds[i].rlon[1]-ds[i].rlon[0])))
    except Exception as err:
        diff_lon.append(float(np.mean(ds[i].lon[:,1]-ds[i].lon[:,0])))
        print(err)
               
#calcul de la distance en km des degres de latitude
#avec exception pour valeur manquante        
dis_lat=[]
for i in range(0,len(diff_lat)):
    try:
        dis_lat.append(round(diff_lat[i]*2*3.1416*6371/360,0))
    except Exception as err:
        dis_lat.append(None)
        print(err)   

#calcul de la distance en km des degres de longitude
#avec exception pour valeur manquante 
dis_lon=[]
for i in range(0,len(diff_lat)):
    try:
        dis_lon.append(round(diff_lon[i]*2*3.1416*6371/360,0))
    except Exception as err:
        dis_lon.append(None)
        print(err)    

#calcul distance moyenne entre lon et lat
#avec exception pour valeur manquante 
dis_moy=[]
for i in range(0,len(diff_lat)):
    try:
        dis_moy.append(round((dis_lat[i]+dis_lon[i])/2,0))
    except Exception as err:
        dis_moy.append(dis_lon[i])
        print(err)
        
###################################################################
#ajouter colonne avec distance moyenne dans dataframe
df['distance']=dis_moy
L=10000
#condition pour vecteur de 1 et 0
dis=((df['distance'] <= np.sqrt(L))&(df['rcp'] == 'rcp45')).astype(int)

#unifier le df et dis
frames=[df,dis]
dff=pd.concat(frames,axis=1)

#enregistrer csv dff
dff.to_csv('/tank/begin/weighting/resultats/df_rcp45_10000km2.csv')
