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

var='pr'
stat1='sai_1981_2010_'#référence
stat2='sai_2041_2070_'
stat3='sai_2071_2100_'
b_pt='posttraite'
rcp='rcp45'

#saison n=position dans saison 0=DJF 1=JJA
s=3
saison=['DJF','JJA','MAM','SON']


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
    da_all.append(xr.open_dataarray(path_all+'/'+files_all[j])*86400)

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

        
########################################################################

#ouvrir tous les fichiers qui commence par stat2 
path_all2=('/tank/begin/weighting/E_1/'+b_pt+'/'+var)
files_all2= []
for i in os.listdir(path_all2):
    if os.path.isfile(os.path.join(path_all2,i)) and stat2 in i:
        files_all2.append(i)
        files_all2.sort()

#ouvrir dataarray des fichiers qui commence par stat2
da_all2=[]
for j in range(0,(len(files_all2))):
    da_all2.append(xr.open_dataarray(path_all2+'/'+files_all2[j])*86400)

#créer un dictionnaire avec dataarray 
files_totale=files_all2
files_split=[]
dictio2=[]
for i in range(0,len(files_totale)):
    files_split.append(files_totale[i].split('_'))
    dictio2.append({'groupe':files_split[i][3],
                   'gcm':files_split[i][4],
                   'rcm':files_split[i][5],
                   'membre':files_split[i][6],
                   'resolution':files_split[i][7],
                   'rcp':files_split[i][8],
                   'variable':files_split[i][9],
                   'files':files_totale[i],
                   'data':da_all2[i]})

#faire dataframe avec dictionnaire2
df2=pd.DataFrame.from_dict(dictio2) 

        
########################################################

#ouvrir tous les fichiers qui commence par stat3 
path_all3=('/tank/begin/weighting/E_1/'+b_pt+'/'+var)
files_all3= []
for i in os.listdir(path_all3):
    if os.path.isfile(os.path.join(path_all3,i)) and stat3 in i:
        files_all3.append(i)
        files_all3.sort()


#ouvrir dataarray des fichiers qui commence par stat3
da_all3=[]
for j in range(0,(len(files_all3))):
    da_all3.append(xr.open_dataarray(path_all3+'/'+files_all3[j])*86400)

#créer un dictionnaire avec dataarray 
files_totale=files_all3
files_split=[]
dictio3=[]
for i in range(0,len(files_totale)):
    files_split.append(files_totale[i].split('_'))
    dictio3.append({'groupe':files_split[i][3],
                   'gcm':files_split[i][4],
                   'rcm':files_split[i][5],
                   'membre':files_split[i][6],
                   'resolution':files_split[i][7],
                   'rcp':files_split[i][8],
                   'variable':files_split[i][9],
                   'files':files_totale[i],
                   'data':da_all3[i]})

#faire dataframe avec dictionnaire3
df3=pd.DataFrame.from_dict(dictio3) 

#données CMIP5 tcr et ecs tirées de Forster et al.2013
gcm=['ACCESS1-0','BCC-CSM1-1','BCC-CSM1-1-m','CanESM2','CCSM4','CNRM-CM5',
     'CSIRO-Mk3-6-0','FGOALS-s2','GFDL-CM3','GFDL-ESM2G','GFDL-ESM2M',
     'GISS-E2-H','GISS-E2-R','HadGEM2-ES','INMCM4','IPSL-CM5A-LR','IPSL-CM5B-LR',
     'MIROC5','MIROC-ESM','MPI-ESM-LR','MPI-ESM-P','MRI-CGCM3','NorESM1-M']
ecs=[3.83,2.82,2.87,3.69,2.89,3.25,4.08,4.17,3.97,2.39,2.44,2.31,2.11,
     4.59,2.08,4.13,2.61,2.72,4.67,3.63,3.45,2.60,2.80]
tcr=[2.0,1.7,2.1,2.4,1.8,2.1,1.8,2.4,2.0,1.10,1.30,1.7,1.5,2.5,1.3,
     2.0,1.5,1.5,2.2,2.0,2.0,1.6,1.4]

#changer pour ecs ou tcr(à changer titre figure et nom fichier)
test=tcr

