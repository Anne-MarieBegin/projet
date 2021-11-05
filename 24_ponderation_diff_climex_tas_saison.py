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
stat1='30x4_1971_2000_'#référence
b_pt='posttraite'
s=0
saison=['DJF','JJA','MAM','SON']

path_obs=('/tank/begin/weighting/E_1/traite/obs/'+var)

files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j]))

df_obs=pd.DataFrame(da_obs[0])

##ouvrir tous les fichiers qui commence par stat1 
path_all=('/tank/begin/weighting/E_1/traite/'+b_pt+'/'+var)

files_all= []
for i in os.listdir(path_all):
    if os.path.isfile(os.path.join(path_all,i)) and stat1 in i:
        files_all.append(i)
        files_all.sort()

#ouvrir dataarray des fichiers qui commence par stat1
da_all=[]
for j in range(0,(len(files_all))):
    da_all.append(xr.open_dataarray(path_all+'/'+files_all[j])-273.15)

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
                   'data':pd.DataFrame(da_all[i])})

#faire dataframe avec dictionnaire
df_all=pd.DataFrame.from_dict(dictio)
df_all['iden']=df_all['groupe']+'_'+df_all['gcm']+'_'+df_all['rcm']+'_'+df_all['membre']+'_'+df_all['resolution']+'_'+df_all['rcp']

#calcul std observation
std_da_obs=np.nanstd(df_obs[0])

#calcul std groupe climex
std_climex=[]
climex_=[]
for i in range(len(da_all)):
    if df_all.groupe[i]=='ClimEx':
        std_climex.append(np.nanstd(df_all.data[i][s]))
        climex_.append(df_all.iden[i][-16:-13])
#calcul std tous l'ensemble
std_da_all=[]
for i in range(len(da_all)):
    std_da_all.append(np.nanstd(df_all.data[i][s]))

for c in range(0,50):
    diff_std_all=[]
    for j in range(len(da_all)):
        diff_std_all.append(abs(std_da_all[j]-std_climex[c]))
    
    w_all=[]
    for k in range(len(da_all)):
        if diff_std_all[k]==0:
            w_all.append(0)
        else:
            w_all.append(1/diff_std_all[k])
    sum_diff=np.sum(w_all)
    
    w_all_norm=[]
    for k in range(len(da_all)):
        w_all_norm.append(w_all[k]/sum_diff)
        
    df_w_all_norm=pd.DataFrame(w_all_norm)
    df_w_all_norm['iden']=df_all['iden']
    df_w_all_norm['g']=df_all['groupe']
    
#    if b_pt=='brute':
#        df_w_all_norm.to_csv('/tank/begin/weighting/resultats/pond_diff_'+climex_[c]+'_b_'+var+'_'+saison[s]+'.csv')
#    else:
#        df_w_all_norm.to_csv('/tank/begin/weighting/resultats/pond_diff_'+climex_[c]+'_pt_'+var+'_'+saison[s]+'.csv')
#    
    
    climex=[];climex_iden=[]
    cmip5=[];cmip5_iden=[]
    cordex=[];cordex_iden=[]
    co=['CORDEX','Ouranos']
    for k in range(len(df_w_all_norm)):
        if df_w_all_norm['g'][k]=='ClimEx':
            climex.append(df_w_all_norm[0][k])
            climex_iden.append(df_w_all_norm['iden'][k])
        if df_w_all_norm['g'][k]=='CMIP5':
            cmip5.append(df_w_all_norm[0][k])
            cmip5_iden.append(df_w_all_norm['iden'][k])
        for i in range(0,2):
            if df_w_all_norm['g'][k]==co[i]:
                cordex.append(df_w_all_norm[0][k])
                cordex_iden.append(df_w_all_norm['iden'][k])
    plt.figure(figsize=(25,5))
    for j in range(0,50):
       
        plt.xticks(rotation=270)
        
        plt.plot(cmip5_iden,cmip5,'.',color='b')
        plt.plot(cordex_iden,cordex,'.',color='r')
        plt.plot('ClimEx',climex[j],'.',color='grey')
    plt.ylim(0,0.75)
    plt.grid()
    if b_pt == 'brute':
        plt.title('Poids référence '+climex_[c]+'\n'+var+' variabilité interannuelle (E_1) 1971-2000 '+saison[s]+'\nBrutes',fontsize=30)
       # plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_E_1_b_pond_diff_'+climex_[c]+'_1971-2000_'+saison[s],bbox_inches='tight')
    else:
        plt.title('Poids référence '+climex_[c]+'\n'+var+' variabilité interannuelle (E_1)1971-2000 '+saison[s]+'\nPost-traitées',fontsize=30)
       # plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_E_1_pt_pond_diff_'+climex_[c]+'_1971-2000_'+saison[s],bbox_inches='tight')
