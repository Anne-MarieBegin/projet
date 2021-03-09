#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:34:36 2019

@author: begin

v20201216 Ouvre fichier, sélectionne 1971-2000(moins 1995 1996 29 fev), fait une moyenne par année/mois, fait une moyenne sur le domaine, enregistre 

"""
import xclim as xc
from xclim import subset
import xarray as xr
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
var = 'pr' #changer ligne 58
b_pt='brute'# brute ou posttraite
SE='SE_1_complet'#sous-ensemble

#open all files in repertory
dd=[]
path=('/tank/begin/weighting/'+SE+'/'+b_pt+'/'+var)  
#path=('/tank/begin/weighting/SE_1/brute/'+var)  #observations
files=os.listdir(path)
files.sort()
for i in files:
    dd.append(path+'/'+i)
    
#Make dataset with all files
ds=[]
for j in range(0,len(files)):    
    ds.append(xr.open_mfdataset(dd[j]))

#calcul distance en degre entre deux points de latitude
#avec exception pour valeur manquante
diff_lat=[]
for i in range(0,len(ds)):
    try:
        diff_lat.append(float(np.mean(ds[i].lat[1]-ds[i].lat[0])))
    except Exception as err:
        diff_lat.append(None)
        print(err)

#calcul distance en degre entre deux points de longitude
#avec exception grille NAM pas bonne valeur avec lon
        # a partir de 110 lon en 2D alors [:,1]
diff_lon=[]
for i in range(0,110):
    try:
        diff_lon.append(float(np.mean(ds[i].rlon[1]-ds[i].rlon[0])))
    except Exception as err:
        diff_lon.append(float(np.mean(ds[i].lon[1]-ds[i].lon[0])))
        print(err)
for i in range(110,len(ds)):
    try:
        diff_lon.append(float(np.mean(ds[i].rlon[1]-ds[i].rlon[0])))
    except Exception as err:
        diff_lon.append(float(np.mean(ds[i].lon[:,1]-ds[i].lon[:,0])))
        print(err)
               
#calcul de la distance en km des degres de latitude
#avec exception pour valeur manquante        
dis_lat=[]
for i in range(0,len(diff_lat)):
    try:
        dis_lat.append(round(diff_lat[i]*2*3.1416*6371/360,0))
    except Exception as err:
        dis_lat.append(None)
        print(err)   

#calcul de la distance en km des degres de longitude
#avec exception pour valeur manquante 
dis_lon=[]
for i in range(0,len(diff_lat)):
    try:
        dis_lon.append(round(diff_lon[i]*2*3.1416*6371/360,0))
    except Exception as err:
        dis_lon.append(None)
        print(err)    

#calcul distance moyenne entre lon et lat
#avec exception pour valeur manquante 
dis_moy=[]
for i in range(0,len(diff_lat)):
    try:
        dis_moy.append(round((dis_lat[i]+dis_lon[i])/2,0))
    except Exception as err:
        dis_moy.append(dis_lon[i])
        print(err)

#condition 1 et 2*delta(X) plus petit que dimension bassin versant L1
L1=[25,200,1000,5000,25000,50000,100000,200000,500000,1000000] #km2

nombre_total_1=[]#1*deltaX
for y in range(0,len(L1)):
    nombre=[]
    for i in range(0,len(ds)):
        if dis_moy[i]<=np.sqrt(L1[y]):
            nombre.append(i)
    print(len(nombre))
    nombre_total_1.append(len(nombre))
    
nombre_total_2=[]#2*delataX
for y in range(0,len(L1)):
    nombre=[]
    for i in range(0,len(ds)):
        if 2*dis_moy[i]<=np.sqrt(L1[y]):
            nombre.append(i)
    print(len(nombre))
    nombre_total_2.append(len(nombre))

#plot dimension bassin versant vs nombre de simulation
legende=['2*$\Delta$X','1*$\Delta$X']
plt.figure(1)
plt.plot(L1,nombre_total_2,'.r')
plt.plot(L1,nombre_total_1,'xb')
plt.legend(legende)
plt.xscale('log')
plt.grid(True,which="both", linestyle='-')
plt.ylabel('Nombre de simulation sur 179')
plt.xlabel('Taille du bassin versant km²')
plt.title('Résolution minimale')
plt.savefig('/tank/begin/weighting/plots/resolution_minimale')