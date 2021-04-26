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
stat1='sai_1981_2010_'#référence
stat2='sai_2041_2070_'
stat3='sai_2071_2100_'
b_pt='posttraite'
rcp='rcp85'

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
    da_all2.append(xr.open_dataarray(path_all2+'/'+files_all2[j])-273.15)

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
    da_all3.append(xr.open_dataarray(path_all3+'/'+files_all3[j])-273.15)

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

#liste GCM et RCM
GCM=np.unique(df2['gcm'])
RCM=np.unique(df2['rcm'])

#enregistrer data pour condition
#trier par GCM modèle globaux et rcp
gcm_data=[[]for k in range(len(GCM))]
for i in range(len(df2)):
    for j in range(len(GCM)):
        if df2['gcm'][i] == GCM[j] and df2['rcp'][i]==rcp and df2['rcm'][i]=='NotApplicable':
            gcm_data[j].append(df2['data'][i][s])
           # print(i,df1['rcm'][i])

#faire moyenne des datas des modèles globaux
moy=[]            
for i in gcm_data:
    moy.append(np.mean(i))

#dataframe moyenne et GCM
df=pd.DataFrame(moy,GCM).reset_index() 
plt.figure(1)
#sélectionner rcm qui correspond au gcm
rcm_data=[[]for k in range(len(GCM))]
df_data=[[]for k in range(len(GCM))]
for i in range(len(df2)):
    for j in range(len(df)):
        if df2['gcm'][i] == df['index'][j] and df2['rcm'][i]!='NotApplicable'and df2['rcp'][i]==rcp:
            rcm_data[j].append(df2['data'][i][s])
            df_data[j].append(df[0][j])
            
            #plot gcm vs rcm
            if df2['groupe'][i]=='ClimEx':
                color='grey'
            else:
                color='b'
            plt.scatter(df2['data'][i][s],df[0][j],c=color)
t_gcm=[]
t_rcm=[]
for i in range(len(rcm_data)):  
    for j in range(len(rcm_data[i])):
        if not np.isnan (df_data[i][j]):
            t_gcm.append(df_data[i][j])
            t_rcm.append(rcm_data[i][j])
cc=np.corrcoef(t_rcm,t_gcm)
            
plt.xlabel('température du RCM ($\circ$C)')
plt.ylabel('température du GCM ($\circ$C)')
           
if b_pt=='brute':
    plt.title(var+'_'+stat2[-10:-1]+'_'+saison[s]+'_'+rcp+'\ncoefficient corélation='+str(round(cc[0][1],3))+'\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_GCM_vs_RCM_'+stat2[-10:-1]+'_'+rcp+'_'+saison[s],bbox_inches='tight')
else:
    plt.title(var+'_'+stat2[-10:-1]+'_'+saison[s]+'_'+rcp+'\ncoefficient corélation='+str(round(cc[0][1],3))+'\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_GCM_vs_RCM_'+stat2[-10:-1]+'_'+rcp+'_'+saison[s],bbox_inches='tight')

#liste GCM et RCM
GCM=np.unique(df3['gcm'])
RCM=np.unique(df3['rcm'])

#enregistrer data pour condition
#trier par GCM modèle globaux et rcp
gcm_data=[[]for k in range(len(GCM))]
for i in range(len(df3)):
    for j in range(len(GCM)):
        if df3['gcm'][i] == GCM[j] and df3['rcp'][i]==rcp and df3['rcm'][i]=='NotApplicable':
            gcm_data[j].append(df3['data'][i][s])
           # print(i,df1['rcm'][i])

#faire moyenne des datas des modèles globaux
moy=[]            
for i in gcm_data:
    moy.append(np.mean(i))

#dataframe moyenne et GCM
df=pd.DataFrame(moy,GCM).reset_index() 

#sélectionner rcm qui correspond au gcm
plt.figure(2)
rcm_data=[[]for k in range(len(GCM))]
df_data=[[]for k in range(len(GCM))]
for i in range(len(df3)):
    for j in range(len(df)):
        if df3['gcm'][i] == df['index'][j] and df3['rcm'][i]!='NotApplicable'and df3['rcp'][i]==rcp:
            rcm_data[j].append(df3['data'][i][s])
            df_data[j].append(df[0][j])
            
            #plot gcm vs rcm
            if df2['groupe'][i]=='ClimEx':
                color='grey'
            else:
                color='b'
            plt.scatter(df3['data'][i][s],df[0][j],c=color)
t_gcm=[]
t_rcm=[]
for i in range(len(rcm_data)):  
    for j in range(len(rcm_data[i])):
        if not np.isnan (df_data[i][j]):
            t_gcm.append(df_data[i][j])
            t_rcm.append(rcm_data[i][j])
cc=np.corrcoef(t_rcm,t_gcm)
            
plt.xlabel('température du RCM ($\circ$C)')
plt.ylabel('température du GCM ($\circ$C)')
           
if b_pt=='brute':
    plt.title(var+'_'+stat3[-10:-1]+'_'+saison[s]+'_'+rcp+'\ncoefficient corélation='+str(round(cc[0][1],3))+'\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_GCM_vs_RCM_'+stat3[-10:-1]+'_'+rcp+'_'+saison[s],bbox_inches='tight')
else:
    plt.title(var+'_'+stat3[-10:-1]+'_'+saison[s]+'_'+rcp+'\ncoefficient corélation='+str(round(cc[0][1],3))+'\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_GCM_vs_RCM_'+stat3[-10:-1]+'_'+rcp+'_'+saison[s],bbox_inches='tight')
