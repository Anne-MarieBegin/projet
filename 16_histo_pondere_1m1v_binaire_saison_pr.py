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
rcp='rcp45'
#saison n=position dans saison demandée
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
df=pd.DataFrame.from_dict(dictio) 

#sélectionner rcp dans dataframe
RCP=df['rcp']==rcp
dff=df[RCP]
#trié pour obetnir même ordre que fichier csv
df_trier=dff.sort_values(['gcm','rcm','membre'],axis=0)
#ajouter index de 0 à ...
dff=df_trier.reset_index(drop=True)
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

#sélectionner rcp dans dataframe
RCP=df2['rcp']==rcp
dff2=df2[RCP]
#trié pour obetnir même ordre que fichier csv
df2_trier=dff2.sort_values(['gcm','rcm','membre'],axis=0) 
#ajouter index de 0 à ... 
dff2=df2_trier.reset_index(drop=True)     
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

#sélectionner rcp dans dataframe
RCP=df3['rcp']==rcp
dff3=df3[RCP]
#trié pour obetnir même ordre que fichier csv
df3_trier=dff3.sort_values(['gcm','rcm','membre'],axis=0)
#ajouter index de 0 à ...
dff3=df3_trier.reset_index(drop=True)


#ouverture fichier csv pour condition
ff=pd.read_csv('/tank/begin/weighting/resultats/df_'+rcp+'_1m1v_binaire.csv',delimiter=';',header=1)
#colonne avec des 1 et 0 dans dataframe ff
df_condition=ff['1m1v_binaire']

#s pour saison
#selon sélection fichier csv avec un 1 pour True
data_1=[]
for i in range(0,len(dff)):
    if df_condition[i]==1:
        data_1.append(dff['data'][i][s])

data_2=[]
for i in range(0,len(dff2)):
    if df_condition[i]==1:
        data_2.append(dff2['data'][i][s])

data_3=[]
for i in range(0,len(dff3)):
    if df_condition[i]==1:
        data_3.append(dff3['data'][i][s])

#########################################
#nombre de bins = racine carré du nombre de données
n_bins=int(np.sqrt(len(data_1)))



###plot data saison periode historique
#plt.figure(1)
#plt.style.use('ggplot')
#plt.hist(data_1,bins=n_bins,color='blue')
#plt.xlabel('Précipitation (mm/jour)')
#plt.ylabel('Nombre (total '+str(len(data_1))+')')
#plt.xlim(2.5,4.2)
#if b_pt=='brute':
#    plt.title('Précipitation '+saison[s]+'_'+stat1[4:-1]+'\n'+rcp+'_un modèle un vote_binaire\nBrutes')
#    #plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_1m1v_binaire_hist_'+rcp+stat1[3::]+'_'+saison[s],bbox_inches='tight')   
#else:
#    plt.title('Précipitation '+saison[s]+'_'+stat1[4:-1]+'\n'+rcp+'_un modèle un vote_binaire\nPost-traitées')
#    #plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_1m1v_binaire_hist_'+rcp+stat1[3::]+'_'+saison[s],bbox_inches='tight') 
#
#
##
###plot data période futur 2041-2070
#plt.figure(2)
#plt.style.use('ggplot')
#plt.hist(data_2,bins=n_bins,color='blue')
#plt.xlabel('Précipitation (mm/jour)')
#plt.ylabel('Nombre (total '+str(len(data_2))+')')
#plt.xlim(2.5,4.2)
#if b_pt=='brute':
#    plt.title('Précipitation '+saison[s]+'_'+stat2[4:-1]+'\n'+rcp+'_un modèle un vote_binaire\nBrutes')
#   # plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_1m1v_binaire_hist_'+rcp+stat2[3::]+'_'+saison[s],bbox_inches='tight')   
#else:
#    plt.title('Précipitation '+saison[s]+'_'+stat2[4:-1]+'\n'+rcp+'_un modèle un vote_binaire\nPost-traitées')
#   # plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_1m1v_binaire_hist_'+rcp+stat2[3::]+'_'+saison[s],bbox_inches='tight') 
#
#
##
###plot data période futur 2071-2100
#plt.figure(3)
#plt.style.use('ggplot')
#plt.hist(data_3,bins=n_bins,color='blue')
#plt.xlabel('Précipitation (mm/jour)')
#plt.ylabel('Nombre (total '+str(len(data_3))+')')
#plt.xlim(2.5,4.2)
#if b_pt=='brute':
#    plt.title('Précipitation '+saison[s]+'_'+stat3[4:-1]+'\n'+rcp+'_un modèle un vote_binaire\nBrutes')
#    #plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_1m1v_binaire_hist_'+rcp+stat3[3::]+'_'+saison[s],bbox_inches='tight')   
#else:
#    plt.title('Précipitation '+saison[s]+'_'+stat3[4:-1]+'\n'+rcp+'_un modèle un vote_binaire\nPost-traitées')
#   # plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_1m1v_binaire_hist_'+rcp+stat3[3::]+'_'+saison[s],bbox_inches='tight') 

###################       
#
##calcul du delta entre futur et historique 2041-2070
delta1=[]
for i in range(0,len(data_1)):
    delta1.append(data_2[i]-data_1[i])
#

#
##plot delta
plt.figure(4)
plt.style.use('ggplot')
plt.hist(delta1,bins=n_bins,color='green')
plt.xlabel('Delta (mm/jour)')
plt.ylabel('Nombre (total '+str(len(delta1))+')')
plt.xlim(-0.6,0.7)
if b_pt=='brute':
    plt.title('Précipitation '+saison[s]+'_'+rcp+'\n2041_2070-1981_2010\nun modèle un vote_binaire\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_1m1v_binaire_hist_delta_'+rcp+stat2[3::]+'_'+saison[s],bbox_inches='tight')
else:
    plt.title('Précipitation '+saison[s]+'_'+rcp+'\n2041_2070-1981_2010\nun modèle un vote_binaire\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_1m1v_binaire_hist_delta_'+rcp+stat2[3::]+'_'+saison[s],bbox_inches='tight')

##calcul du delta entre futur et historique 2071-2100
delta2=[]
for i in range(0,len(data_1)):
    delta2.append(data_3[i]-data_1[i])


#
##plot delta
plt.figure(5)
plt.style.use('ggplot')
plt.hist(delta2,bins=n_bins,color='red')
plt.xlabel('Delta (mm/jour)')
plt.ylabel('Nombre (total '+str(len(delta1))+')')
plt.xlim(-0.6,0.7)
if b_pt=='brute':
    plt.title('Précipitation '+saison[s]+'_'+rcp+'\n2071_2100-1981_2010\nun modèle un vote_binaire\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_1m1v_binaire_hist_delta_'+rcp+stat3[3::]+'_'+saison[s],bbox_inches='tight')
else:
    plt.title('Précipitation '+saison[s]+'_'+rcp+'\n2071_2100-1981_2010\nun modèle un vote_binaire\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_1m1v_binaire_hist_delta_'+rcp+stat3[3::]+'_'+saison[s],bbox_inches='tight')
