"""

Get the latest bank holidays from the UK Gov't Website, useful for highlighting key dates and outliers in sales and marketing activities. 


"""

import requests
import pandas as pd
import json

# Import Modules. 

url = "https://www.gov.uk/bank-holidays.json"

r = requests.get(url)
d = r.json()

df = pd.DataFrame.from_dict(d)
print(df)
"""
                                         england-and-wales  \
division                                  england-and-wales   
events    [{'title': 'New Year’s Day', 'date': '2012-01-...   

                                                   scotland  \
division                                           scotland   
events    [{'title': '2nd January', 'date': '2012-01-02'...   

                                           northern-ireland  
division                                   northern-ireland  
events    [{'title': 'New Year’s Day', 'date': '2012-01-...  
"""

dfs = []

for country, data in d.items():
    df = pd.DataFrame(data['events'])
    df['Country'] = country
    dfs.append(df)

final = pd.concat(dfs, ignore_index=True)

print(final.head(5))

"""
bunting	date	notes	title	Country
0	True	2012-01-02	Substitute day	New Year’s Day	england-and-wales
1	False	2012-04-06		Good Friday	england-and-wales
2	True	2012-04-09		Easter Monday	england-and-wales
3	True	2012-05-07		Early May bank holiday	england-and-wales
4	True	2012-06-04	Substitute day	Spring bank holiday	england-and-wales
"""

