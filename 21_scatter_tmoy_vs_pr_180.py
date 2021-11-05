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
from matplotlib.lines import Line2D
import seaborn as sns
var='tmoy'
var2='pr'
stat1='sai_1981_2010_'#référence
stat2='sai_2041_2070_'
stat3='sai_2071_2100_'
b_pt='posttraite'
rcp='rcp85'
#saison s=position dans saison 0=DJF 1=JJA
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
##################################################précipitation
#ouvrir tous les fichiers qui commence par stat1 
path_allp=('/tank/begin/weighting/E_1/'+b_pt+'/'+var2)
files_allp= []
for i in os.listdir(path_allp):
    if os.path.isfile(os.path.join(path_allp,i)) and stat1 in i:
        files_allp.append(i)
        files_allp.sort()

#ouvrir dataarray des fichiers qui commence par stat1
da_allp=[]
for j in range(0,(len(files_allp))):
    da_allp.append(xr.open_dataarray(path_allp+'/'+files_allp[j])*86400)

#créer un dictionnaire avec dataarray       
files_totale=files_allp
files_split=[]
dictiop=[]
for i in range(0,len(files_totale)):
    files_split.append(files_totale[i].split('_'))
    dictiop.append({'groupe':files_split[i][3],
                   'gcm':files_split[i][4],
                   'rcm':files_split[i][5],
                   'membre':files_split[i][6],
                   'resolution':files_split[i][7],
                   'rcp':files_split[i][8],
                   'variable':files_split[i][9],
                   'files':files_totale[i],
                   'data':da_allp[i]})

#faire dataframe avec dictionnaire
df1p=pd.DataFrame.from_dict(dictiop) 

#trouver position selon condition rcp
positionp=[]
for i in range(0,len(df1p)):
    if df1p.rcp[i]==rcp:
        positionp.append(i)
        
########################################################################

#ouvrir tous les fichiers qui commence par stat2 
path_all2p=('/tank/begin/weighting/E_1/'+b_pt+'/'+var2)
files_all2p= []
for i in os.listdir(path_all2p):
    if os.path.isfile(os.path.join(path_all2p,i)) and stat2 in i:
        files_all2p.append(i)
        files_all2p.sort()

#ouvrir dataarray des fichiers qui commence par stat2
da_all2p=[]
for j in range(0,(len(files_all2p))):
    da_all2p.append(xr.open_dataarray(path_all2p+'/'+files_all2p[j])*86400)

#créer un dictionnaire avec dataarray 
files_totale=files_all2p
files_split=[]
dictio2p=[]
for i in range(0,len(files_totale)):
    files_split.append(files_totale[i].split('_'))
    dictio2p.append({'groupe':files_split[i][3],
                   'gcm':files_split[i][4],
                   'rcm':files_split[i][5],
                   'membre':files_split[i][6],
                   'resolution':files_split[i][7],
                   'rcp':files_split[i][8],
                   'variable':files_split[i][9],
                   'files':files_totale[i],
                   'data':da_all2p[i]})

#faire dataframe avec dictionnaire2
df2p=pd.DataFrame.from_dict(dictio2p) 

#trouver position selon condition rcp
position2p=[]
for i in range(0,len(df2p)):
    if df2p.rcp[i]==rcp:
        position2p.append(i)
        
########################################################

#ouvrir tous les fichiers qui commence par stat3 
path_all3p=('/tank/begin/weighting/E_1/'+b_pt+'/'+var2)
files_all3p= []
for i in os.listdir(path_all3p):
    if os.path.isfile(os.path.join(path_all3p,i)) and stat3 in i:
        files_all3p.append(i)
        files_all3p.sort()


#ouvrir dataarray des fichiers qui commence par stat3
da_all3p=[]
for j in range(0,(len(files_all3p))):
    da_all3p.append(xr.open_dataarray(path_all3p+'/'+files_all3p[j])*86400)

#créer un dictionnaire avec dataarray 
files_totale=files_all3p
files_split=[]
dictio3p=[]
for i in range(0,len(files_totale)):
    files_split.append(files_totale[i].split('_'))
    dictio3p.append({'groupe':files_split[i][3],
                   'gcm':files_split[i][4],
                   'rcm':files_split[i][5],
                   'membre':files_split[i][6],
                   'resolution':files_split[i][7],
                   'rcp':files_split[i][8],
                   'variable':files_split[i][9],
                   'files':files_totale[i],
                   'data':da_all3p[i]})

