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
var2='pr'
stat1='sai_1981_2010_'#référence
stat2='sai_2041_2070_'
stat3='sai_2071_2100_'
b_pt='posttraite'
rcp='rcp85'
SE='E_1'
#saison s=position dans saison 0=DJF 1=JJA
s=3
saison=['DJF','JJA','MAM','SON']


#ouvrir tous les fichiers qui commence par stat1 
path_all=('/tank/begin/weighting/'+SE+'/traite/'+b_pt+'/'+var)
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
DEH=[]
for n in range(0,len(df1)):
    real = (code_rcp[df1.rcp[n]]+code_membre[df1.membre[n]])[-3:]
    DEH.append(code_groupe[df1.groupe[n]]+'_'+code_gcm[df1.gcm[n]]+'_'+code_rcm[df1.rcm[n]]+code_resolution[df1.resolution[n]]+'_'+real)
df1['DEH']=DEH

#trouver position selon condition rcp
position=[]
for i in range(0,len(df1)):
    if df1.rcp[i]==rcp:
        position.append(i)
        
########################################################################

#ouvrir tous les fichiers qui commence par stat2 
path_all2=('/tank/begin/weighting/'+SE+'/traite/'+b_pt+'/'+var)
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
DEH=[]
for n in range(0,len(df2)):
    real = (code_rcp[df2.rcp[n]]+code_membre[df2.membre[n]])[-3:]
    DEH.append(code_groupe[df2.groupe[n]]+'_'+code_gcm[df2.gcm[n]]+'_'+code_rcm[df2.rcm[n]]+code_resolution[df2.resolution[n]]+'_'+real)
df2['DEH']=DEH
#trouver position selon condition rcp
position2=[]
for i in range(0,len(df2)):
    if df2.rcp[i]==rcp:
        position2.append(i)
        
########################################################

#ouvrir tous les fichiers qui commence par stat3 
path_all3=('/tank/begin/weighting/'+SE+'/traite/'+b_pt+'/'+var)
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
DEH=[]
for n in range(0,len(df3)):
    real = (code_rcp[df3.rcp[n]]+code_membre[df3.membre[n]])[-3:]
    DEH.append(code_groupe[df3.groupe[n]]+'_'+code_gcm[df3.gcm[n]]+'_'+code_rcm[df3.rcm[n]]+code_resolution[df3.resolution[n]]+'_'+real)
df3['DEH']=DEH
#trouver position selon condition rcp
position3=[]
for i in range(0,len(df3)):
    if df3.rcp[i]==rcp:
        position3.append(i)
##################################################précipitation
#ouvrir tous les fichiers qui commence par stat1 
path_allp=('/tank/begin/weighting/'+SE+'/traite/'+b_pt+'/'+var2)
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
DEH=[]
for n in range(0,len(df1p)):
    real = (code_rcp[df1p.rcp[n]]+code_membre[df1p.membre[n]])[-3:]
    DEH.append(code_groupe[df1p.groupe[n]]+'_'+code_gcm[df1p.gcm[n]]+'_'+code_rcm[df1p.rcm[n]]+code_resolution[df1p.resolution[n]]+'_'+real)
df1p['DEH']=DEH
#trouver position selon condition rcp
positionp=[]
for i in range(0,len(df1p)):
    if df1p.rcp[i]==rcp:
        positionp.append(i)
        
########################################################################

#ouvrir tous les fichiers qui commence par stat2 
path_all2p=('/tank/begin/weighting/'+SE+'/traite/'+b_pt+'/'+var2)
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
DEH=[]
for n in range(0,len(df2p)):
    real = (code_rcp[df2p.rcp[n]]+code_membre[df2p.membre[n]])[-3:]
    DEH.append(code_groupe[df2p.groupe[n]]+'_'+code_gcm[df2p.gcm[n]]+'_'+code_rcm[df2p.rcm[n]]+code_resolution[df2p.resolution[n]]+'_'+real)
df2p['DEH']=DEH
#trouver position selon condition rcp
position2p=[]
for i in range(0,len(df2p)):
    if df2p.rcp[i]==rcp:
        position2p.append(i)
        
########################################################

