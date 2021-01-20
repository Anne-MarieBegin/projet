#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:34:36 2019

@author: begin

v20201216 Ouvre fichier, sélectionne 1971-2000(moins 19951996 29 fev), fait une moyenne par année/mois, fait une moyenne sur le domaine, enregistre 

"""
import xclim as xc
from xclim import subset
import xarray as xr
import os

var = 'tasmax' #changer ligne 59
b_pt='posttraite'# brute ou posttraite
SE='SE_1'#sous-ensemble
#open all files in repertory
dd=[]
path=('/exec/begin/weighting/'+SE+'/'+b_pt+'/'+var)  
files=os.listdir(path)
files.reverse()
for i in files:
    dd.append(path+'/'+i)
    
#Make dataset with all files
ds=[]
for j in range(0,len(files)):    
    ds.append(xr.open_mfdataset(dd[j]))


dsr = []
for dd in ds:

    #on enleve les donnes de 1995 et 1996 des ds
    l_annees_a_enlever = [1995, 1996]
    ddr = dd.sel(time = ~dd.time.dt.year.isin(l_annees_a_enlever))

    # on enleve les 29 fevrier
    ddrr = ddr.sel(time = ~((ddr.time.dt.month == 2) & (ddr.time.dt.day == 29)))

    dsr.append(ddrr)
ds = dsr

#select period in dataset
ds_p=[]
start_date = '1971-01-01'
end_date = '2000-12-31'
for n in range(0,len(files)):
    ds_p.append(subset.subset_gridpoint(ds[n], start_date= start_date, end_date=end_date))

#Monthly,year :  nothing,mean,std,var over the period
df=[]
ds_1=[];ds_2=[];ds_3=[]
list1=[];list2=[];list3=[]
for k in range(0,len(files)):
    df.append(ds_p[k].tasmax.groupby('time.year').mean('time'))

#Mean on region
    #condition according to the identifier of the dimension (lat,lon)
    print(df[k].dims)
    if df[k].dims[1] == 'rlat':

        ds_1.append(df[k].mean(dim=['rlat','rlon']))
        list1.append(k)

    elif df[k].dims[1] == 'lat':
        ds_2.append(df[k].mean(dim=['lat','lon']))
        list2.append(k)
        
    else:
        ds_3.append(df[k].mean(dim=['y','x']))
        list3.append(k)

#combine list dataarray
ds_4=ds_1+ds_2+ds_3
dss=ds_4[0].to_dataframe()

#combine position
list4=list1+list2+list3

#create file name list with good order
file=[]
for t in range(0,len(files)):
    file.append(files[list4[t]])
   
#save dataarrays with same name as openning
for m in range(0,len(files)):
    ds_4[m].to_netcdf('/exec/begin/weighting/'+SE+'/'+b_pt+'/traite/'+var+'/moy_an_30_'+file[m])
    print(file[m])
