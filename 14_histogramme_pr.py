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
stat1='sai_1981_2010_'#référence
stat2='sai_2041_2070_'
stat3='sai_2071_2100_'
b_pt='posttraite'
rcp='rcp85'
#saison n=position dans saison demandée
n=3
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
df=pd.DataFrame.from_dict(dictio) 

#trouver position selon condition rcp
position=[]
for i in range(0,len(df)):
    if df.rcp[i]==rcp:
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

#trouver position selon condition rcp
position3=[]
for i in range(0,len(df3)):
    if df3.rcp[i]==rcp:
        position3.append(i)

#########################################
#nombre de bins = racine carré du nombre de données
n_bins=int(np.sqrt(len(position)))



#sélectionner dans da_all les simulations selon condition rcp (position)et la saison
data=[]
for i in position:
    data.append(da_all[i][n])

#plot data saison periode historique
plt.figure(1)
plt.style.use('ggplot')
plt.hist(data,bins=n_bins,color='blue')
plt.xlabel('Précipitation (mm/jour)')
plt.ylabel('Nombre')
#plt.ylim(0,45)
plt.xlim(2.4,4.2)
if b_pt=='brute':
    plt.title('Précipitation '+saison[n]+'\n'+stat1[4::]+rcp+'\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_E_1_hist_'+rcp+stat1[3::]+'_'+saison[n],bbox_inches='tight')   
else:
    plt.title('Précipitation '+saison[n]+'\n'+stat1[4::]+rcp+'\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_E_1_hist_'+rcp+stat1[3::]+'_'+saison[n],bbox_inches='tight') 

#sélectionner dans da_all2 les simulations selon condition rcp (position2)et la saison
data2=[]
for i in position2:
    data2.append(da_all2[i][n])

#plot data période futur 2041-2070
plt.figure(2)
plt.style.use('ggplot')
plt.hist(data2,bins=n_bins,color='blue')
plt.xlabel('Précipitation (mm/jour)')
plt.ylabel('Nombre')
#plt.ylim(0,45)
plt.xlim(2.4,4.2)
if b_pt=='brute':
    plt.title('Précipitation '+saison[n]+'\n'+stat2[4::]+rcp+'\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_E_1_hist_'+rcp+stat2[3::]+'_'+saison[n],bbox_inches='tight')   
else:
    plt.title('Précipitation '+saison[n]+'\n'+stat2[4::]+rcp+'\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_E_1_hist_'+rcp+stat2[3::]+'_'+saison[n],bbox_inches='tight') 

#sélectionner dans da_all3 les simulations selon condition rcp (position3) et la saison
data3=[]
for i in position3:
    data3.append(da_all3[i][n])

#plot data période futur 2071-2100
plt.figure(3)
plt.style.use('ggplot')
plt.hist(data3,bins=n_bins,color='blue')
plt.xlabel('Précipitation (mm/jour)')
plt.ylabel('Nombre')
#plt.ylim(0,45)
plt.xlim(2.4,4.2)
if b_pt=='brute':
    plt.title('Précipitation '+saison[n]+'\n'+stat3[4::]+rcp+'\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_E_1_hist_'+rcp+stat3[3::]+'_'+saison[n],bbox_inches='tight')   
else:
    plt.title('Précipitation '+saison[n]+'\n'+stat3[4::]+rcp+'\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_E_1_hist_'+rcp+stat3[3::]+'_'+saison[n],bbox_inches='tight') 

##################       

#calcul du delta entre futur et historique 2041-2070
delta1=[]
for i in position:
    delta1.append(da_all2[i]-da_all[i])

#sélectionner la saison   
delta_1=[]
for j in range(0,len(delta1)):
    delta_1.append(delta1[j][n])

#plot delta
plt.figure(4)
plt.style.use('ggplot')
plt.hist(delta_1,bins=n_bins,color='green')
plt.xlabel('Delta (mm/jour)')
plt.ylabel('Nombre')
plt.xlim(-0.6,1)
#plt.ylim(0,30)
if b_pt=='brute':
    plt.title('Précipitation '+saison[n]+' \n'+rcp+'\n2041_2070-1981_2010\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_E_1_hist_delta_'+rcp+stat2[3::]+'_'+saison[n],bbox_inches='tight')
else:
    plt.title('Précipitation '+saison[n]+'\n'+rcp+'\n2041_2070-1981_2010\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_E_1_hist_delta_'+rcp+stat2[3::]+'_'+saison[n],bbox_inches='tight')

#calcul du delta entre futur et historique 2071-2100
delta2=[]
for i in position:
    delta2.append(da_all3[i]-da_all[i])

#sélectionner la saison     
delta_2=[]
for j in range(0,len(delta2)):
    delta_2.append(delta2[j][n])#1=été

#plot delta
plt.figure(5)
plt.style.use('ggplot')
plt.hist(delta_2,bins=n_bins,color='red')
plt.xlabel('Delta (mm/jour)')
plt.ylabel('Nombre')
plt.xlim(-0.6,1)
#plt.ylim(0,30)
if b_pt=='brute':
    plt.title('Précipitation '+saison[n]+' \n'+rcp+'\n2071_2100-1981_2010\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_E_1_hist_delta_'+rcp+stat3[3::]+'_'+saison[n],bbox_inches='tight')
else:
    plt.title('Précipitation '+saison[n]+'\n'+rcp+'\n2071_2100-1981_2010\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_E_1_hist_delta_'+rcp+stat3[3::]+'_'+saison[n],bbox_inches='tight')
