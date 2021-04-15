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
#saison n=position dans saison 0=DJF 1-JJA
s=3
saison=['DJF','JJA','MAM','SON']

path_obs=('/tank/begin/weighting/E_1/obs/'+var)
files_obs= []
for i in os.listdir(path_obs):
    if os.path.isfile(os.path.join(path_obs,i)) and stat1 in i:
        files_obs.append(i)
        

#ouvrir dataarray des fichiers qui commence par stat1
da_obs=[]
for j in range(0,(len(files_obs))):
    da_obs.append(xr.open_dataarray(path_obs+'/'+files_obs[j]))


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
                   'data':da_all[i]})

#faire dataframe avec dictionnaire
df=pd.DataFrame.from_dict(dictio) 

#créer une combinaison de deux variables
df['gcm_rcm'] = df['gcm'] + '_' + df['rcm']

#position selon condition
position=[]
for i in range(0,len(df)):
    if df['rcp'][i] == rcp:
        position.append(i)

#sélectionner dans df['modele'] qui corrrespond a position
modele=[]
for j in position:
    modele.append(df['gcm_rcm'][j])

#sélectionner dans modele les descriptions uniques
m_unique=np.unique(modele)

#classe numero modèle en fonction de la sélection df['gcm_rcm']
liste=[[]for k in range (len(m_unique))]
for j in range (0,len(m_unique)):
    for i in range(0,len(modele)):
        if m_unique[j]==modele[i]:
           liste[j].append(df['data'][i][s])
         
#calcul la pondération de chaque liste
pond=[]
for i in range(0,len(liste)):
    pond.append(1/len(liste[i]))

#appliquer ponderation a chaque position
sp=[[]for k in range (len(m_unique))]
for i in range(len(liste)):
    for j in range(len(liste[i])):
        sp[i].append(pond[i])

#multiplier valeur par son poids
liste2=[[]for k in range (len(m_unique))]
for i in range(len(liste)):
    for j in range(len(liste[i])):
        liste2[i].append(liste[i][j]*sp[i][j])

#faire la somme par modele unique(schema pondéré)
somme=[]
for i in range(len(liste2)):
    somme.append(np.sum(liste2[i]))
    
    #ouvrir tous les fichiers qui commence par stat1 
path_all=('/tank/begin/weighting/E_1/'+b_pt+'/'+var)
files_all= []
for i in os.listdir(path_all):
    if os.path.isfile(os.path.join(path_all,i)) and stat2 in i:
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
                   'data':da_all[i]})

#faire dataframe avec dictionnaire
df=pd.DataFrame.from_dict(dictio) 

#créer une combinaison de deux variables
df['gcm_rcm'] = df['gcm'] + '_' + df['rcm']

#position selon condition
position=[]
for i in range(0,len(df)):
    if df['rcp'][i] == rcp:
        position.append(i)

#sélectionner dans df['modele'] qui corrrespond a position
modele=[]
for j in position:
    modele.append(df['gcm_rcm'][j])

#sélectionner dans modele les descriptions uniques
m_unique=np.unique(modele)

#classe numero modèle en fonction de la sélection df['gcm_rcm']
liste=[[]for k in range (len(m_unique))]
for j in range (0,len(m_unique)):
    for i in range(0,len(modele)):
        if m_unique[j]==modele[i]:
           liste[j].append(df['data'][i][s])
         
#calcul la pondération de chaque liste
pond=[]
for i in range(0,len(liste)):
    pond.append(1/len(liste[i]))

#appliquer ponderation a chaque position
sp=[[]for k in range (len(m_unique))]
for i in range(len(liste)):
    for j in range(len(liste[i])):
        sp[i].append(pond[i])

#multiplier valeur par son poids
liste2=[[]for k in range (len(m_unique))]
for i in range(len(liste)):
    for j in range(len(liste[i])):
        liste2[i].append(liste[i][j]*sp[i][j])

#faire la somme par modele unique(schema pondéré)
somme2=[]
for i in range(len(liste2)):
    somme2.append(np.sum(liste2[i]))

