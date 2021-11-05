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

var='pr'
stat1='30x4_1971_2000_'#référence
b_pt='posttraite'
s=0
#saison=['DJF','JJA','MAM','SON']
rcp='rcp45'
path_obs=('/tank/begin/weighting/E_1/traite/obs/'+var)

files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j])*86400)

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
    da_all.append(xr.open_dataarray(path_all+'/'+files_all[j])*86400)

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
#moy_da_obs=np.nanmean(df_obs[s])
#
#
##calcul moyenne tous l'ensemble selon rcp
moy_da_all=[]
identifiant=[]
for i in range(len(df_all)):
    if df_all.rcp[i]==rcp:
        moy_da_all.append(np.nanmean(df_all.data[i][s]))
        identifiant.append(df_all['combine'][i])


##ouverture fichiers de poids non-normalisés
if b_pt == 'brute':
    df_exp_djf_pr=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_b_pr_DJF_'+rcp+'.csv')
    df_exp_mam_pr=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_b_pr_MAM_'+rcp+'.csv')
    df_exp_jja_pr=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_b_pr_JJA_'+rcp+'.csv')
    df_exp_son_pr=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_b_pr_SON_'+rcp+'.csv')
    
    df_exp_djf_tmoy=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_b_tmoy_DJF_'+rcp+'.csv')
    df_exp_mam_tmoy=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_b_tmoy_MAM_'+rcp+'.csv')
    df_exp_jja_tmoy=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_b_tmoy_JJA_'+rcp+'.csv')
    df_exp_son_tmoy=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_b_tmoy_SON_'+rcp+'.csv')

    #df_1m1v=pd.read_csv('/tank/begin/weighting/resultats/df_'+rcp+'_1m1v_uniforme.csv',delimiter=';',header=2)
else:
    df_exp_djf_pr=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_pt_pr_DJF_'+rcp+'.csv')
    df_exp_mam_pr=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_pt_pr_MAM_'+rcp+'.csv')
    df_exp_jja_pr=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_pt_pr_JJA_'+rcp+'.csv')
    df_exp_son_pr=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_pt_pr_SON_'+rcp+'.csv')
    
    df_exp_djf_tmoy=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_pt_tmoy_DJF_'+rcp+'.csv')
    df_exp_mam_tmoy=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_pt_tmoy_MAM_'+rcp+'.csv')
    df_exp_jja_tmoy=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_pt_tmoy_JJA_'+rcp+'.csv')
    df_exp_son_tmoy=pd.read_csv('/tank/begin/weighting/resultats/pond_exp_sigmadx2_mc_obs_pt_tmoy_SON_'+rcp+'.csv')

    #df_1m1v=pd.read_csv('/tank/begin/weighting/resultats/df_'+rcp+'_1m1v_uniforme.csv',delimiter=';',header=2)

#df_1m1v['iden']=df_1m1v['groupe']+'_'+df_1m1v['gcm']+'_'+df_1m1v['rcm']
#dff_1m1v=df_1m1v.sort_values(['iden','membre']).reset_index()

w_exp_djf_pr=df_exp_djf_pr['0']
w_exp_mam_pr=df_exp_mam_pr['0']
w_exp_jja_pr=df_exp_jja_pr['0']
w_exp_son_pr=df_exp_son_pr['0']

w_exp_djf_tmoy=df_exp_djf_tmoy['0']
w_exp_mam_tmoy=df_exp_mam_tmoy['0']
w_exp_jja_tmoy=df_exp_jja_tmoy['0']
w_exp_son_tmoy=df_exp_son_tmoy['0']
#w_exp_pente=df_exp_pente['0']
#w_1m1v=dff_1m1v['1m1v_uniforme']
w_exp=[]
for i in range(len(w_exp_djf_pr)):
    w_exp.append(w_exp_djf_pr[i]*w_exp_djf_tmoy[i]*w_exp_mam_pr[i]*w_exp_mam_tmoy[i]*w_exp_jja_pr[i]*w_exp_jja_tmoy[i]*w_exp_son_pr[i]*w_exp_son_tmoy[i])
                   
sum_exp=np.sum(w_exp)

w_exp_norm=[]
for j in range(len(w_exp)):
    w_exp_norm.append(w_exp[j]/sum_exp)

df_w_all_norm=pd.DataFrame(w_exp_norm)
df_w_all_norm['iden']=identifiant

#dff=df_w_all_norm.sort_values(['identifiant']).reset_index()

##enregistrer poids normalisés
if b_pt=='brute':
    df_w_all_norm.to_csv('/tank/begin/weighting/pond_combine/pond_mixte_sigmadx2_mc_DJF+MAM+JJA+SON_obs_b_tmoy_pr_'+rcp+'.csv')
else:
    df_w_all_norm.to_csv('/tank/begin/weighting/pond_combine/pond_mixte_sigmadx2_mc_DJF+MAM+JJA+SON_obs_pt_tmoy_pr_'+rcp+'.csv')


#identifier gcm-RCM unique
combine=[[]for k in range(len(df_unique))]
combine_iden=[[]for k in range(len(df_unique))]

for k in range(len(w_exp)):  
    for i in range(len(df_unique)):
        if df_unique[i]==identifiant[k]:
            combine[i].append(w_exp_norm[k])
            #combine_iden[i].append(df_w_all_norm['iden'][k])
 
#plot            
plt.figure(figsize=(9,5))
axe=plt.axes()
axe.set_yscale('log')
axe.set_ylim(10e-6,1)
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
    plt.title('Poids référence NRcan\ntmoy_pr sigmadx2_mc_DJF+MAM+JJA+SON (E_1)_'+rcp+'\nBrutes',fontsize=15)
    plt.savefig('/tank/begin/weighting/plots/brute/tmoy_pr_E_1_b_pond_mixte_sigmadx2_mc_DJF+MAM+JJA+SON_obs_'+rcp,bbox_inches='tight')
else:
    plt.title('Poids référence NRcan\ntmoy_pr sigmadx2_mc_DJF+MAM+JJA+SON (E_1)_'+rcp+'\nPost-traitées',fontsize=15)
    plt.savefig('/tank/begin/weighting/plots/posttraite/tmoy_pr_E_1_pt_pond_mixte_sigmadx2_mc_DJF+MAM+JJA+SON_obs_'+rcp,bbox_inches='tight')