#ouvrir tous les fichiers qui commence par stat3 
path_all3p=('/tank/begin/weighting/'+SE+'/traite/'+b_pt+'/'+var2)
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
DEH=[]
for n in range(0,len(df3p)):
    real = (code_rcp[df3p.rcp[n]]+code_membre[df3p.membre[n]])[-3:]
    DEH.append(code_groupe[df3p.groupe[n]]+'_'+code_gcm[df3p.gcm[n]]+'_'+code_rcm[df3p.rcm[n]]+code_resolution[df3p.resolution[n]]+'_'+real)
df3p['DEH']=DEH
#trouver position selon condition rcp
position3p=[]
for i in range(0,len(df3p)):
    if df3p.rcp[i]==rcp:
        position3p.append(i)

######################################################################################
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

#calcul du delta
delta_moy_pond_10000_1=moy_pond_10000_2-moy_pond_10000_1
delta_moy_pond_10000_2=moy_pond_10000_3-moy_pond_10000_1
moyip=[]
for i in range(0,len(df1p)):
    moyip.append(df1p['data'][i][s]*wi[i])
moy_pond_10000_1p=(np.sum(moyip))/np.sum(wi)

moyip=[]
for i in range(0,len(df2p)):
    moyip.append(df2p['data'][i][s]*wi[i])
moy_pond_10000_2p=(np.sum(moyip))/np.sum(wi)


moyip=[]
for i in range(0,len(df3p)):
    moyip.append(df3p['data'][i][s]*wi[i])
moy_pond_10000_3p=(np.sum(moyip))/np.sum(wi)

#calcul du delta
delta_moy_pond_10000_1p=(moy_pond_10000_2p-moy_pond_10000_1p)/moy_pond_10000_1p*100
delta_moy_pond_10000_2p=(moy_pond_10000_3p-moy_pond_10000_1p)/moy_pond_10000_1p*100

################################################################################

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

#calcul du delta
delta_moy_pond_uniforme_1=moy_pond_uniforme_2-moy_pond_uniforme_1
delta_moy_pond_uniforme_2=moy_pond_uniforme_3-moy_pond_uniforme_1

dff1p=df1p.iloc[position].sort_values(['gcm','rcm','membre']).reset_index()
moyjp=[]
for j in range(len(dff1p)):
    moyjp.append(dff1p['data'][j][s]*wj[j])
moy_pond_uniforme_1p=(np.sum(moyjp))/np.sum(wj)  
  
dff2p=df2p.iloc[position].sort_values(['gcm','rcm','membre']).reset_index()
moyjp=[]
for j in range(len(dff1p)):
    moyjp.append(dff2p['data'][j][s]*wj[j])
moy_pond_uniforme_2p=(np.sum(moyjp))/np.sum(wj)


dff3p=df3p.iloc[position].sort_values(['gcm','rcm','membre']).reset_index()
moyjp=[]
for j in range(len(dff1p)):
    moyjp.append(dff3p['data'][j][s]*wj[j])
moy_pond_uniforme_3p=(np.sum(moyjp))/np.sum(wj)

#calcul du delta
delta_moy_pond_uniforme_1p=(moy_pond_uniforme_2p-moy_pond_uniforme_1p)/moy_pond_uniforme_1p*100
delta_moy_pond_uniforme_2p=(moy_pond_uniforme_3p-moy_pond_uniforme_1p)/moy_pond_uniforme_1p*100
#s pour saison

################################################################################

#fichier Gabriel pour un centre un vote (CM-S)
df_cm=pd.read_csv('/tank/begin/weighting/resultats/'+rcp+'.csv')
df_cm_sort=df_cm.sort_values(['scenario_id']).reset_index()
#enlever une simulation qui n'est pas dans ma liste
if rcp == 'rcp45':
    df_cm_sort_=df_cm_sort.drop(31).reset_index()
else:
    df_cm_sort_=df_cm_sort
