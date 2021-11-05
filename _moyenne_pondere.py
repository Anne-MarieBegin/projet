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

var='tasmax'
stat1='sai_1981_2010_'#référence
stat2='sai_2041_2070_'
stat3='sai_2071_2100_'
b_pt='posttraite'
rcp='rcp85'
#saison n=position dans saison 0=DJF 1=JJA
s=0
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

#trouver position selon condition rcp
position=[]
for i in range(0,len(df1)):
    if df1.rcp[i]==rcp:
        position.append(i)
        
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

#trouver position selon condition rcp
position2=[]
for i in range(0,len(df2)):
    if df2.rcp[i]==rcp:
        position2.append(i)
        
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

#trouver position selon condition rcp
position3=[]
for i in range(0,len(df3)):
    if df3.rcp[i]==rcp:
        position3.append(i)



#s pour saison
#calcul moyenne pondérée bassin versant 10000km²
df_bv=pd.read_csv('/tank/begin/weighting/resultats/df_'+rcp+'_10000km2.csv')
wi=df_bv['0']
moyi=[]
for i in range(0,len(df1)):
    moyi.append(df1['data'][i][s]*wi[i])
moy_pond_10000_1=(np.sum(moyi))/np.sum(wi)

moyi=[]
for i in range(0,len(df2)):
    moyi.append(df2['data'][i][s]*wi[i])
moy_pond_10000_2=(np.sum(moyi))/np.sum(wi)

moyi=[]
for i in range(0,len(df3)):
    moyi.append(df3['data'][i][s]*wi[i])
moy_pond_10000_3=(np.sum(moyi))/np.sum(wi)

#s pour saison
#calcul moyenne pondérée 1m1v uniforme
df_u=pd.read_csv('/tank/begin/weighting/resultats/df_'+rcp+'_1m1v_uniforme.csv',delimiter=';',header=2)
wj=df_u['1m1v_uniforme']
#trier dans l'ordre requis et remettre index
dff1=df1.iloc[position].sort_values(['gcm','rcm','membre']).reset_index()
moyj=[]
for j in range(len(dff1)):
    moyj.append(dff1['data'][j][s]*wj[j])
moy_pond_uniforme_1=(np.sum(moyj))/np.sum(wj)  
  
dff2=df2.iloc[position].sort_values(['gcm','rcm','membre']).reset_index()
moyj=[]
for j in range(len(dff1)):
    moyj.append(dff2['data'][j][s]*wj[j])
moy_pond_uniforme_2=(np.sum(moyj))/np.sum(wj)

dff3=df3.iloc[position].sort_values(['gcm','rcm','membre']).reset_index()
moyj=[]
for j in range(len(dff1)):
    moyj.append(dff3['data'][j][s]*wj[j])
moy_pond_uniforme_3=(np.sum(moyj))/np.sum(wj)

#s pour saison
#moyenne non pondérée
mm_1=[]
for k in range(len(dff1)):
    mm_1.append(dff1['data'][k][s])
moyenne_1=np.mean(mm_1)

mm_2=[]
for k in range(len(dff2)):
    mm_2.append(dff2['data'][k][s])
moyenne_2=np.mean(mm_2)

mm_3=[]
for k in range(len(dff3)):
    mm_3.append(dff3['data'][k][s])
moyenne_3=np.mean(mm_3)

#plot 
mean1=[moyenne_1,moyenne_2,moyenne_3]
mean2=[moy_pond_10000_1,moy_pond_10000_2,moy_pond_10000_3]
mean3=[moy_pond_uniforme_1,moy_pond_uniforme_2,moy_pond_uniforme_3]
legend=['moyenne non pondérée','moy pondérée_bassin<10000km²','moy pondérée_un modèle un vote uniforme']
x=['1981-2010','2041-2070','2071-2100']
plt.plot(x,mean1,'.',color='c')
plt.plot(x,mean2,'.',color='b')
plt.plot(x,mean3,'.',color='g')
plt.legend(legend)
plt.ylabel('Température ($\circ$C)')
if b_pt=='brute':
    plt.title(var+'_'+saison[s]+'_'+rcp+'\nBrutes')
    #plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_moy_pondérée_'+rcp+'_'+saison[s],bbox_inches='tight')
else:
    plt.title(var+'_'+saison[s]+'_'+rcp+'\nPost-traitées')
   #plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_moy_pondérée_'+rcp+'_'+saison[s],bbox_inches='tight')
