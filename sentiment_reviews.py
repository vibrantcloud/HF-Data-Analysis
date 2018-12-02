
import pandas as pd
import os
import numpy as np

df = pd.read_csv(r'C:\Users\hussa\Downloads\Google Reviews Report - Comments.csv')
## Melt Data Frame and change from wide to long 

new_df = pd.melt(df,id_vars=['Store code','Review comment'],var_name=['Score'],value_name='Date').fillna(0).set_index('Store code')

## Rename Columns  ## 
new_df.rename(columns={'Score' : 'Date', 'Date': 'Attribution'},inplace=True)


## remove 0's these are useless duplicates ## 
df1 = new_df.loc[new_df['Attribution'] != 0].copy()

## Drop Duplicates as a row was created for every Date, but we only want to keep the data where the first 1 or 2 appeared. ##
df1.drop_duplicates(subset=['Review comment'],keep='first',inplace=True)


## Apply Sentiment to Review Column, seperate functions to allow nulls and non text fields that throw up errors. ##
from textblob import TextBlob

def polarity_calc(text):
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return None

df1['Polarity'] = df1['Review comment'].apply(polarity_calc)

## Subjectivity could probably write this into one function..# 

def objectivity_calc(text):
    try:
        return TextBlob(text).sentiment.subjectivity
    except:
return None

df1['Subjectivity'] = df1['Review comment'].apply(objectivity_calc)

## Create a WordCloud ##

df2 = df1.loc[df1['Review comment'] != 0]
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

cloud = WordCloud(background_color="white", max_words=50, stopwords=stopwords.words('english'))

positive_cloud = cloud.generate(df2['Review comment'].str.cat(sep='\n'))
plt.figure()
plt.imshow(positive_cloud)
plt.axis("off")
plt.show()