df1_sort=df1.iloc[position].sort_values(['DEH']).reset_index()
df2_sort=df2.iloc[position].sort_values(['DEH']).reset_index()
df3_sort=df3.iloc[position].sort_values(['DEH']).reset_index()
df1p_sort=df1p.iloc[position].sort_values(['DEH']).reset_index()
df2p_sort=df2p.iloc[position].sort_values(['DEH']).reset_index()
df3p_sort=df3p.iloc[position].sort_values(['DEH']).reset_index()
wk=df_cm_sort_['CM-S']

moyk=[]
for j in range(len(df1_sort)):
    moyk.append(df1_sort['data'][j][s]*wk[j])
moy_pond_cm_1=(np.sum(moyk)/np.sum(wk))

moyk=[]
for j in range(len(df2_sort)):
    moyk.append(df2_sort['data'][j][s]*wk[j])
moy_pond_cm_2=(np.sum(moyk)/np.sum(wk))

moyk=[]
for j in range(len(df3_sort)):
    moyk.append(df3_sort['data'][j][s]*wk[j])
moy_pond_cm_3=(np.sum(moyk)/np.sum(wk))

delta_moy_pond_cm_1=moy_pond_cm_2-moy_pond_cm_1
delta_moy_pond_cm_2=moy_pond_cm_3-moy_pond_cm_1


moyk=[]
for j in range(len(df1p_sort)):
    moyk.append(df1p_sort['data'][j][s]*wk[j])
moy_pond_cm_1p=(np.sum(moyk)/np.sum(wk))

moyk=[]
for j in range(len(df2p_sort)):
    moyk.append(df2p_sort['data'][j][s]*wk[j])
moy_pond_cm_2p=(np.sum(moyk)/np.sum(wk))

moyk=[]
for j in range(len(df3p_sort)):
    moyk.append(df3p_sort['data'][j][s]*wk[j])
moy_pond_cm_3p=(np.sum(moyk)/np.sum(wk))

delta_moy_pond_cm_1p=(moy_pond_cm_2p-moy_pond_cm_1p)/moy_pond_cm_1p*100
delta_moy_pond_cm_2p=(moy_pond_cm_3p-moy_pond_cm_1p)/moy_pond_cm_1p*100


######################################################################
if b_pt == 'brute':
    df_diff=pd.read_csv('/tank/begin/weighting/pond_combine/pond_mixte_mc_obs_b_tmoy_'+saison[s]+'_'+rcp+'.csv')
else:
    df_diff=pd.read_csv('/tank/begin/weighting/pond_combine/pond_mixte_mc_obs_pt_tmoy_'+saison[s]+'_'+rcp+'.csv')

w_diff=df_diff['0']

dff1_=df1.iloc[position].reset_index()
moyd=[]
for j in range(len(dff1_)):
    moyd.append(dff1_['data'][j][s]*w_diff[j])
moy_pond_diff_1=(np.sum(moyd)/np.sum(w_diff))

dff2_=df2.iloc[position].reset_index()
moyd=[]
for j in range(len(dff2_)):
    moyd.append(dff2_['data'][j][s]*w_diff[j])
moy_pond_diff_2=(np.sum(moyd)/np.sum(w_diff))

dff3_=df3.iloc[position].reset_index()
moyd=[]
for j in range(len(dff3_)):
    moyd.append(dff3_['data'][j][s]*w_diff[j])
moy_pond_diff_3=(np.sum(moyd)/np.sum(w_diff))

delta_moy_pond_diff_1=moy_pond_diff_2-moy_pond_diff_1
delta_moy_pond_diff_2=moy_pond_diff_3-moy_pond_diff_1

dff1p_=df1p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff1p_)):
    moyd.append(dff1p_['data'][j][s]*w_diff[j])
moy_pond_diff_1p=(np.sum(moyd)/np.sum(w_diff))

dff2p_=df2p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff2p_)):
    moyd.append(dff2p_['data'][j][s]*w_diff[j])
moy_pond_diff_2p=(np.sum(moyd)/np.sum(w_diff))

dff3p_=df3p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff3p_)):
    moyd.append(dff3p_['data'][j][s]*w_diff[j])
moy_pond_diff_3p=(np.sum(moyd)/np.sum(w_diff))

