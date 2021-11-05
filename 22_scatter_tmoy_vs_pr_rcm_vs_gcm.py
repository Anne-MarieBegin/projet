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

var='tmoy'
var2='pr'
stat1='sai_1981_2010_'#référence
stat2='sai_2041_2070_'
stat3='sai_2071_2100_'
b_pt='posttraite'
rcp='rcp85'
SE='E_2'
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


df_all=pd.merge(df1,df2['data'],suffixes=['1','2'],how='outer',left_index=True,right_index=True)
df_all=pd.merge(df_all,df3['data'].rename('data3'),how='outer',left_index=True,right_index=True)
df_all=pd.merge(df_all,df1p['data'].rename('data1p'),how='outer',left_index=True,right_index=True)
df_all=pd.merge(df_all,df2p['data'].rename('data2p'),how='outer',left_index=True,right_index=True)
df_all=pd.merge(df_all,df3p['data'].rename('data3p'),how='outer',left_index=True,right_index=True)

df_all['pilote']=df1['gcm']+'_'+df1['membre']

pilote_liste=['CanESM2_r1i1p1','GFDL-ESM2M_r1i1p1','MPI-ESM-LR_r1i1p1','MPI-ESM-MR_r1i1p1',
             'CNRM-CM5_r1i1p1','CanESM2_r2i1p1','CanESM2_r3i1p1','CanESM2_r4i1p1',
             'CanESM2_r5i1p1']

figT, ax1 = plt.subplots()
figP, ax2 = plt.subplots()

cgcm = 'k'
crcm = 'g'

for pilote in pilote_liste:
    
    p=df_all[(df_all['pilote'] == pilote) & (df_all['rcm'] == 'NotApplicable') & (df_all['rcp'] == rcp)].iloc[0]
     
    pxT=p['data2'][s]-p['data1'][s]
    pyT=p['data3'][s]-p['data1'][s]
    pxP=(p['data2p'][s]-p['data1p'][s])/p['data1p'][s]*100
    pyP=(p['data3p'][s]-p['data1p'][s])/p['data1p'][s]*100

    ax1.scatter(pxT,pxP,color=cgcm)
    ax2.scatter(pyT,pyP,color=cgcm)
    
    for i, rcm in df_all[(df_all['pilote'] == pilote) & (df_all['rcm'] != 'NotApplicable') & (df_all['rcp']==rcp)].iterrows():

       rxT = rcm['data2'][s] - rcm['data1'][s]
       ryT = rcm['data3'][s] - rcm['data1'][s]
       rxP = (rcm['data2p'][s] - rcm['data1p'][s])/rcm['data1p'][s]*100
       ryP = (rcm['data3p'][s] - rcm['data1p'][s])/rcm['data1p'][s]*100
       if df_all['rcm'][i]=='RegCM4':
           color='r'
       if df_all['rcm'][i]=='CRCM5-UQAM':
           color='g'
       if df_all['rcm'][i]=='CanRCM4':
           color='b'
       if df_all['rcm'][i]=='RCA4':
           color='m'
       if df_all['rcm'][i]=='CRCM5-Ouranos':
           color='c'
           
       ax1.scatter(rxT, rxP,color=color)
       ax2.scatter(ryT, ryP,color=color)
       plt.figure(1)
       ax1.plot([pxT, rxT], [pxP, rxP], '-', color='lightgrey')
       plt.xlabel('Température ($\circ$C)')
       plt.ylabel('Précipitation (%)')
       lines = [Line2D([0], [0], color='k', marker='o',lw=0)
                ,Line2D([0], [0], color='r', marker='o',lw=0)
                ,Line2D([0], [0], color='g', marker='o',lw=0)
                ,Line2D([0], [0], color='b', marker='o',lw=0) 
                ,Line2D([0], [0], color='m', marker='o',lw=0)
                ,Line2D([0], [0], color='c', marker='o',lw=0)]
       labels = ['GCM','RegCM4', 'CRCM5-UQAM','CanRCM4','RCA4','CRCM5-Ouranos']
       plt.legend(lines,labels,bbox_to_anchor=(1.2, 1),loc='upper left')
       plt.text(pxT+0.03,pxP+0.03,pilote)
       if b_pt=='brute':
           plt.title('Delta entre 1981-2010 et 2041-2070\n'+saison[s]+'_'+rcp+' ('+SE+')\nBrutes')
          # plt.savefig('/tank/begin/weighting/plots/brute/pr_tmoy_b_'+SE+'_delta_pilote_2041_2070_'+rcp+'_'+saison[s],bbox_inches='tight')
       else:
           plt.title('Delta entre 1981-2010 et 2041-2070\n'+saison[s]+'_'+rcp+' ('+SE+')\nPost-traitées')
          # plt.savefig('/tank/begin/weighting/plots/posttraite/pr_tmoy_pt_'+SE+'_delta_pilote_2041_2070_'+rcp+'_'+saison[s],bbox_inches='tight')
       plt.figure(2)
       ax2.plot([pyT, ryT], [pyP, ryP], '-', color='lightgrey')
       plt.xlabel('Température ($\circ$C)')
       plt.ylabel('Précipitation (%)')
       lines = [Line2D([0], [0], color='k', marker='o',lw=0)
                ,Line2D([0], [0], color='r', marker='o',lw=0)
                ,Line2D([0], [0], color='g', marker='o',lw=0)
                ,Line2D([0], [0], color='b', marker='o',lw=0) 
                ,Line2D([0], [0], color='m', marker='o',lw=0)
                ,Line2D([0], [0], color='c', marker='o',lw=0)]
       labels = ['GCM','RegCM4', 'CRCM5-UQAM','CanRCM4','RCA4','CRCM5-Ouranos']
       plt.legend(lines,labels,bbox_to_anchor=(1.2, 1),loc='upper left')
       plt.text(pyT+0.03,pyP+0.03,pilote)
       if b_pt=='brute':
           plt.title('Delta entre 1981-2010 et 2071-2100\n'+saison[s]+'_'+rcp+' ('+SE+')\nBrutes')
          # plt.savefig('/tank/begin/weighting/plots/brute/pr_tmoy_b_'+SE+'_delta_pilote_2071_2100_'+rcp+'_'+saison[s],bbox_inches='tight')
       else:
           plt.title('Delta entre 1981-2010 et 2071-2100\n'+saison[s]+'_'+rcp+' ('+SE+')\nPost-traitées')
         #  plt.savefig('/tank/begin/weighting/plots/posttraite/pr_tmoy_pt_'+SE+'_delta_pilote_2071_2100_'+rcp+'_'+saison[s],bbox_inches='tight')

