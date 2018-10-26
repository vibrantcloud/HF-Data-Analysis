import pandas as pd
import os
import numpy as np
from itertools import chain


## Set the path to the data files: ##

PATH_TO_FILES = '/your/path/here/'


## Read in the Data as Pandas DataFrames (csv files, in this example): ## 

frames = list()

for csv in [os.path.join(PATH_TO_FILES, f) for f in os.listdir(PATH_TO_FILES) if f.endswith('.csv')]:
    frames.append(pd.read_csv(csv))


##Define a function to flatten large 2D lists quickly:##

def fast_flatten(input_list):
    return list(chain.from_iterable(input_list))


##Next, construct a dictionary using the column names from one of the dataframes (located at index 0):##

COLUMN_NAMES = frames[0].columns


##Now, construct a dictionary from the column names:##

df_dict = dict.fromkeys(COLUMN_NAMES, [])


## Iterate though the columns:##

for col in COLUMN_NAMES:
    # Use a generator to save memory
    extracted = (frame[col] for frame in frames)

    # Flatten and save to df_dict
    df_dict[col] = fast_flatten(extracted) 
## Lastly use the from_dict method to produce the combined DataFrame: ## 

df = pd.DataFrame.from_dict(df_dict)[COLUMN_NAMES]


