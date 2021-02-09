import os
import numpy as np
import pandas as pd

FILEPATH = 'E:/datasets/ESS/dataset'
datasets = os.listdir(FILEPATH)
datasets = datasets[4:]

# Process owid data
owid_path = os.path.join(FILEPATH, datasets[0])
owid_df = pd.read_csv(owid_path)

owid_features = ['iso_code', 'country', 'year', 'co2_per_capita']

owid_df = owid_df.loc[owid_df['year'] == 2018 , owid_features]
owid_df = owid_df.loc[owid_df['iso_code'].notnull()]
owid_df = owid_df.loc[owid_df['iso_code'] != 'OWID_WRL']
owid_df = owid_df.set_index('iso_code')
owid_df.to_csv("newdata/owid.csv")

# Process GNI data
gni_path = os.path.join(FILEPATH, datasets[2])
gni_df = pd.read_csv(gni_path)

gni_features = ['Country Name', 'Country Code', '2018']
not_countries = ['ARB', 'CEB', 'CSS', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS',
                 'EMU', 'EUU', 'FCS', 'HIC', 'HPC', 'IBD','IBT', 'IDA',
                 'IDB', 'IDX', 'INX', 'LAC', 'LCN', 'LDC', 'LIC', 'LKA',
                 'LMC', 'LMY', 'LTE', 'MEA', 'MIC', 'MNA', 'OED', 'PRE',
                 'PST', 'SSA', 'SSF', 'SST', 'TEA', 'TEC', 'TLA', 'TMN', 
                 'TSA', 'TSS', 'UMC', 'WLD']

gni_df = gni_df.loc[:, gni_features]

for code in not_countries:
    gni_df = gni_df[gni_df['Country Code'] != code]
    
gni_df = gni_df.rename(columns = {'2018':'GNI per capita, PPP (current international $)'})
gni_df = gni_df.set_index('Country Code')
gni_df.to_csv("newdata/gni.csv")

# Process Population Data
pop_path = os.path.join(FILEPATH, datasets[3])
pop_df = pd.read_csv(pop_path)

pop_features = ['Country Name', 'Country Code', '2018']
pop_df = pop_df.loc[:, pop_features]

for code in not_countries:
    pop_df = pop_df[pop_df['Country Code'] != code]
    
pop_df = pop_df.rename(columns = {'2018':'Population'})
pop_df = pop_df.set_index('Country Code')
pop_df.to_csv("newdata/pop.csv")

# Process Waste Data
waste_path = os.path.join(FILEPATH, datasets[1])
waste_df = pd.read_csv(waste_path)
waste_features = ['iso3c', 'total_msw_total_msw_generated_tons_year']

waste_df = waste_df.loc[:, waste_features]
waste_df = waste_df.rename(columns = {'total_msw_total_msw_generated_tons_year':'Total Waste (tons)',
                                      'iso3c':'Country Code'})
waste_df = waste_df.set_index('Country Code')
waste_df.to_csv("newdata/waste.csv")