#
#data_rcm_1=[]  
#data_rcm_2=[]          
#for i in range(len(df1)):
#    for j in range(len(pilote_liste)):
#        if df1['pilote'][i]==pilote_liste[j] and df1['rcm'][i]!='NotApplicable'and df1['rcp'][i]==rcp:
#            data_rcm_1.append(df2['data'][i][s]-df1['data'][i][s])
#            data_rcm_2.append(df3['data'][i][s]-df1['data'][i][s])
#            print(df1['rcm'][i])
#            print(i,j)
#data_gcm_1=[]
#data_gcm_2=[]           
#for i in range(len(df1)):
#    for j in range(len(pilote_liste)):
#        if df1['pilote'][i]==pilote_liste[j] and df1['rcm'][i]=='NotApplicable'and df1['rcp'][i]==rcp:
#            data_gcm_1.append(df2['data'][i][s]-df1['data'][i][s])
#            data_gcm_2.append(df3['data'][i][s]-df1['data'][i][s])
#            print(df1['rcm'][i])
#            print(i,j)
#data_rcm_1p=[] 
#data_rcm_2p=[]          
#for i in range(len(df1)):
#    for j in range(len(pilote_liste)):
#        if df1['pilote'][i]==pilote_liste[j] and df1['rcm'][i]!='NotApplicable'and df1['rcp'][i]==rcp:
#            data_rcm_1p.append((df2p['data'][i][s]-df1p['data'][i][s])/df1p['data'][i][s]*100)
#            data_rcm_2p.append((df3p['data'][i][s]-df1p['data'][i][s])/df1p['data'][i][s]*100)
#            print(df1['rcm'][i])
#            print(i,j)
#data_gcm_1p=[]
#data_gcm_2p=[]           
#for i in range(len(df1)):
#    for j in range(len(pilote_liste)):
#        if df1['pilote'][i]==pilote_liste[j] and df1['rcm'][i]=='NotApplicable'and df1['rcp'][i]==rcp:
#            data_gcm_1p.append((df2p['data'][i][s]-df1p['data'][i][s])/df1p['data'][i][s]*100)
#            data_gcm_2p.append((df3p['data'][i][s]-df1p['data'][i][s])/df1p['data'][i][s]*100)
#            print(df1['rcm'][i])
#            print(i,j)
#data_climex_1=[]
#data_climex_2=[]
#for i in range(len(df1)):
#    if df1['groupe'][i]=='ClimEx'and df1['rcp'][i]==rcp:
#         data_climex_1.append(df2['data'][i][s]-df1['data'][i][s])
#         data_climex_2.append(df3['data'][i][s]-df1['data'][i][s])
#data_climex_1p=[]
#data_climex_2p=[]
#for i in range(len(df1)):
#    if df1['groupe'][i]=='ClimEx'and df1['rcp'][i]==rcp:
#         data_climex_1p.append((df2p['data'][i][s]-df1p['data'][i][s])/df1p['data'][i][s]*100)
#         data_climex_2p.append((df3p['data'][i][s]-df1p['data'][i][s])/df1p['data'][i][s]*100)
#
#plt.figure(1)
#plt.scatter(data_rcm_1,data_rcm_1p,color='r')
#plt.scatter(data_gcm_1,data_gcm_1p,color='g')
##plt.scatter(data_climex_1,data_climex_1p,color='grey')
#plt.legend(['RCM','Pilote'],loc=2)
#
#plt.figure(2)
#plt.scatter(data_rcm_2,data_rcm_2p,color='r')
#plt.scatter(data_gcm_2,data_gcm_2p,color='g')
##plt.scatter(data_climex_2,data_climex_2p,color='grey')
#plt.legend(['RCM','Pilote'],loc=2)

#if b_pt=='brute':
#    plt.title('Delta entre 1981-2010 et 2041-2070\n'+saison[s]+'_'+rcp+' (E_1)\nBrutes')
#    plt.savefig('/tank/begin/weighting/plots/brute/pr_tmoy_b_E_1_delta_pilote_2041_2070_'+rcp+'_'+saison[s],bbox_inches='tight')
#else:
#    plt.title('Delta entre 1981-2010 et 2041-2070\n'+saison[s]+'_'+rcp+' (E_1)\nPost-traitées')
#    plt.savefig('/tank/begin/weighting/plots/posttraite/pr_tmoy_pt_E_1_delta_pilote_2041_2070_'+rcp+'_'+saison[s],bbox_inches='tight')

