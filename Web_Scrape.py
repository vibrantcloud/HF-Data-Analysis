from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import numpy as np

query = 
search url = 'https://www.halfords.com/webapp/wcs/stores/servlet/SearchRouter?langId=-1&storeId=10001&catalogId=10151&action=search&srch=' + query
response = get(url)
print(response.text[:500])