delta_moy_pond_diff_1p=(moy_pond_diff_2p-moy_pond_diff_1p)/moy_pond_diff_1p*100
delta_moy_pond_diff_2p=(moy_pond_diff_3p-moy_pond_diff_1p)/moy_pond_diff_1p*100
######################################################################
if b_pt == 'brute':
    df_diff=pd.read_csv('/tank/begin/weighting/pond_combine/pond_mixte_mc+pente_obs_b_tmoy_'+saison[s]+'_'+rcp+'.csv')
else:
    df_diff=pd.read_csv('/tank/begin/weighting/pond_combine/pond_mixte_mc+pente_obs_pt_tmoy_'+saison[s]+'_'+rcp+'.csv')

w_diff=df_diff['0']

dff1_=df1.iloc[position].reset_index()
moyd=[]
for j in range(len(dff1_)):
    moyd.append(dff1_['data'][j][s]*w_diff[j])
moy_pond_diff_1=(np.sum(moyd)/np.sum(w_diff))

dff2_=df2.iloc[position].reset_index()
moyd=[]
for j in range(len(dff2_)):
    moyd.append(dff2_['data'][j][s]*w_diff[j])
moy_pond_diff_2=(np.sum(moyd)/np.sum(w_diff))

dff3_=df3.iloc[position].reset_index()
moyd=[]
for j in range(len(dff3_)):
    moyd.append(dff3_['data'][j][s]*w_diff[j])
moy_pond_diff_3=(np.sum(moyd)/np.sum(w_diff))

delta_moy_pond_diff_pente_1=moy_pond_diff_2-moy_pond_diff_1
delta_moy_pond_diff_pente_2=moy_pond_diff_3-moy_pond_diff_1

dff1p_=df1p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff1p_)):
    moyd.append(dff1p_['data'][j][s]*w_diff[j])
moy_pond_diff_1p=(np.sum(moyd)/np.sum(w_diff))

dff2p_=df2p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff2p_)):
    moyd.append(dff2p_['data'][j][s]*w_diff[j])
moy_pond_diff_2p=(np.sum(moyd)/np.sum(w_diff))

dff3p_=df3p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff3p_)):
    moyd.append(dff3p_['data'][j][s]*w_diff[j])
moy_pond_diff_3p=(np.sum(moyd)/np.sum(w_diff))

delta_moy_pond_diff_pente_1p=(moy_pond_diff_2p-moy_pond_diff_1p)/moy_pond_diff_1p*100
delta_moy_pond_diff_pente_2p=(moy_pond_diff_3p-moy_pond_diff_1p)/moy_pond_diff_1p*100
##########################################################################################
if b_pt == 'brute':
    df_diff=pd.read_csv('/tank/begin/weighting/pond_combine/pond_mixte_mc+pente+1m1v_obs_b_tmoy_'+saison[s]+'_'+rcp+'.csv')
else:
    df_diff=pd.read_csv('/tank/begin/weighting/pond_combine/pond_mixte_mc+pente+1m1v_obs_pt_tmoy_'+saison[s]+'_'+rcp+'.csv')

w_diff=df_diff['0']

dff1_=df1.iloc[position].reset_index()
moyd=[]
for j in range(len(dff1_)):
    moyd.append(dff1_['data'][j][s]*w_diff[j])
moy_pond_diff_1=(np.sum(moyd)/np.sum(w_diff))

dff2_=df2.iloc[position].reset_index()
moyd=[]
for j in range(len(dff2_)):
    moyd.append(dff2_['data'][j][s]*w_diff[j])
moy_pond_diff_2=(np.sum(moyd)/np.sum(w_diff))

dff3_=df3.iloc[position].reset_index()
moyd=[]
for j in range(len(dff3_)):
    moyd.append(dff3_['data'][j][s]*w_diff[j])
moy_pond_diff_3=(np.sum(moyd)/np.sum(w_diff))

delta_moy_pond_diff_mixte_1=moy_pond_diff_2-moy_pond_diff_1
delta_moy_pond_diff_mixte_2=moy_pond_diff_3-moy_pond_diff_1

dff1p_=df1p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff1p_)):
    moyd.append(dff1p_['data'][j][s]*w_diff[j])
moy_pond_diff_1p=(np.sum(moyd)/np.sum(w_diff))

