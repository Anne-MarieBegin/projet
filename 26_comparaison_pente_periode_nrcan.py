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
import pandas as pd

var='tmoy'
stat1='nrcan'#référence
b_pt='posttraite'
s=3
saison=['DJF','JJA','MAM','SON']
rcp='rcp45'
path_obs=('/tank/begin/weighting/E_1/traite/obs/'+var)

files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j]))

df_obs=[]
for i in range(len(da_obs)):
    df_obs.append(pd.DataFrame(da_obs[i]))

x=np.arange(1988,2018)

fit_da_obs_1988_2017=[]
df_obs_sans_nan = [x for x in df_obs[0][s] if np.isnan(x) == False]
fit_da_obs_1988_2017.append(np.polyfit(x,df_obs_sans_nan,1)[0])#[0]pour obtenir la pente)

#saison[0] 3 nan saison[123] 2 nan
if s==0:
    x=np.arange(1973,2000)
else:
    x=np.arange(1972,2000)

fit_da_obs_1971_2000=[]
df_obs_sans_nan = [x for x in df_obs[1][s] if np.isnan(x) == False]
fit_da_obs_1971_2000.append(np.polyfit(x,df_obs_sans_nan,1)[0])#[0]pour obtenir la pente)
#saison[0] 3 nan saison[123] 2 nan


x=np.arange(1971,2018)

fit_da_obs_1971_2017=[]
df_obs_sans_nan = [x for x in df_obs[2][s] if np.isnan(x) == False]
fit_da_obs_1971_2017.append(np.polyfit(x,df_obs_sans_nan,1)[0])


plt.plot(np.arange(1988,2018),df_obs[0][s],'b',label='NRcan_1988_2017 pente='+str(round(fit_da_obs_1988_2017[0],4)))
plt.plot(np.arange(1971,2001),df_obs[1][s],'r.',label='NRcan_1971_2000 pente='+str(round(fit_da_obs_1971_2000[0],4)))
plt.plot(np.arange(1971,2018),df_obs[2][s],'k--',label='NRcan_1971_2017 pente='+str(round(fit_da_obs_1971_2017[0],4)))
plt.legend(framealpha=0.1)
plt.ylabel('Temp moyenne $\circ$C')
plt.title('Comparaison NRcan\n(E_1) pente différente période_'+saison[s],fontsize=15)
plt.savefig('/tank/begin/weighting/plots/'+var+'_E_1_comparaison_nrcan_pente_periode_'+saison[s],bbox_inches='tight')