#condition pour calculer delta qui correspond à la liste gcm
ii=[[]for k in range(len(gcm))]
for i in range(len(df1)):
    for j in range(len(gcm)):
        if (df1['gcm'][i]==gcm[j])&(df1['resolution'][i]=='NotApplicable')&(df1['rcp'][i]==rcp):
            print(i,gcm[j])
            ii[j].append((df2['data'][i][s]-df1['data'][i][s]))

#moyenne multi-membres
moy_delta_1=[]
for i in ii:
    moy_delta_1.append(np.mean(i))

#faire dataframe qui combine delta et tcr/ecs
df=pd.DataFrame(moy_delta_1,test).reset_index()
#ajouter colonne gcm
df['g']=gcm
#enlever les données nan
df_1=df.dropna().reset_index()

#scatter plot
plt.figure(1)
for i,z in enumerate(df_1['g']):
    x=df_1[0][i]
    y=df_1['index'][i]
    plt.scatter(x,y)
    #afficher étiquette
    plt.text(x+0.003,y+0.003,z) 

#calcul coefficient corrélation entre les points
cc=np.corrcoef(df_1[0],df_1['index']) 

#droite de tendance 
z = np.polyfit(df_1[0], df_1['index'], 1)
p = np.poly1d(z)
plb.plot(df_1[0], p(df_1[0]), '--k',linewidth=0.5)

plt.xlabel('Delta (mm/jour)')
plt.ylabel('Transient climate response (TCR) (K)') 
#plt.ylabel('Equilibrium climate sensitivity (ECS) (K)')
if b_pt=='brute':
    plt.title(var+'_'+saison[s]+'\n'+stat2[-10:-1]+'_'+rcp+'\nCoefficient corrélation ='+str(round(cc[0][1],3))+'\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_TCR_VS_delta_'+stat2[-10:-1]+'_'+rcp+'_'+saison[s],bbox_inches='tight')
else:
    plt.title(var+'_'+saison[s]+'\n'+stat2[-10:-1]+'_'+rcp+'\nCoefficient corrélation ='+str(round(cc[0][1],3))+'\nPost-traitées')  
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_TCR_VS_delta_'+stat2[-10:-1]+'_'+rcp+'_'+saison[s],bbox_inches='tight')


#condition pour calculer delta qui correspond à la liste gcm
ii=[[]for k in range(len(gcm))]
for i in range(len(df1)):
    for j in range(len(gcm)):
        if (df1['gcm'][i]==gcm[j])&(df1['resolution'][i]=='NotApplicable')&(df1['rcp'][i]==rcp):
            print(i,gcm[j])
            ii[j].append((df3['data'][i][s]-df1['data'][i][s]))

#moyenne multi-membres
moy_delta_2=[]
for i in ii:
    moy_delta_2.append(np.mean(i))

#faire dataframe qui combine delta et tcr/ecs
df=pd.DataFrame(moy_delta_2,test).reset_index()
#ajouter colonne gcm
df['g']=gcm
#enlever les données nan
df_2=df.dropna().reset_index()

plt.figure(2)
for i,z in enumerate(df_2['g']):
    x=df_2[0][i]
    y=df_2['index'][i]
    plt.scatter(x,y)
    #afficher étiquette
    plt.text(x+0.003,y+0.003,z) 

#calcul coefficient corrélation entre les points
cc=np.corrcoef(df_2[0],df_2['index']) 

#droite de tendance 
z = np.polyfit(df_2[0], df_2['index'], 1)
p = np.poly1d(z)
plb.plot(df_2[0], p(df_2[0]), '--k',linewidth=0.5)

plt.xlabel('Delta (mm/jour)')
plt.ylabel('Transient climate response (TCR) (K)') 
#plt.ylabel('Equilibrium climate sensitivity (ECS) (K)')
if b_pt=='brute':
    plt.title(var+'_'+saison[s]+'\n'+stat3[-10:-1]+'_'+rcp+'\nCoefficient corrélation ='+str(round(cc[0][1],3))+'\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_TCR_VS_delta_'+stat3[-10:-1]+'_'+rcp+'_'+saison[s],bbox_inches='tight')
else:
    plt.title(var+'_'+saison[s]+'\n'+stat3[-10:-1]+'_'+rcp+'\nCoefficient corrélation ='+str(round(cc[0][1],3))+'\nPost-traitées')  
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_TCR_VS_delta_'+stat3[-10:-1]+'_'+rcp+'_'+saison[s],bbox_inches='tight')