dff2p_=df2p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff2p_)):
    moyd.append(dff2p_['data'][j][s]*w_diff[j])
moy_pond_diff_2p=(np.sum(moyd)/np.sum(w_diff))

dff3p_=df3p.iloc[position].reset_index()
moyd=[]
for j in range(len(dff3p_)):
    moyd.append(dff3p_['data'][j][s]*w_diff[j])
moy_pond_diff_3p=(np.sum(moyd)/np.sum(w_diff))

delta_moy_pond_diff_mixte_1p=(moy_pond_diff_2p-moy_pond_diff_1p)/moy_pond_diff_1p*100
delta_moy_pond_diff_mixte_2p=(moy_pond_diff_3p-moy_pond_diff_1p)/moy_pond_diff_1p*100



######################################################################
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

#calcul du delta
delta_moyenne_1=moyenne_2-moyenne_1
delta_moyenne_2=moyenne_3-moyenne_1

mm_1p=[]
for k in range(len(dff1p)):
    mm_1p.append(dff1p['data'][k][s])
moyenne_1p=np.mean(mm_1p)

mm_2p=[]
for k in range(len(dff2p)):
    mm_2p.append(dff2p['data'][k][s])
moyenne_2p=np.mean(mm_2p)


mm_3p=[]
for k in range(len(dff3p)):
    mm_3p.append(dff3p['data'][k][s])
moyenne_3p=np.mean(mm_3p)

#calcul du delta
delta_moyenne_1p=(moyenne_2p-moyenne_1p)/moyenne_1p*100
delta_moyenne_2p=(moyenne_3p-moyenne_1p)/moyenne_1p*100

###############################################################################

#moyenne cmip5
cmip5=[]
for i in range(len(dff1)):
    if dff1['groupe'][i]=='CMIP5':
        cmip5.append(dff1['data'][i][s])
moy_cmip5_1=np.mean(cmip5)

cmip5=[]
for i in range(len(dff2)):
    if dff2['groupe'][i]=='CMIP5':
        cmip5.append(dff2['data'][i][s])
moy_cmip5_2=np.mean(cmip5)
cmip5=[]


for i in range(len(dff3)):
    if dff3['groupe'][i]=='CMIP5':
        cmip5.append(dff3['data'][i][s])
moy_cmip5_3=np.mean(cmip5)

#calcul du delta
delta_moy_cmip5_1=moy_cmip5_2-moy_cmip5_1
delta_moy_cmip5_2=moy_cmip5_3-moy_cmip5_1

cmip5p=[]
for i in range(len(dff1p)):
    if dff1p['groupe'][i]=='CMIP5':
        cmip5p.append(dff1p['data'][i][s])
moy_cmip5_1p=np.mean(cmip5p)

cmip5p=[]
for i in range(len(dff2p)):
    if dff2p['groupe'][i]=='CMIP5':
        cmip5p.append(dff2p['data'][i][s])
moy_cmip5_2p=np.mean(cmip5p)


cmip5p=[]
for i in range(len(dff3p)):
    if dff3p['groupe'][i]=='CMIP5':
        cmip5p.append(dff3p['data'][i][s])
moy_cmip5_3p=np.mean(cmip5p)

#calcul du delta
delta_moy_cmip5_1p=(moy_cmip5_2p-moy_cmip5_1p)/moy_cmip5_1p*100
delta_moy_cmip5_2p=(moy_cmip5_3p-moy_cmip5_1p)/moy_cmip5_1p*100

################################################################################

#moyenne cordex
cordex=[]
mod=['CORDEX','Ouranos']
for i in range(len(dff1)):
    for j in range(len(mod)):
        if dff1['groupe'][i]==mod[j]:
            cordex.append(dff1['data'][i][s])
moy_cordex_1=np.mean(cordex)

cordex=[]
mod=['CORDEX','Ouranos']
for i in range(len(dff1)):
    for j in range(len(mod)):
        if dff2['groupe'][i]==mod[j]:
            cordex.append(dff2['data'][i][s])
moy_cordex_2=np.mean(cordex)