#ouvrir tous les fichiers qui commence par stat1 
path_all=('/tank/begin/weighting/E_1/'+b_pt+'/'+var)
files_all= []
for i in os.listdir(path_all):
    if os.path.isfile(os.path.join(path_all,i)) and stat3 in i:
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
                   'data':da_all[i]})

#faire dataframe avec dictionnaire
df=pd.DataFrame.from_dict(dictio) 

#créer une combinaison de deux variables
df['gcm_rcm'] = df['gcm'] + '_' + df['rcm']

#position selon condition
position=[]
for i in range(0,len(df)):
    if df['rcp'][i] == rcp:
        position.append(i)

#sélectionner dans df['modele'] qui corrrespond a position
modele=[]
for j in position:
    modele.append(df['gcm_rcm'][j])

#sélectionner dans modele les descriptions uniques
m_unique=np.unique(modele)

#classe numero modèle en fonction de la sélection df['gcm_rcm']
liste=[[]for k in range (len(m_unique))]
for j in range (0,len(m_unique)):
    for i in range(0,len(modele)):
        if m_unique[j]==modele[i]:
           liste[j].append(df['data'][i][s])
         
#calcul la pondération de chaque liste
pond=[]
for i in range(0,len(liste)):
    pond.append(1/len(liste[i]))

#appliquer ponderation a chaque position
sp=[[]for k in range (len(m_unique))]
for i in range(len(liste)):
    for j in range(len(liste[i])):
        sp[i].append(pond[i])

#multiplier valeur par son poids
liste2=[[]for k in range (len(m_unique))]
for i in range(len(liste)):
    for j in range(len(liste[i])):
        liste2[i].append(liste[i][j]*sp[i][j])

#faire la somme par modele unique(schema pondéré)
somme3=[]
for i in range(len(liste2)):
    somme3.append(np.sum(liste2[i]))
    
    ##calcul du delta entre futur et historique 2041-2070
delta1=[]
for i in range(0,len(somme)):
    delta1.append(somme2[i]-somme[i])
#
n_bins=int(np.sqrt(len(somme)))
#
##plot delta
plt.figure(4)
plt.style.use('ggplot')
plt.hist(delta1,bins=n_bins,color='green')
plt.xlabel('Delta (mm/jour)')
plt.ylabel('Nombre (total '+str(len(delta1))+')')
plt.xlim(-0.6,0.7)
if b_pt=='brute':
    plt.title('Précipitation '+saison[s]+'_'+rcp+'\n2041_2070-1981_2010\nun modèle un vote_uniforme\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_1m1v_uniforme_hist_delta_'+rcp+stat2[3::]+'_'+saison[s],bbox_inches='tight')
else:
    plt.title('Précipitation '+saison[s]+'_'+rcp+'\n2041_2070-1981_2010\nun modèle un vote_uniforme\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_1m1v_uniforme_hist_delta_'+rcp+stat2[3::]+'_'+saison[s],bbox_inches='tight')

##calcul du delta entre futur et historique 2071-2100
delta2=[]
for i in range(0,len(somme)):
    delta2.append(somme3[i]-somme[i])


#
##plot delta
plt.figure(5)
plt.style.use('ggplot')
plt.hist(delta2,bins=n_bins,color='red')
plt.xlabel('Delta (mm/jour)')
plt.ylabel('Nombre (total '+str(len(delta1))+')')
plt.xlim(-0.6,0.7)
if b_pt=='brute':
    plt.title('Précipitation '+saison[s]+'_'+rcp+'\n2071_2100-1981_2010\nun modèle un vote_uniforme\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/'+var+'_b_1m1v_uniforme_hist_delta_'+rcp+stat3[3::]+'_'+saison[s],bbox_inches='tight')
else:
    plt.title('Précipitation '+saison[s]+'_'+rcp+'\n2071_2100-1981_2010\nun modèle un vote_uniforme\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/'+var+'_pt_1m1v_uniforme_hist_delta_'+rcp+stat3[3::]+'_'+saison[s],bbox_inches='tight')
