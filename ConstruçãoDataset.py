# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:06:31 2022

@author: userDCPS
"""

import pandas as pd
import numpy as np
from pyproj import Proj
import warnings
warnings.filterwarnings("ignore")
from pykdtree.kdtree import KDTree
import time

# Carregando todos os arquivos BATIMÉTRICOS de todas as resoluções.
df_bat_2m = pd.read_csv("C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\Madeira_13e14_WGS84_UTM28N_2m.txt",
                      skiprows=1,delim_whitespace=True,names=['utmx','utmy','z'])
df_bat_2m['res'] = '2m'
df_bat_4m = pd.read_csv("C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\Madeira_13e14_WGS84_UTM28N_4m.txt",
                      skiprows=1,delim_whitespace=True,names=['utmx','utmy','z'])
df_bat_4m['res'] = '4m'
df_bat_8m = pd.read_csv("C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\Madeira_13e14_WGS84_UTM28N_8m.txt",
                      skiprows=1,delim_whitespace=True,names=['utmx','utmy','z'])
df_bat_8m['res'] = '8m'
df_bat_16m = pd.read_csv("C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\Madeira_13e14_WGS84_UTM28N_16m.txt",
                      skiprows=1,delim_whitespace=True,names=['utmx','utmy','z'])
df_bat_16m['res'] = '16m'
df_bat_32m = pd.read_csv("C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\Madeira_13e14_WGS84_UTM28N_32m.txt",
                      skiprows=1,delim_whitespace=True,names=['utmx','utmy','z'])
df_bat_32m['res'] = '32m'
df_bat_64m = pd.read_csv("C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\Madeira_13e14_WGS84_UTM28N_64m.txt",
                      skiprows=1,delim_whitespace=True,names=['utmx','utmy','z'])
df_bat_64m['res'] = '64m'

# Criando arquivo único da batimetria, com coluna associada à resolução.
df_bat = pd.concat([df_bat_2m,df_bat_4m,df_bat_8m,df_bat_16m,df_bat_32m,df_bat_64m,],axis=0)
del df_bat_2m,df_bat_4m,df_bat_8m,df_bat_16m,df_bat_32m,df_bat_64m

# Carregando dado sísmico
df_sbp = pd.read_csv(r"C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\Thickness_MadeiraNW.txt",sep=';')

# Convertendo de projeção geográfica WGS84 para UTM WGS84
df_sbp['LATITUDE'] = df_sbp['LATITUDE'].str.replace(',','.')
df_sbp['LATITUDE'] = df_sbp['LATITUDE'].astype("float")
df_sbp['LONGITUDE'] = df_sbp['LONGITUDE'].str.replace(',','.')
df_sbp['LONGITUDE'] = df_sbp['LONGITUDE'].astype("float")
df_sbp['classe'] = 1
df_sbp['classe'][df_sbp[df_sbp['THICKNESS_']!=0].index] = 0

myProj = Proj("+proj=utm +zone=28 +north +ellps=WGS84 +datum=WGS84 +units=m")
utmx, utmy = myProj(df_sbp.LONGITUDE, df_sbp.LATITUDE) 
df_sbp['utmx'] = utmx
df_sbp['utmy'] = utmy

# Pegando somente colunas de interesse
df_sbp = df_sbp[['utmx','utmy','classe']]
del utmx,utmy





#PYKDTREE
kd_tree = KDTree(df_bat[['utmx','utmy']].values)
start = time.time()
dist, idx = kd_tree.query(df_sbp[df_sbp.classe==0][['utmx','utmy']].values, k=1)
end = time.time()
print(end - start)










