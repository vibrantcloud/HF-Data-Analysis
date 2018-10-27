import glob
import pandas as pd
import os
from datetime import datetime

## Import Modules& set dir ## 

os.chdir(r'')
cwd = os.getcwd()

## Set Path to Concat Files ## 

path = cwd

## Find all files with xlsx ending and pass them to a list ## 

allFiles = glob.glob(path + "/*.xlsx")
frame = pd.DataFrame()
list_ = []

## Loop over list and pass them to individual dataframes remove headers ## 

for file_ in allFiles:
    df = pd.read_excel(file_,index_col=None, header=0)
    list_.append(df)

## Concat all files into one ##     

frame = pd.concat(list_)
df = frame
## Same Process as above but for Aspire ## 
os.chdir(r'')
cwd = os.getcwd()


path = cwd

allFiles = glob.glob(path + "/*.xlsx")
frame2 = pd.DataFrame()
list_ = []


for file_ in allFiles:
    df2 = pd.read_excel(file_,index_col=None, header=0)
    list_.append(df2)

frame2 = pd.concat(list_)

## Drop Duplicates ## 

df = df[~df.duplicated(['Username', 'Course Name'], keep=False) | df.Status.ne('Booked','Requested','Fully Attended')]

## Merge Aspire & Non Aspire File ##

finaldfs = [frame2, df]
final_df = pd.concat(finaldfs)



df3 = final_df[final_df.Status != 'User Cancelled']
## Save to Excel in a Specified Directory ## 

from datetime import date
today = date.today().strftime('%Y_%m_%d')
print(today)   # '2017-12-26


df3.to_excel(today +'_Extra Hours.xlsx',index=False)
