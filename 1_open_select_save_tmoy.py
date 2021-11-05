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
import matplotlib.pyplot as plt
var1 = 'tasmin' #changer ligne 59
var2='tasmax'
b_pt='posttraite'# brute ou posttraite
SE='E_2'#sous-ensemble
#open all files in repertory
dd1=[]
dd2=[]

#path1=('/tank/begin/weighting/'+SE+'/'+b_pt+'/'+var1) 
#path2=('/tank/begin/weighting/'+SE+'/'+b_pt+'/'+var2) 

path1=('/tank/begin/weighting/'+SE+'/obs/'+var1)  #observations 
path2=('/tank/begin/weighting/'+SE+'/obs/'+var2)  #observations 

files1=os.listdir(path1)
files1.sort()
for i in files1:
    dd1.append(path1+'/'+i)
    
#Make dataset with all files
ds1=[]
for j in range(len(files1)):    
    ds1.append(xr.open_mfdataset(dd1[j]))

files2=os.listdir(path2)
files2.sort()

for i in files2:
    dd2.append(path2+'/'+i)
    
#Make dataset with all files
ds2=[]
for j in range(len(files2)):    
    ds2.append(xr.open_mfdataset(dd2[j]))

ds=[]
for k in range(len(files1)):
    ds.append((ds1[k].tasmin+ds2[k].tasmax)/2)

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
for n in range(0,len(files1)):
    ds_p.append(subset.subset_gridpoint(ds[n], start_date= start_date, end_date=end_date))

#Monthly,year,season :  nothing,mean,std,var over the period
df=[]
ds_1=[];ds_2=[];ds_3=[]
list1=[];list2=[];list3=[]
for k in range(0,len(files1)):
    df.append(ds_p[k].groupby('time.season').mean('time'))

#Mean on region
    #condition according to the identifier of the dimension (lat,lon)
    print(df[k].dims)
    if df[k].dims[1]==('rlat'):

        ds_1.append(df[k].mean(dim=['rlat','rlon']))
        list1.append(k)

    elif df[k].dims[1]==('lat'):
        ds_2.append(df[k].mean(dim=['lat','lon']))
        list2.append(k)
        
    else:
        ds_3.append(df[k].mean(dim=['y','x']))
        list3.append(k)

#combine list dataarray
ds_4=ds_1+ds_2+ds_3
#dss=ds_4[0].to_dataframe()

#combine position
list4=list1+list2+list3

#create file name list with good order
file=[]
for t in range(0,len(files1)):
    file.append(files1[list4[t]])
   
#save dataarrays with same name as openning
for m in range(0,len(files1)):
   
    #ds_4[m].to_netcdf('/tank/begin/weighting/'+SE+'/traite/'+b_pt+'/tmoy/sai_'+str(start_date[0:4])+'_'+str(end_date[0:4])+'_'+file[m])
    ds_4[m].to_netcdf('/tank/begin/weighting/'+SE+'/traite/obs/tmoy/sai_'+str(start_date[0:4])+'_'+str(end_date[0:4])+'_'+file[m])
  
    print(file[m])
