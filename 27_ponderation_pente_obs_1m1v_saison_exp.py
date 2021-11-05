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
stat1='30x4_1971_2017_'#référence
b_pt='posttraite'
s=3
saison=['DJF','JJA','MAM','SON']
rcp='rcp85'
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
df_all['combine']=df_all['groupe']+'_'+df_all['gcm']+'_'+df_all['rcm']
df_unique=np.unique(df_all['combine'])

#calcul moyenne observation
moy_da_obs=np.nanmean(df_obs[s])

x=np.arange(1971,2018)
df_obs_sans_nan = [x for x in df_obs[s] if np.isnan(x) == False]
fit_da_obs=np.polyfit(x,df_obs_sans_nan,1)[0]#[0]pour obtenir la pente

#calcul pente tendance tous l'ensemble selon rcp
fit_da_all=[]
identifiant=[]
complet=[]
for i in range(len(df_all)):
    if df_all.rcp[i]==rcp:
        sans_nan=[x for x in df_all.data[i][s] if np.isnan(x) == False]
        fit_da_all.append(np.polyfit(x,sans_nan,1)[0])#[0]pour obtenir la pente
        identifiant.append(df_all['combine'][i])
        complet.append(df_all['iden'][i])


#calcul de la différence entre simulation et observation        
diff_fit_all=[]
for j in range(len(fit_da_all)):
    diff_fit_all.append(abs(fit_da_all[j]-fit_da_obs))

fit_da_climex=[]
for i in range(len(df_all)):
    if df_all.groupe[i]=='ClimEx':
        sans_nan_climex=[x for x in df_all.data[i][s] if np.isnan(x) == False]
        fit_da_climex.append(np.polyfit(x,sans_nan_climex,1)[0])
diff_climex=[]
for j in range(len(fit_da_climex)):
    diff_climex.append(abs(fit_da_climex[j]-fit_da_obs))

sigma_d=(np.std(diff_climex))*np.sqrt(2)

#sigma_d=0.025


#calcul de l'exponentielle (poids) simulation
w_all=[]
for k in range(len(diff_fit_all)):
    w_all.append(np.exp(-(diff_fit_all[k]/sigma_d)**2))

#
##calcul somme des poids
sum_w=np.sum(w_all)
#
##calcul des poids normalisés
w_all_norm=[]
for k in range(len(diff_fit_all)):
    w_all_norm.append(w_all[k]/sum_w)
 
##dataframe avec poids normalisés
df_w_all_norm=pd.DataFrame(w_all_norm)
df_w_all_norm['iden']=identifiant
df_w_all_norm['identifiant']=complet
#dff=df_w_all_norm.sort_values(['identifiant']).reset_index()

##enregistrer poids normalisés
if b_pt=='brute':
    df_w_all_norm.to_csv('/tank/begin/weighting/pond_combine/pond_exp_pente_71_17_obs_b_'+var+'_'+saison[s]+'_'+rcp+'.csv')
else:
    df_w_all_norm.to_csv('/tank/begin/weighting/pond_combine/pond_exp_pente_71_17_obs_pt_'+var+'_'+saison[s]+'_'+rcp+'.csv')


#identifier gcm-RCM unique
combine=[[]for k in range(len(df_unique))]
combine_iden=[[]for k in range(len(df_unique))]

for k in range(len(df_w_all_norm)):  
    for i in range(len(df_unique)):
        if df_unique[i]==identifiant[k]:
            combine[i].append(df_w_all_norm[0][k])
            combine_iden[i].append(df_w_all_norm['iden'][k])
 
#plot            
plt.figure(figsize=(9,5))
axe=plt.axes()
axe.set_yscale('log')
axe.set_ylim(0.00001,1)
plt.grid()
plt.ylabel('Poids')
plt.xticks(rotation=270)

for i in range(len(df_unique)):
    for j in range(len(combine[i])):
        plt.plot(df_unique[i],combine[i][j],'.',color='b')
        if df_unique[i]=='ClimEx_CanESM2_CRCM5-Ouranos':
            plt.plot(df_unique[i],combine[i][j],'.',color='grey')
        if 'CORDEX'in df_unique[i]:
            plt.plot(df_unique[i],combine[i][j],'.',color='r')
        if 'Ouranos_'in df_unique[i]:
            plt.plot(df_unique[i],combine[i][j],'.',color='r')

if b_pt == 'brute':
    plt.title('Poids référence NRcan\n'+var+' pente tendance (E_1) 1971-2017_'+saison[s]+'_'+rcp+'\nBrutes\n sigma_d='+str(round(sigma_d,3)),fontsize=15)
    #plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_E_1_b_pond_exp_pente_obs_1m1v_1971-2017_'+saison[s]+'_'+rcp+'_sa_al',bbox_inches='tight')
else:
    plt.title('Poids référence NRcan\n'+var+' pente tendance (E_1) 1971-2017_'+saison[s]+'_'+rcp+'\nPost-traitées\nsigma_d='+str(round(sigma_d,3)),fontsize=15)
    #plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_E_1_pt_pond_exp_pente_obs_1m1v_1971-2017_'+saison[s]+'_'+rcp+'_sa_al',bbox_inches='tight')
