import pandas as pd


## Creates a Financial week number from the selected date column ##

df['Week'] = np.where(df['Dates'].dt.month >= 4, (df['Dates'] + pd.Timedelta(days=2)).dt.week - 13,
                       (df['Dates'] + pd.Timedelta(days=2)).dt.week + 39)
                       
                       
 ## Gets the Financial Year ##
 
 df['Year'] = np.where(df['Dates'].dt.month >= 4,  df['Dates'].dt.year +1, 
                        df['Dates'].dt.year
                       )
                       
                       
     
