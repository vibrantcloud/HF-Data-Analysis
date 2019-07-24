import pandas as pd
import numpy as np
import os

file = ''
df = pd.read_csv(file)

## Melt the Curent DF ## 
new_df = pd.melt(df,id_vars=['ID'],var_name=['Store'],value_name='Score').fillna(0).set_index('ID')

# sort index so all the 'Date' values are at the bottom
new_df.sort_index(inplace=True) 

# create a new df of just the dates because that is your review types
review_types = new_df.loc['Date']

# rename column to review types
review_types.rename(columns={'Score':'Review Type'}, inplace=True)

# remove new_df.loc['Date']
new_df = new_df.drop(new_df.tail(len(review_types)).index).reset_index()

# rename ID column to Date
new_df.rename(columns={'ID':'Date'}, inplace=True)

# merge your two dataframes together
new_df = new_df.merge(review_types, on='Store')
new_df = new_df[['Store','Date','Score','Review Type']].copy()
new_df['Store'] = new_df['Store'].astype(str).str.replace('.1','')
new_df2 = new_df.loc[new_df.Score != 0].copy()


new_df.to_csv('Cleaned_Reviews.csv',index=False)
new_df2.to_csv('Cleaned_Reviews_NaNs_Removed.csv',index=False)

""" 
Unsure of Data so creating both variants of the code.

"""


df1.rename(columns={'Review Type' : 'Reviews'},inplace=True)
df2.rename(columns={'Review Type' : 'Average Review'},inplace=True)
df1.rename(columns={'Score' : 'Count'},inplace=True)
df3 = pd.merge(df1,df2,on=['Date','Store'],how='left')
df3 = df3[['Store','Date','Reviews','Count','Average Review','Score']].copy()

df3.to_csv('Greviews.csv',index=False)
