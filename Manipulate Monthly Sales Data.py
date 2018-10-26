import pandas as pd
import os
import numpy as np


#set dir#
os.chdir(r'')

#set current dir as path##

path = os.getcwd()

# Collect CSV files
pattern = path + *'.csv'

csv_files = glob.glob(pattern)

# Create an empty list
frames = []

#  Iterate over csv_files
for csv in csv_files:
    df = pd.read_csv(csv, dtype = object)
    frames.append(df)

# Concatenate frames into a single DataFrame
dfs = pd.concat(frames)

## Import Master Data File ##

df1 = pd.read_csv(r'ArticleData.csv')

## change Article column to int64 ## 

df1 = df1[pd.to_numeric(df1['Article'], errors='coerce').notnull()]

##Change dtype to int##
df1['Article'] = df1['Article'].astype(int)

##Join Master Data into dfs##

merged = pd.merge(df,df1)

## Ensure Date is an actual datetime dtype ## 
merged['Calendar day'] = pd.to_datetime(merged['Calendar day'].str.replace('.','/'),format="%d/%m/%Y")




