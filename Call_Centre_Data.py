import pandas as pd
from os.path import basename
import os
import glob


os.chdir(r'')
path = os.getcwd()
allFiles = glob.glob(path + "/*.csv")

frame = pd.DataFrame()
master_list = []


dfs = [pd.read_excel(f,index_col=None,header=1) for f in allFiles]

keys = [os.path.basename(f) for f in allFiles]
frame = pd.concat(dfs, keys=keys)

df1['Shop'] = df1.loc[df1.Interval.str.contains('Queue')]
df1.Shop.ffill(inplace=True)

df['Date'] = pd.to_datetime(df.Date)

df1 = df.loc[~df.Interval.str.contains('Total', 'Rel:')]

