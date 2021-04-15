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
import matplotlib.pylab as plb

var='tasmin'
stat1='an_1981_2010_'#référence
b_pt='posttraite'
rcp='rcp85'


#ouvrir tous les fichiers qui commence par stat1 
path_all=('/tank/begin/weighting/E_1/'+b_pt+'/'+var)
files_all= []
for i in os.listdir(path_all):
    if os.path.isfile(os.path.join(path_all,i)) and stat1 in i:
        files_all.append(i)
        files_all.sort()

#ouvrir dataarray des fichiers qui commence par stat1
da_all=[]
for j in range(0,(len(files_all))):
    da_all.append(xr.open_dataarray(path_all+'/'+files_all[j])-273.15)

#créer un dictionnaire avec dataarray       
files_totale=files_all
files_split=[]
dictio=[]
for i in range(0,len(files_totale)):
    files_split.append(files_totale[i].split('_'))
    dictio.append({'groupe':files_split[i][3],
                   'gcm':files_split[i][4],
                   'rcm':files_split[i][5],
                   'membre':files_split[i][6],
                   'resolution':files_split[i][7],
                   'rcp':files_split[i][8],
                   'variable':files_split[i][9],
                   'files':files_totale[i],
                   'data':da_all[i]})

#faire dataframe avec dictionnaire
df1=pd.DataFrame.from_dict(dictio) 

pente=[]  
oo=[]    
for i in range(0,len(df1)):
    x=np.arange(1981,2009)
    y=df1['data'][i]
    m,b=np.polyfit(x,y,1)
    pente.append(m*10)#pente sur 10 ans
    oo.append(b)

#données CMIP5 tcr et ecs tirées de Forster et al.2013
gcm=['ACCESS1-0','BCC-CSM1-1','BCC-CSM1-1-m','CanESM2','CCSM4','CNRM-CM5',
     'CSIRO-Mk3-6-0','FGOALS-s2','GFDL-CM3','GFDL-ESM2G','GFDL-ESM2M',
     'GISS-E2-H','GISS-E2-R','HadGEM2-ES','INMCM4','IPSL-CM5A-LR','IPSL-CM5B-LR',
     'MIROC5','MIROC-ESM','MPI-ESM-LR','MPI-ESM-P','MRI-CGCM3','NorESM1-M']
ecs=[3.83,2.82,2.87,3.69,2.89,3.25,4.08,4.17,3.97,2.39,2.44,2.31,2.11,
     4.59,2.08,4.13,2.61,2.72,4.67,3.63,3.45,2.60,2.80]
tcr=[2.0,1.7,2.1,2.4,1.8,2.1,1.8,2.4,2.0,1.10,1.30,1.7,1.5,2.5,1.3,
     2.0,1.5,1.5,2.2,2.0,2.0,1.6,1.4]
#sélectionner les modeles globaux qui correspondent à la liste de Forster
#sélectionner rcp
#enregistrer les données saison dans une liste
ii=[[]for k in range(len(gcm))]
for i in range(len(df1)):
    for j in range(len(gcm)):
        if (df1['gcm'][i]==gcm[j])&(df1['resolution'][i]=='NotApplicable')&(df1['rcp'][i]==rcp):
            print(i,gcm[j])
            ii[j].append((pente[i]))
moy_pente=[]
for i in ii:
    moy_pente.append(np.mean(i))

#faire dataframe qui combine moy et tcr/ecs
df=pd.DataFrame(moy_pente,tcr).reset_index()
#ajouter colonne gcm
df['g']=gcm
#enlever les données nan
df_=df.dropna().reset_index()

#scatter plot
for i,z in enumerate(df_['g']):
    x=df_[0][i]
    y=df_['index'][i]
    plt.scatter(x,y)
    #afficher étiquette
    plt.text(x+0.03,y+0.03,z) 
#calcul coefficient corrélation entre les points
cc=np.corrcoef(df_[0],df_['index']) 
#droite de tendance 
z = np.polyfit(df_[0], df_['index'], 1)
p = np.poly1d(z)
plb.plot(df_[0], p(df_[0]), '--k',linewidth=0.5)

plt.xlabel('Pente ($\circ$C/10ans)')
plt.ylabel('Transient climate response (TCR) (K)') 
#plt.ylabel('Equilibrium climate sensitivity (ECS) (K)')
if b_pt=='brute':
    plt.title(var+'\n'+stat1[-10:-1]+'_'+rcp+'\nCoefficient corrélation ='+str(round(cc[0][1],3))+'\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_TCR_VS_pente_'+stat1[-10:-1]+'_'+rcp,bbox_inches='tight')
else:
    plt.title(var+'\n'+stat1[-10:-1]+'_'+rcp+'\nCoefficient corrélation ='+str(round(cc[0][1],3))+'\nPost-traitées')  
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_TCR_VS_pente_'+stat1[-10:-1]+'_'+rcp,bbox_inches='tight')
