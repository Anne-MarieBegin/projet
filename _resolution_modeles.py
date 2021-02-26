#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:34:36 2019

@author: begin

v20201216 Ouvre fichier, sélectionne 1971-2000(moins 1995 1996 29 fev), fait une moyenne par année/mois, fait une moyenne sur le domaine, enregistre 

"""
import xclim as xc
from xclim import subset
import xarray as xr
import os
import time
import pandas as pd

var = 'tasmax' #changer ligne 58
b_pt='brute'# brute ou posttraite
SE='SE_1_CORDEX'#sous-ensemble
#open all files in repertory
dd=[]
path=('/tank/begin/weighting/'+SE+'/'+b_pt+'/'+var)  
#path=('/tank/begin/weighting/SE_1/brute/'+var)  #observations
files=os.listdir(path)
files.reverse()
for i in files:
    dd.append(path+'/'+i)
    
#Make dataset with all files
ds=[]
for j in range(0,len(files)):    
    ds.append(xr.open_mfdataset(dd[j]))

mod=[]
lat=[]
for j in range(0,len(ds)):
    mod.append({'modele':ds[j].model_id,'lat':ds[j].lat[0]-ds[j].lat[1],'lon':ds[j].lon[0]-ds[j].lon[1]})
    lat.append(ds[j].lat[0]-ds[j].lat[1])
df=pd.DataFrame.from_dict(mod)    
    