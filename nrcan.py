#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 10:47:48 2021

@author: begin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
from xclim import subset



ds=xr.open_mfdataset('/tank/scenario/netcdf/nrcan/nrcan_canada_daily_v2/*/*.nc')
ds=ds.sel(time=slice('1970-01-01','2018-12-31'),lon=slice(-80,-75),lat=slice(50,45))
ds=ds.mean(['lat','lon'])

#1971-2000
#start_date = '1970-12-01'
#end_date = '2000-11-30'
#
#d1 = subset.subset_time(ds, start_date= start_date,  end_date='1994-11-30')
#d2 = subset.subset_time(ds,  start_date='1997-03-01',  end_date=end_date)
#ds=xr.concat( [d1, d2] ,'time')

start_date = '1987-12-01'
end_date = '2017-11-30'

ds = subset.subset_time(ds, start_date= start_date,  end_date=end_date)


ds=ds.resample(time='QS-DEC').mean(skipna=False)

new_time=pd.MultiIndex.from_product([pd.unique(ds.time[1:].dt.year),['DJF','MAM','JJA','SON']],names=['year','season'])    
ds['time']=new_time
ds_out=ds.unstack('time')

ds=((ds_out.tasmax+ds_out.tasmin)/2)-273.15
#df=pd.DataFrame(ds)
ds.to_netcdf('/tank/begin/weighting/E_1/traite/obs/tmoy/30x4_1988_2017_nrcan')
