import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select
import pyodbc
import os



server = r'prod'
database = 'database'
username = 'username'
password = 'pw'


cnxn = pyodbc.connect('Driver={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

sql = "SELECT * FROM dbo.Xh19"

df = pd.read_sql(sql,cnxn)


df.columns = [i if not i.startswith('Week') else int(i[-1]) for i in df]

res = pd.melt(df, id_vars='Store', var_name='Week', value_name='Hours')\
        .sort_values('Store').reset_index(drop=True)

xh19 = res.loc[res.Store != '#N/A']

xh19['Extra'] = "Extra"


