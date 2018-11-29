import pandas as pd
import numpy as np
import os

file = input(r"Enter your File Path : ")

df = pd.read_csv(file +".csv")

## Melt the Curent DF ## 
new_df = pd.melt(df,id_vars=['ID'],var_name=['Store'],value_name='Score').fillna(0).set_index('ID')

# sort index so all the 'Date' values are at the bottom
new_df.sort_index(inplace=True) 

# create a new df of just the dates becuase that is your review types
review_types = new_df.loc['Date']

# rename column to review types
review_types.rename(columns={'Score':'Review Type'}, inplace=True)

# remove new_df.loc['Date']
new_df = new_df.drop(new_df.tail(len(review_types)).index).reset_index()

# rename ID column to Date
new_df.rename(columns={'ID':'Date'}, inplace=True)

# merge your two dataframes together
new_df = new_df.merge(review_types, on='Store')
new_df['Store'] = new_df['Store'].astype(str).str.replace('.1','')

