import sys, os
import warnings

import pandas as pd
import numpy as np
import sqlalchemy

from app.database import engine

sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

warnings.filterwarnings('ignore')
pd.set_option('display.float_format', lambda x: '%.3f' % x)

cols = [
    'DR_NO', 
    'Date Rptd', 
    'DATE OCC', 
    'TIME OCC', 
    'AREA ', 
    'AREA NAME',
    'Rpt Dist No', 
    'Part 1-2', 
    'Crm Cd', 
    'Crm Cd Desc', 
    'Mocodes',
    'Vict Age', 
    'Vict Sex', 
    'Vict Descent', 
    'Premis Cd', 
    'Premis Desc',
    'Weapon Used Cd', 
    'Weapon Desc', 
    'Status', 
    'Status Desc', 
    'Crm Cd 1',
    'Crm Cd 2', 
    'Crm Cd 3', 
    'Crm Cd 4', 
    'LOCATION', 
    'Cross Street', 
    'LAT',
    'LON']


col_map = {}
for c in cols:
    col_map[c] = c.strip().replace(' ', '_').replace('-', '_').lower()
print(col_map)


df = pd.read_csv('https://data.lacity.org/api/views/63jg-8b9z/rows.csv?accessType=DOWNLOAD', index_col=False)
df.rename(columns=col_map, inplace=True)

df['date_rptd'] = pd.to_datetime(df['date_rptd'])
df['date_occ'] = pd.to_datetime(df['date_occ'])
for column in df.columns:
    if column == 'part_1_2':
        continue
    if df[column].dtype == 'int64':
        df[column] = df[column].astype(str)
    if column in ['premis_cd', 'weapon_used_cd', 'crm_cd_1', 'crm_cd_2', 'crm_cd_3', 'crm_cd_4']:
        df[column] = df[column].astype(str)

df_part = df[df['date_rptd']<'2015-01-01']
df_part = df_part.replace('nan', '')

print(df_part.shape)
print(df_part.columns)


df_part.to_sql('crimes', engine, if_exists='append', index=False)
