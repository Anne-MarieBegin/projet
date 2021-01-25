#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 14:34:30 2020

@author: begin

v20201217 cycle interannuel, cycle interannuel - tendance,rapport variance sans tendance,pente
v20201222 cycle interannuel,rapport variance avec tendance,pente (ajustement échelle)(corriger rapport écarttype pour variance)
v20210106 (brute et posttraitee) serie interannuel, rapport écart type,pente de la tendance(changer titre )

"""


import xarray as xr
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

var='tasmin'
#moyenne annuel 1971-2000
stat='moy_an_30_'

#b_pt='brute'
b_pt='posttraite'

#open files begin by stat
path=('/exec/begin/weighting/SE_1/'+b_pt+'/traite/'+var)
files = []
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and stat in i:
        files.append(i)
files.sort()

#open observation file begin with stat        
path_obs=('/exec/begin/weighting/SE_1/brute/traite/obs/'+var)
files_obs = []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat in i:
        files_obs.append(i)

#open datarray
da=[]
da_obs=[]
for j in range(0,(len(files))):
    da.append(xr.open_dataarray(path+'/'+files[j])-273.15)
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j]))

#add obs at the beginning of the list
da.insert(0,da_obs[0]) 

    
#determine the curve minus trend (function signal.detrend())
x_detrended=[]
for f in range(0,len(files)+1):
    x_detrended.append(signal.detrend(da[f]))
    
#calcul écart type courbe avec tendance
std_inter_annuel=[]
for g in range(0,len(files)+1):
    std_inter_annuel.append(da[g].std())

#calcul rapport écart type
rapport_std=[]
for h in range(0,len(files)+1):
    rapport_std.append(std_inter_annuel[h]/std_inter_annuel[0])

ans=['1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1997','1998','1999','2000']
sim=['Observations',
     'CMIP5_CanESM2_r1i1p1_rcp85',
     'CMIP5_MPI-ESM-LR_r1i1p1_rcp85',
     'CORDEX_CanESM2_CanRCM4_r1i1p1_NAM-22_rcp45',
     'CORDEX_CanESM2_CanRCM4_r1i1p1_NAM-44_rcp45',   
     'CORDEX_CanESM2_RCA4_r1i1p1_NAM-44_rcp85',
     'CORDEX_MPI-ESM-LR_CRCM5-UQAM_r1i1p1_NAM-44_rcp45',
     'CORDEX_MPI-ESM-LR_RegCM4_r1i1p1_NAM-22_rcp85',
     'CORDEX_MPI-ESM-LR_RegCM4_r1i1p1_NAM-44_rcp85',
     'ClimEx_CanESM2_CRCM5-Ouranos_kda_NAM-11_rcp85',
     'ClimEx_CanESM2_CRCM5-Ouranos_kex_NAM-11_rcp85',
     'Ouranos_CanESM2_CRCM5-Ouranos_r1i1p1_NAM-22_rcp85',
     'Ouranos_MPI-ESM-LR_CRCM5-Ouranos_r1i1p1_NAM-22_rcp45'
     ]

#plot interannual cycle
plt.figure(1)
plt.plot(ans,da[0],'--k',zorder=13)
plt.plot(ans,da[1],'r')
plt.plot(ans,da[2],'b')
plt.plot(ans,da[3],'g')
plt.plot(ans,da[4],'c')
plt.plot(ans,da[5],'m')
plt.plot(ans,da[6],'y')
plt.plot(ans,da[7],'grey')
plt.plot(ans,da[8],'hotpink')
plt.plot(ans,da[9],'orange')
plt.plot(ans,da[10],'dimgrey')
plt.plot(ans,da[11],'brown')
plt.plot(ans,da[12],'olive')
plt.legend(sim[:],bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=270)
plt.ylabel('Température ($^\circ$C)')
if var == 'tasmax':
    plt.ylim(4,15)
else:
    plt.ylim(-6,4)
if b_pt == 'brute':
    plt.title(var+'\nSérie annuelle 1971-2000*\nBrutes')
    plt.savefig('/exec/begin/weighting/plots/brute/'+var+'_SE_1_b_cycle_interannuel_1971-2000',bbox_inches='tight')
else:
    plt.title(var+'\nSérie annuelle 1971-2000*\nPost-traitées')
    plt.savefig('/exec/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_cycle_interannuel_1971-2000',bbox_inches='tight')

    
    
#plot rapport variance 
plt.figure(2)
plt.plot(sim[1], rapport_std[1], 'xg',markersize=12)
plt.plot(sim[2], rapport_std[2], 'xg',markersize=12)
plt.plot(sim[3], rapport_std[3], 'xg',markersize=12)
plt.plot(sim[4], rapport_std[4], 'xg',markersize=12)
plt.plot(sim[5], rapport_std[5], 'xg',markersize=12)
plt.plot(sim[6], rapport_std[6], 'xg',markersize=12)
plt.plot(sim[7], rapport_std[7], 'xg',markersize=12)
plt.plot(sim[8], rapport_std[8], 'xg',markersize=12)
plt.plot(sim[9], rapport_std[9], 'xg',markersize=12)
plt.plot(sim[10], rapport_std[10], 'xg',markersize=12)
plt.plot(sim[11], rapport_std[11], 'xg',markersize=12)
plt.plot(sim[12], rapport_std[12], 'xg',markersize=12)
plt.ylabel('Rapport écart type')
plt.xticks(rotation=270)
if var =='tasmax':
    plt.ylim(0.6,1.1)
else:
    plt.ylim(0.5,1.1)
if b_pt == 'brute':
    plt.title('Évaluation variabilité interannuelle\n'+var+'\nSérie annuelle 1971-2000*\nBrutes')
    plt.savefig('/exec/begin/weighting/plots/brute/'+var+'_SE_1_b_rapport_std_1971-2000',bbox_inches='tight')
else:
    plt.title('Évaluation variabilité interannuelle\n'+var+'\nSérie annuelle 1971-2000*\nPost-traitées')
    plt.savefig('/exec/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_rapport_std_1971-2000',bbox_inches='tight')


#méthode longue pour enlever courbe de tendance
#calcul équation pente
pente=[]  
oo=[]    
for i in range(0,len(files)+1):
    x=np.arange(1971,1999)
    y=da[i]
    m,b=np.polyfit(x,y,1)
    pente.append(m*10)#pente sur 10 ans
    oo.append(b)
    #plot courbe plus tendance
#    plt.figure(4)
#    plt.plot(ans,y,ans,m*x+b,'-k')
#    plt.xticks(rotation=270)
    
#calcul de y pour chaque x avec equation pente
yy=[[],[],[],[],[],[],[],[],[],[],[],[],[]]
for p in range(0,len(files)+1):
    for t in range(0,28):
        yy[p].append((pente[p]/10)*x[t]+oo[p])#(/10 pour compenser ligne 129)
        
#calcul de la courbe moins la tendance
detrend=[]
for g in range(0,len(files)+1):
    detrend.append(da[g]-yy[g])

#plot pente tendance sur 10 ans
plt.figure(3)
plt.plot(sim[:],pente[:],'.r',markersize=12)
plt.xticks(rotation=270)
plt.ylabel('Pente tendance ($^\circ$C / 10 ans)')
if var == 'tasmax':
    plt.ylim(0,0.7)
else:
    plt.ylim(0,0.7)
if b_pt == 'brute':
    plt.title(var+'\nSérie annuelle 1971-2000*\nBrutes')
    plt.savefig('/exec/begin/weighting/plots/brute/'+var+'_SE_1_b_pente_1971-2000',bbox_inches='tight')
else:
    plt.title(var+'\nSérie annuelle 1971-2000*\nPost-traitées')
    plt.savefig('/exec/begin/weighting/plots/posttraite/'+var+'_SE_1_pt_pente_1971-2000',bbox_inches='tight')
    
