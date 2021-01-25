# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

v20201216 tracer carte domaine

"""
from mpl_toolkits.basemap import Basemap
import numpy as np
from netCDF4 import Dataset,num2date, date2num,date2index, MFDataset
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
import os


#open files in repertoire
dd=[]
path='/exec/begin/weighting/SE_1/brute/tasmin'

#file to see all domaine
all_dom='/crue/rondeau/cQ2/delivery_cQ2/cordex/v1.0/DIR/tasmax/CQ2_CLISIM_QUEBEC_XXX_TASMAX_CON_COR_CE2_RC4_R81_DIR_XXX_XXX_XXXXXX_XXX_MB_20190325-1831.nc'  

files=os.listdir(path)
for i in files:
    dd.append(path+'/'+i)
     
#Make dataset with all files
ds=[]
for j in range(0,len(files)):    
    ds.append(xr.open_mfdataset(dd[j])) 

#select one file (i=) to plot map with different resolution   
i=11

lon=ds[i].variables['lon'][:]
lat=ds[i].variables['lat'][:]    
data=ds[i].tasmin.groupby('time.month').mean('time')               
data_sel=data.isel(month=8)

#plot map with selection
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.coastlines()
ax.set_extent([-85, -55, 40, 65], crs=ccrs.PlateCarree())
plt.pcolormesh(lon, lat, data_sel,vmin=275, vmax=290)
plt.colorbar()
plt.title(files[i])
plt.annotate('lon=[-75,-80], lat=[45,50]', xy=(0.25, 0.5), xycoords='axes fraction')
#plt.savefig('/exec/begin/weighting/plots/brute/map_'+files[i]+'.png',bbox_inches='tight')
                
