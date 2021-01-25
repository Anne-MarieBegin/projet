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

var='pr'
#moyenne annuel 1971-2000
stat='moy_an_30_'
#b_pt='posttraite'
b_pt='brute'

#open files begin by stat
path=('/tank/begin/weighting/SE_1/'+b_pt+'/traite/'+var)
files = []
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and stat in i:
        files.append(i)
files.sort()

#open observation file begin with stat        
path_obs=('/tank/begin/weighting/SE_1/brute/traite/obs/'+var)
files_obs = []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat in i:
        files_obs.append(i)

path_c=('/tank/begin/weighting/SE_1_climex/'+b_pt+'/traite/'+var)
files_c= []
for i in os.listdir(path_c):
    if os.path.isfile(os.path.join(path_c,i)) and stat in i:
        files_c.append(i)



#open datarray
da=[]
da_obs=[]
da_c=[]
for j in range(0,(len(files))):
    da.append(xr.open_dataarray(path+'/'+files[j])*86400)
del da[8:10]

for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j])*86400)
for j in range(0,(len(files_c))):
    da_c.append(xr.open_dataarray(path_c+'/'+files_c[j])*86400)
#add obs at the beginning of the list
da.insert(0,da_c[:]) 
da.insert(0,da_obs[0])

##calcul écart type courbe avec tendance
std=[]
for g in range(2,12):
    std.append(np.std(da[g])/np.std(da[0]))
std_c=[]
for g in range(0,50):
    std_c.append(np.std(da[1][g])/np.std(da[0]))



ans=['1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1997','1998','1999','2000']
sim=['Observations',
     'ClimEx(50)',
     'CMIP5_CanESM2_r1i1p1_rcp85',
     'CMIP5_MPI-ESM-LR_r1i1p1_rcp85',
     'CORDEX_CanESM2_CanRCM4_r1i1p1_NAM-22_rcp45',
     'CORDEX_CanESM2_CanRCM4_r1i1p1_NAM-44_rcp45',   
     'CORDEX_CanESM2_RCA4_r1i1p1_NAM-44_rcp85',
     'CORDEX_MPI-ESM-LR_CRCM5-UQAM_r1i1p1_NAM-44_rcp45',
     'CORDEX_MPI-ESM-LR_RegCM4_r1i1p1_NAM-22_rcp85',
     'CORDEX_MPI-ESM-LR_RegCM4_r1i1p1_NAM-44_rcp85',
     'Ouranos_CanESM2_CRCM5-Ouranos_r1i1p1_NAM-22_rcp85',
     'Ouranos_MPI-ESM-LR_CRCM5-Ouranos_r1i1p1_NAM-22_rcp45'
     ]
#
#plot interannual cycle
for y in range(0,50):
    plt.figure(1)
    plt.plot(ans,da[0],'--k',zorder=13)
    plt.plot(ans,da[1][y],'silver')
    plt.plot(ans,da[2],'r')
    plt.plot(ans,da[3],'b')
    plt.plot(ans,da[4],'g')
    plt.plot(ans,da[5],'c')
    plt.plot(ans,da[6],'m')
    plt.plot(ans,da[7],'y')
    plt.plot(ans,da[8],'grey')
    plt.plot(ans,da[9],'hotpink')
    plt.plot(ans,da[10],'brown')
    plt.plot(ans,da[11],'olive')

plt.legend(sim[:],bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=270)
plt.ylabel('Précipitation (mm/jour)')
plt.ylim(1.5,4.5)
if b_pt == 'brute':
    plt.title('Précipitation\nSérie annuelle 1971-2000*\nBrutes')
  #  plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_1_b_cycle_interannuel_climex_1971-2000',bbox_inches='tight')
else:
    plt.title('Précipitation\nSérie annuelle 1971-2000*\nPost-traitées')
    #plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cycle_interannuel_climex_1971-2000',bbox_inches='tight')
#
##plot rapport variance avec tendance
plt.figure(2)
for y in range(0,50):   
    plt.plot(sim[1], std_c[y], 'xg',markersize=12)
    plt.plot(sim[2],std[0],'xg',markersize=12)
    plt.plot(sim[3],std[1],'xg',markersize=12)
    plt.plot(sim[4],std[2],'xg',markersize=12)
    plt.plot(sim[5],std[3],'xg',markersize=12)
    plt.plot(sim[6],std[4],'xg',markersize=12)
    plt.plot(sim[7],std[5],'xg',markersize=12)
    plt.plot(sim[8],std[6],'xg',markersize=12)
    plt.plot(sim[9],std[7],'xg',markersize=12)
    plt.plot(sim[10],std[8],'xg',markersize=12)
    plt.plot(sim[11],std[9],'xg',markersize=12)

plt.ylabel('Rapport écart type')
plt.xticks(rotation=270)
plt.ylim(1,3)
if b_pt == 'brute':
    plt.title('Évaluation variabilité interannuelle\nPrécipitation\nSérie annuelle 1971_2000*\nBrutes')
    #plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_SE_1_b_rstd_climex_1971-2000',bbox_inches='tight')
else:
    plt.title('Évaluation variabilité interannuelle\nPrécipitation\nSérie annuelle 1971_2000*\nPost-traitées')
    #plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_rstd_climex_1971-2000',bbox_inches='tight')

    
#    