cordex=[]
mod=['CORDEX','Ouranos']
for i in range(len(dff3)):
    for j in range(len(mod)):
        if dff3['groupe'][i]==mod[j]:
            cordex.append(dff3['data'][i][s])
moy_cordex_3=np.mean(cordex)

#calcul du delta
delta_moy_cordex_1=moy_cordex_2-moy_cordex_1
delta_moy_cordex_2=moy_cordex_3-moy_cordex_1

cordexp=[]
mod=['CORDEX','Ouranos']
for i in range(len(dff1p)):
    for j in range(len(mod)):
        if dff1p['groupe'][i]==mod[j]:
            cordexp.append(dff1p['data'][i][s])
moy_cordex_1p=np.mean(cordexp)

cordexp=[]
mod=['CORDEX','Ouranos']
for i in range(len(dff1p)):
    for j in range(len(mod)):
        if dff2p['groupe'][i]==mod[j]:
            cordexp.append(dff2p['data'][i][s])
moy_cordex_2p=np.mean(cordexp)

cordexp=[]
mod=['CORDEX','Ouranos']
for i in range(len(dff3p)):
    for j in range(len(mod)):
        if dff3p['groupe'][i]==mod[j]:
            cordexp.append(dff3p['data'][i][s])
moy_cordex_3p=np.mean(cordexp)

#calcul du delta
delta_moy_cordex_1p=(moy_cordex_2p-moy_cordex_1p)/moy_cordex_1p*100
delta_moy_cordex_2p=(moy_cordex_3p-moy_cordex_1p)/moy_cordex_1p*100

################################################################################

#moyenne climex
climex=[]
for i in range(len(dff1)):
    if dff1['groupe'][i]=='ClimEx':
        climex.append(dff1['data'][i][s])
moy_climex_1=np.mean(climex)

climex=[]
for i in range(len(dff2)):
    if dff2['groupe'][i]=='ClimEx':
        climex.append(dff2['data'][i][s])
moy_climex_2=np.mean(climex)


climex=[]
for i in range(len(dff3)):
    if dff3['groupe'][i]=='ClimEx':
        climex.append(dff3['data'][i][s])
moy_climex_3=np.mean(climex)

#calcul du delta
delta_moy_climex_1=moy_climex_2-moy_climex_1
delta_moy_climex_2=moy_climex_3-moy_climex_1

climexp=[]
for i in range(len(dff1p)):
    if dff1p['groupe'][i]=='ClimEx':
        climexp.append(dff1p['data'][i][s])
moy_climex_1p=np.mean(climexp)

climexp=[]
for i in range(len(dff2p)):
    if dff2p['groupe'][i]=='ClimEx':
        climexp.append(dff2p['data'][i][s])
moy_climex_2p=np.mean(climexp)


climexp=[]
for i in range(len(dff3p)):
    if dff3p['groupe'][i]=='ClimEx':
        climexp.append(dff3p['data'][i][s])
moy_climex_3p=np.mean(climexp)

#calcul du delta
delta_moy_climex_1p=(moy_climex_2p-moy_climex_1p)/moy_climex_1p*100
delta_moy_climex_2p=(moy_climex_3p-moy_climex_1p)/moy_climex_1p*100

################################################################################

plt.figure(1)
legend=['moyenne non pondérée','moy pondérée_250000km²(5$\Delta$x)',
        'moy pondérée_un modèle un vote uniforme','moy_pondérée_un centre un vote',
        'CMIP5','CORDEX','ClimEx','moy_pondérée_mixte_mc_tmoy_obs_'+saison[s],'moy_pondérée_mixte_mc+pente_tmoy_obs_'+saison[s]
        ,'moy_pondérée_mixte_mc+pente+1m1v_tmoy_obs_'+saison[s]
        ]

