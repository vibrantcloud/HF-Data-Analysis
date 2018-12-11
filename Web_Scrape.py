from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import numpy as np


for x in df['Product ID']:
    search_url = murl + x
    print(search_url)
    uclient = uReq(search_url)
    print(uclient)
    page_html = uclient.read()
    uclient.close()
    page_soup = soup(page_html,"html.parser")
    rp = page_soup.findAll("h2",{"class" : 'highlightValue'})[0].text.strip()
    
    
