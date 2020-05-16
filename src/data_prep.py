#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import HTML
import matplotlib
import numpy as np


# In[6]:


# df_verhuurd = pd.read_csv('C:\\Users\\jniens\\GoogleDrive\\Python_Projects\\real_estate_analysis\\data_files\\csv\\verhuurde_woningen_driemaanden.csv', sep=';')
# df_verkocht = pd.read_csv('C:\\Users\\jniens\\GoogleDrive\\Python_Projects\\real_estate_analysis\\data_files\\csv\\verkochte_woningen_driemaanden.csv', sep=';')
# df_stadsdelen = pd.read_csv('C:\\Users\\jniens\\GoogleDrive\\Python_Projects\\real_estate_analysis\\data_files\\csv\\dim_stadsdelen3.csv', sep=';')


# In[7]:


def prep_df(df_fact, df_stadsdelen):
    
    "Make id column"
    df_fact['Huisnr.'] = df_fact['Huisnr.'].fillna(0).astype(int).astype(str)
    df_fact['Toev.'] = df_fact['Toev.'].fillna('')
    
    df_fact['id'] = df_fact.Straat + "-" +     df_fact['Huisnr.'].astype(int).astype(str) + "-" +     df_fact['Toev.']
    
    "Convert currency columns to number columns"
    col_name_dict = {'Huidige prijs' : 'huidige_prijs', 
                 'Prijs per m2' : 'prijs_perm2' ,
                'Transactie prijs / huur' : 'transactieprijs', 
                 'Huidige huur' : 'huidige_huur',
                'Transactieprijs per m2' : 'transactieprijs_perm2'}

    "Convert euro column to type number"
    for cur_col, new_col in col_name_dict.items():
        df_fact[new_col] = df_fact[cur_col].str.replace('€', '')         .str.replace(',', '')
        df_fact[new_col] = pd.to_numeric(df_fact[new_col], errors='coerce')

    
    "Extract number from Postcode column"
    df_fact.loc[:, 'Postcode_cijfers'] = df_fact.Postcode.str[:4].astype(int).copy()
    
    "Join stadsdelen via postcode cijfers"
    df_fact = df_fact.merge(df_stadsdelen, left_on='Postcode_cijfers', right_on='postcode', how='left')

    "Select subset columns"
    cols = [
        'id', 
        'postcode',
        'stadsdeel',
        'Soort OG',
        'Soort appartement',
        'Aantal kamers', 
        'Dagen op de markt',
        'Woonoppervlakte',
        'Inhoud woning',
        'Status',
        #'Makelaar',
        'Datum aanmelding',
        'Transactiedatum',      
        'Huur conditie',
        'Koop conditie',
        'huidige_huur',
        'huidige_prijs',
        'prijs_perm2',
        'transactieprijs', 
        'transactieprijs_perm2'                  
    ]

    df_fact = df_fact[cols]
    
    "Make indicators"
    df_fact['trans_eq_huid'] = df_fact.transactieprijs_perm2.eq(df_fact.prijs_perm2)
    df_fact['trans_gt_huid'] = df_fact.transactieprijs_perm2.gt(df_fact.prijs_perm2)
    df_fact['trans_lt_huid'] = df_fact.transactieprijs_perm2.lt(df_fact.prijs_perm2)
    
    "Convert date columns to pd.datetime format"
    dateformat = '%d-%m-%Y'
    df_fact['Transactiedatum'] = pd.to_datetime(df_fact['Transactiedatum'], format=dateformat)
    df_fact['Datum aanmelding'] = pd.to_datetime(df_fact['Datum aanmelding'], format=dateformat)
    
    "Set id column as index"
    df_fact = df_fact.set_index('id')
    
    return df_fact

