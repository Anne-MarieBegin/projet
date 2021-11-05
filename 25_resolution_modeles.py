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
SE='E_1'#sous-ensemble

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
               
#calcul de la résolution moyenne
#avec exception pour valeur manquante append 3.6 information connue       
diff_moy=[]
for i in range(0,len(diff_lat)):
    try:
        diff_moy.append(round((diff_lat[i]+diff_lon[i])/2,2))
    except Exception as err:
        diff_moy.append(3.6)
        print(err)   

df=pd.DataFrame(diff_moy,files).reset_index()
df.to_csv('/tank/begin/weighting/resultats/resolution.csv')


