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


var='tasmin'
stat1='sai_1981_2010_'#référence
b_pt='posttraite'
rcp='rcp85'
#saison n=position dans saison 0=DJF 1-JJA
s=0
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
                   'data':da_all[i]})

#faire dataframe avec dictionnaire
df=pd.DataFrame.from_dict(dictio) 
DEH=[]
for n in range(0,len(df)):
    real = (code_rcp[df.rcp[n]]+code_membre[df.membre[n]])[-3:]
    DEH.append(code_groupe[df.groupe[n]]+'_'+code_gcm[df.gcm[n]]+'_'+code_rcm[df.rcm[n]]+code_resolution[df.resolution[n]]+'_'+real)
df['DEH']=DEH

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