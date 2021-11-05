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
import pandas as pd
from netCDF4 import Dataset,num2date, date2num,date2index, MFDataset
from time import gmtime, strftime
import numpy as np
var = 'pr' #changer ligne 59
b_pt='posttraite'# brute ou posttraite
SE='E_2'#sous-ensemble
#open all files in repertory
dd=[]
##path=('/tank/begin/weighting/'+SE+'/'+b_pt+'/'+var) #SE_1 complet
##path=('/tank/begin/weighting/'+SE+'/brute/obs/'+var) #observations E_1
path=('/tank/begin/weighting/'+SE+'/'+b_pt+'/'+var)  #E_1
#path=('/tank/begin/weighting/'+SE+'/obs/'+var)
#path=('/tank/begin/weighting/'+SE+'/obs_tous/'+var)  #observations E_2
files=os.listdir(path)
files.sort()
for i in files:
    dd.append(path+'/'+i)
    
#Make dataset with all files
ds=[]
for j in range(0,len(files)):    
    ds.append(xr.open_mfdataset(dd[j]))


#select period in dataset
ds_p=[]
start_date = '1970-12-01'
end_date = '2000-11-30'
for n in range(0,len(files)):
    d1 = subset.subset_time(ds[n], start_date= start_date,  end_date='1994-11-30')
    d2 = subset.subset_time(ds[n],  start_date='1997-03-01',  end_date=end_date)
    ds_p .append( xr.concat( [d1, d2] ,'time'))
#    ds_p.append(ds[n].sel(time=slice(start_date,end_date)))
   

#Monthly,year,season :  nothing,mean,std,var over the period
df=[]
ds_1=[];ds_2=[];ds_3=[]
list1=[];list2=[];list3=[]
for k in range(0,len(files)):
    df.append(ds_p[k].pr.resample(time='QS-DEC').mean(skipna=False))
   
#Mean ds.time.dt.season
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

ds_out=[]
for da in ds_4:
    #da=da.isel(time=slice(0,-1))#pour corrriger année incomplete
    new_time=pd.MultiIndex.from_product([pd.unique(da.time[1:].dt.year),['DJF','MAM','JJA','SON']],names=['year','season'])    
    da['time']=new_time
    ds_out.append(da.unstack('time'))

#combine position
list4=list1+list2+list3

#create file name list with good order
file=[]
for t in range(0,len(files)):
    file.append(files[list4[t]])
   
#save dataarrays with same name as openning
for m in range(0,len(files)):
   ## ds_4[m].to_netcdf('/tank/begin/weighting/E_1/obs/'+var+'/sai_'+str(start_date[0:4])+'_'+str(end_date[0:4])+'_'+file[m])
   ## ds_4[m].to_netcdf('/tank/begin/weighting/E_1/'+b_pt+'/'+var+'/sai_'+str(start_date[0:4])+'_'+str(end_date[0:4])+'_'+file[m])
    ds_out[m].to_netcdf('/tank/begin/weighting/'+SE+'/traite/'+b_pt+'/'+var+'/30x4_1971_2000_'+file[m])
    #ds_out[m].to_netcdf('/tank/begin/weighting/'+SE+'/traite/obs/'+var+'/30x4_1971_'+str(end_date[0:4])+'_'+file[m])
    #ds_out[m].to_netcdf('/tank/begin/weighting/'+SE+'/traite/obs_tous/'+var+'/30x4_1971_2000_'+file[m])
    print(file[m])