plt.scatter(delta_moyenne_1,delta_moyenne_1p,color='m')
plt.scatter(delta_moy_pond_10000_1,delta_moy_pond_10000_1p,color='b')
plt.scatter(delta_moy_pond_uniforme_1,delta_moy_pond_uniforme_1p,color='g')
plt.scatter(delta_moy_pond_cm_1,delta_moy_pond_cm_1p,color='k')
plt.scatter(delta_moy_cmip5_1,delta_moy_cmip5_1p,color='c')
plt.scatter(delta_moy_cordex_1,delta_moy_cordex_1p,color='y')
plt.scatter(delta_moy_climex_1,delta_moy_climex_1p,color='r')
plt.scatter(delta_moy_pond_diff_1,delta_moy_pond_diff_1p,color='hotpink')
plt.scatter(delta_moy_pond_diff_pente_1,delta_moy_pond_diff_pente_1p,color='brown')
plt.scatter(delta_moy_pond_diff_mixte_1,delta_moy_pond_diff_mixte_1p,color='orange')

plt.legend(legend,fontsize=7,framealpha=0.1)

plt.ylabel('Précipitation (%)')
plt.xlabel('Température moyenne ($\circ$C)')
if b_pt=='brute':
    plt.title('Delta entre 1981-2010 et 2041-2070\n'+saison[s]+'_'+rcp+' ('+SE+')\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/pr_tmoy_b_'+SE+'_delta_mixte_mc+pente+1m1v_tmoy_2041_2070_'+saison[s]+'_'+rcp,bbox_inches='tight')
else:
    plt.title('Delta entre 1981-2010 et 2041_2070\n'+saison[s]+'_'+rcp+' ('+SE+')\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/pr_tmoy_pt_'+SE+'_delta_mixte_mc+pente+1m1v_tmoy_2041_2070_'+saison[s]+'_'+rcp,bbox_inches='tight')

plt.figure(2)   
legend=['moyenne non pondérée','moy pondérée_250000km²(5$\Delta$x)',
        'moy pondérée_un modèle un vote uniforme','moy_pondérée_un centre un vote',
        'CMIP5','CORDEX','ClimEx','moy_pondérée_mixte_mc_tmoy_obs_'+saison[s],'moy_pondérée_mixte_mc+pente_tmoy_obs_'+saison[s]
        ,'moy_pondérée_mixte_mc+pente+1m1v_tmoy_obs_'+saison[s]
        ]

plt.scatter(delta_moyenne_2,delta_moyenne_2p,color='m')
plt.scatter(delta_moy_pond_10000_2,delta_moy_pond_10000_2p,color='b')
plt.scatter(delta_moy_pond_uniforme_2,delta_moy_pond_uniforme_2p,color='g')
plt.scatter(delta_moy_pond_cm_2,delta_moy_pond_cm_2p,color='k')
plt.scatter(delta_moy_cmip5_2,delta_moy_cmip5_2p,color='c')
plt.scatter(delta_moy_cordex_2,delta_moy_cordex_2p,color='y')
plt.scatter(delta_moy_climex_2,delta_moy_climex_2p,color='r')
plt.scatter(delta_moy_pond_diff_2,delta_moy_pond_diff_2p,color='hotpink')
plt.scatter(delta_moy_pond_diff_pente_2,delta_moy_pond_diff_pente_2p,color='brown')
plt.scatter(delta_moy_pond_diff_mixte_2,delta_moy_pond_diff_mixte_2p,color='orange')

plt.legend(legend,fontsize=7,framealpha=0.1)
#plt.xlim(5.8,7.2)
#plt.ylim(22,34)
plt.ylabel('Précipitation (%)')
plt.xlabel('Température moyenne ($\circ$C)')
if b_pt=='brute':
    plt.title('Delta entre 1981-2010 et 2071-2100\n'+saison[s]+'_'+rcp+' ('+SE+')\nBrutes')
    plt.savefig('/tank/begin/weighting/plots/brute/pr_tmoy_b_'+SE+'_delta_mixte_mc+pente+1m1v_tmoy_2071_2100_'+saison[s]+'_'+rcp,bbox_inches='tight')
else:
    plt.title('Delta entre 1981-2010 et 2071-2100\n'+saison[s]+'_'+rcp+' ('+SE+')\nPost-traitées')
    plt.savefig('/tank/begin/weighting/plots/posttraite/pr_tmoy_pt_'+SE+'_delta_mixte_mc+pente+1m1v_tmoy_2071_2100_'+saison[s]+'_'+rcp,bbox_inches='tight')
