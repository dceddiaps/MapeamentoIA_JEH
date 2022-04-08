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
from scipy.spatial.distance import cdist

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

# Carregando dado SÍSMICO
df_sbp = pd.read_csv(r"C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\Thickness_MadeiraNW.txt",sep=';')

# Convertendo de projeção geográfica WGS84 para UTM WGS84
df_sbp['LATITUDE'] = df_sbp['LATITUDE'].str.replace(',','.')
df_sbp['LATITUDE'] = df_sbp['LATITUDE'].astype("float")
df_sbp['LONGITUDE'] = df_sbp['LONGITUDE'].str.replace(',','.')
df_sbp['LONGITUDE'] = df_sbp['LONGITUDE'].astype("float")
df_sbp['THICKNESS_'] = df_sbp['THICKNESS_'].str.replace(',','.')
df_sbp['THICKNESS_'] = df_sbp['THICKNESS_'].astype("float")
df_sbp['classe'] = 1
df_sbp['classe'][df_sbp[df_sbp['THICKNESS_']!=0].index] = 0

myProj = Proj("+proj=utm +zone=28 +north +ellps=WGS84 +datum=WGS84 +units=m")
utmx, utmy = myProj(df_sbp.LONGITUDE, df_sbp.LATITUDE) 
df_sbp['utmx'] = utmx
df_sbp['utmy'] = utmy

# Pegando somente colunas de interesse da sísmica
df_sbp = df_sbp[['utmx','utmy','classe']]
del utmx,utmy

# Carregando dados de BACKSCATTER
df_bs = pd.read_csv(r"C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\backscatter.txt",
                    names = ['utmx','utmy','bs'])

# Carregando dados de DECLIVIDADE DO FUNDO
df_sl = pd.read_csv(r"C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\slope.xyz",
                    names = ['utmx','utmy','sl'])

# Carregando dados de ORIENTAÇÃO DA DECLIVIDADE DO FUNDO
df_as = pd.read_csv(r"C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\aspect.xyz",
                    names = ['utmx','utmy','as'])

# Carregando dados da DECLIVIDADE SUBMARINA
df_ds = pd.read_csv(r"C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\declive submarino.txt",
                    usecols=[0,1],names = ['utmx','utmy'])

# Carregando dados de LINHA DE COSTA
df_lc = pd.read_csv(r"C:\DCPS\GitHub\Dados_MapeamentoIA_JEH\linha de costa.txt",
                    usecols=[0,1],names = ['utmx','utmy'])

# PYKDTREE

# Correlacionando sísmica com batimetria
kd_tree = KDTree(df_bat[['utmx','utmy']].values)
start = time.time()
dist, idx = kd_tree.query(df_sbp[['utmx','utmy']].values, k=1)
end = time.time()
print(end - start)

# Salvando correlação de batimetria no dataset final
data = df_sbp
data['z'] = df_bat.z.iloc[idx].values
data['z_res'] = df_bat.res.iloc[idx].values
data['z_dist'] = dist

# Correlacionando sísmica com backscatter
kd_tree = KDTree(df_bs[['utmx','utmy']].values)
start = time.time()
dist, idx = kd_tree.query(df_sbp[['utmx','utmy']].values, k=1)
end = time.time()
print(end - start)

# Salvando correlação de batimetria no dataset final
data['bs'] = df_bs.bs.iloc[idx].values
data['bs_dist'] = dist

# Correlacionando sísmica com declividade do fundo
kd_tree = KDTree(df_sl[['utmx','utmy']].values)
start = time.time()
dist, idx = kd_tree.query(df_sbp[['utmx','utmy']].values, k=1)
end = time.time()
print(end - start)

# Salvando correlação de declividade do fundo no dataset final
data['sl'] = df_sl.sl.iloc[idx].values
data['sl_dist'] = dist

# Correlacionando sísmica com orientação da declividade do fundo
kd_tree = KDTree(df_as[['utmx','utmy']].values)
start = time.time()
dist, idx = kd_tree.query(df_sbp[['utmx','utmy']].values, k=1)
end = time.time()
print(end - start)

# Salvando correlação de declividade do fundo no dataset final
data['as'] = df_as['as'].iloc[idx].values
data['as_dist'] = dist

# DISTANCIA EUCLIDIANA DA LINHA DE COSTA
dist = cdist(data[['utmx','utmy']],df_lc,metric='euclidean')
np.argpartition(np.transpose(dist[:,0]),1)[0]
data['dist_costa'] = -999
for i in range(len(dist)):
    data['dist_costa'].iloc[i] = np.min(dist[i,:])

# DISTANCIA EUCLIDIANA DO DECLIVE SUBMARINO
dist = cdist(data[['utmx','utmy']],df_ds,metric='euclidean')
np.argpartition(np.transpose(dist[:,0]),1)[0]
data['dist_declivesub'] = -999
for i in range(len(dist)):
    data['dist_declivesub'].iloc[i] = np.min(dist[i,:])