#faire dataframe avec dictionnaire3
df3p=pd.DataFrame.from_dict(dictio3p) 

#trouver position selon condition rcp
position3p=[]
for i in range(0,len(df3p)):
    if df3p.rcp[i]==rcp:
        position3p.append(i)


plt.figure(1)
for i in position:
    delta_tmoy=(df2['data'][i][s]-df1['data'][i][s])
    delta_pr=((df2p['data'][i][s]-df1p['data'][i][s])/df1p['data'][i][s]*100)
    
    if df1['groupe'][i]=='ClimEx':
        plt.scatter(delta_tmoy,delta_pr,c='grey',marker='o',s=15) 
 
    elif df1['groupe'][i]=='CMIP5':
        plt.scatter(delta_tmoy,delta_pr,c='b',marker='o',s=15)
 
    elif df1['groupe'][i]=='CORDEX'or'Ouranos':
        plt.scatter(delta_tmoy,delta_pr,c='r',marker='o',s=15)

plt.plot(max_climex_tmoy,0,color='g',marker='x')
plt.plot(min_climex_tmoy,0,color='g',marker='x')
lines = [Line2D([0], [0], color='b', marker='.',lw=0)
        ,Line2D([0], [0], color='r', marker='.',lw=0)
        ,Line2D([0], [0], color='grey', marker='.',lw=0) ]
labels = ['CMIP5', 'CORDEX','ClimEx']
plt.legend(lines,labels)
plt.xlabel('Température ($\circ$C)')
plt.ylabel('Précipitation (%)')
if b_pt=='brute':
    plt.title('Delta entre 1981-2010 et 2041-2070\n'+saison[s]+'_'+rcp+' (E_1)\nBrutes')
   # plt.savefig('/tank/begin/weighting/plots/brute/pr_tmoy_b_E_1_delta_ensemble_2041_2070_'+rcp+'_'+saison[s],bbox_inches='tight')
else:
    plt.title('Delta entre 1981-2010 et 2041-2070\n'+saison[s]+'_'+rcp+' (E_1)\nPost-traitées')
  #  plt.savefig('/tank/begin/weighting/plots/posttraite/pr_tmoy_pt_E_1_delta_ensemble_2041_2070_'+rcp+'_'+saison[s],bbox_inches='tight')
plt.figure(2)
for i in position:
    delta_tmoy=(df3['data'][i][s]-df1['data'][i][s])
    delta_pr=((df3p['data'][i][s]-df1p['data'][i][s])/df1p['data'][i][s]*100)
    
    if df1['groupe'][i]=='ClimEx':
        plt.scatter(delta_tmoy,delta_pr,c='grey',marker='o',s=15) 
        
    elif df1['groupe'][i]=='CMIP5':
        plt.scatter(delta_tmoy,delta_pr,c='b',marker='o',s=15)

    elif df1['groupe'][i]=='CORDEX'or'Ouranos':
        plt.scatter(delta_tmoy,delta_pr,c='r',marker='o',s=15)
    

lines = [Line2D([0], [0], color='b', marker='.',lw=0)
        ,Line2D([0], [0], color='r', marker='.',lw=0)
        ,Line2D([0], [0], color='grey', marker='.',lw=0) ]
labels = ['CMIP5', 'CORDEX','ClimEx']
plt.legend(lines,labels)
plt.xlabel('Température ($\circ$C)')
plt.ylabel('Précipitation (%)')
if b_pt=='brute':
    plt.title('Delta entre 1981-2010 et 2071-2100\n'+saison[s]+'_'+rcp+' (E_1)\nBrutes')
  #  plt.savefig('/tank/begin/weighting/plots/brute/pr_tmoy_b_E_1_delta_ensemble_2071_2100_'+rcp+'_'+saison[s],bbox_inches='tight')
else:
    plt.title('Delta entre 1981-2010 et 2071-2100\n'+saison[s]+'_'+rcp+' (E_1)\nPost-traitées')
  #  plt.savefig('/tank/begin/weighting/plots/posttraite/pr_tmoy_pt_E_1_delta_ensemble_2071_2100_'+rcp+'_'+saison[s],bbox_inches='tight')
