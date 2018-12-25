## Script for getting weather, wind speed, humidity, pressure and the next 7 days of postcodes by post code. 

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import pandas as pd
from IPython.core.display import clear_output
from time import time
import pandas as pd

df = pd.read_excel()

todays_max = []
todays_min = []
description = []

wind_speed = []
pressure = []
visiblity = []
humidity = []

day_1_max = []
day_2_max = []
day_3_max = []
day_4_max = []
day_5_max = []
day_6_max = []
day_7_max = []


day_1_min = []
day_2_min = []
day_3_min = []
day_4_min = []
day_5_min = []
day_6_min = []
day_7_min = []


requests = 0
start_time = time()




def get_todays_weather(dataframe):
    requests = 0
    start_time = time()
    for x in df['Post Codes'].str.lower():
            try:
                driver=webdriver.Chrome(r"C:\Users\hussa\Downloads\chromedriver.exe")
                driver.get("https://www.bbc.co.uk/weather/0/" + x)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                requests += 1
                elapsed_time = time() - start_time
                print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
                clear_output(wait = True)
                driver.quit()
                #Today's Weather High
                today_max = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[1].text.strip()
                # Today's Weather Low
                today_min = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[0].text.strip()
                # Description
                des = soup.findAll("div",{"class" : "wr-day__details__weather-type-description"})[0].text.strip()
                wind_s = soup.findAll('span',{'class': 'wr-value--windspeed wr-value--windspeed--mph'})[15].text.strip()
                humid = soup.findAll('li',{'class': 'wr-c-station-data__observation gel-long-primer gs-u-pl0 gs-u-mv--'})[0].text.strip()
                visib = soup.findAll('li',{'class': 'wr-c-station-data__observation gel-long-primer gs-u-pl0 gs-u-mv--'})[1].text.strip()
                press = soup.findAll('li',{'class': 'wr-c-station-data__observation gel-long-primer gs-u-pl0 gs-u-mv--'})[2].text.strip()
                #Following Days 7#
                #Day 1 Date
                d1 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[0].text.strip()
                #Day 1 Temp min & max
                d1max = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[3].text.strip()
                d1min = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[2].text.strip()
                #Day2 Date
                d2 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[1].text.strip()
                #Day 2 Temp min & max
                d2max = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[5].text.strip()
                d2min = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[4].text.strip()
                #Day 3 date
                d3 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[2].text.strip()
                #Day 3 Temp min & max
                d3max = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[7].text.strip()
                d3min = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[6].text.strip()
                #Day 4 Date
                d4 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[3].text.strip()
                #Day 4 Temp min & max
                d4max = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[9].text.strip()
                d4min = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[8].text.strip()
                #Day 5 Date
                d5 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[4].text.strip()
                #Day 5 Temp min & max
                d5max = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[11].text.strip()
                d5min = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[10].text.strip()
                #Day 6 Date
                d6 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[5].text.strip()
                #Day 6 Temp min & max
                d6max = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[13].text.strip()
                d6min = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[12].text.strip()
                #Day 7 Date
                d7 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[6].text.strip()
                #Day 7 Temp min & max
                d7max = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[15].text.strip()
                d7min = soup.findAll("span",{"class" : 'wr-value--temperature--c'})[14].text.strip()
                todays_max.append(today_max)
                todays_min.append(today_min)
                description.append(des)
                day_1_min.append(d1min)
                day_2_min.append(d2min)
                day_3_min.append(d3min)
                day_4_min.append(d4min)
                day_5_min.append(d5min)
                day_6_min.append(d6min)
                day_7_min.append(d7min)
                day_1_max.append(d1max)
                day_2_max.append(d2max)
                day_3_max.append(d3max)
                day_4_max.append(d4max)
                day_5_max.append(d5max)
                day_6_max.append(d6max)
                day_7_max.append(d7max)
                pressure.append(press)
                visiblity.append(visib)
                wind_speed.append(wind_s)
                humidity.append(humid)
            except IndexError:
                d1min = 'Post Code Not Working'
                d2min = 'Post Code Not Working'
                d3min = 'Post Code Not Working'
                d4min = 'Post Code Not Working'
                d5min = 'Post Code Not Working'
                d6min = 'Post Code Not Working'
                d7min = 'Post Code Not Working'
                d1max = 'Post Code Not Working'
                d2max = 'Post Code Not Working'
                d3max = 'Post Code Not Working'
                d4max = 'Post Code Not Working'
                d5max = 'Post Code Not Working'
                d6max = 'Post Code Not Working'
                d7max = 'Post Code Not Working'
                today_max = 'Post Code Not Working'
                today_min = 'Post Code Not Working'
                des = 'Post Code Not Working'
                press = 'Post Code Not Working'
                visib = 'Post Code Not Working'
                wind_s = 'Post Code Not Working'
                humid = 'Post Code Not Working'
                todays_max.append(today_max)
                todays_min.append(today_min)
                description.append(des)
                day_1_min.append(d1min)
                day_2_min.append(d2min)
                day_3_min.append(d3min)
                day_4_min.append(d4min)
                day_5_min.append(d5min)
                day_6_min.append(d6min)
                day_7_min.append(d7min)
                day_1_max.append(d1max)
                day_2_max.append(d2max)
                day_3_max.append(d3max)
                day_4_max.append(d4max)
                day_5_max.append(d5max)
                day_6_max.append(d6max)
                day_7_max.append(d7max)
                pressure.append(press)
                visiblity.append(visib)
                wind_speed.append(wind_s)
                humidity.append(humid)
  
 Get dates and create data frame
 
 
 driver=webdriver.Chrome(r"C:\Users\hussa\Downloads\chromedriver.exe")
driver.get("https://www.bbc.co.uk/weather/0/b23")
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()


d1 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[0].text.strip()
d2 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[1].text.strip()
d3 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[2].text.strip()
d4 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[3].text.strip()
d5 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[4].text.strip()
d6 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[5].text.strip()
d7 = soup.findAll("span",{"class" : 'wr-date__longish__dotm'})[6].text.strip()



df2 = pd.DataFrame({'Post Code' : df['Post Codes'],
              'Humidity' : humidity,
              'Visiblity' : visiblity,
              'Wind Speed' : wind_speed,
              'Pressure' : pressure,
              'Today Max' : todays_max,
              'Today Min' : todays_min,
              'Description' : description,
              d1 + ' Max' : day_1_max,
              d1 + ' Min' : day_1_min,
              d2 + ' Max' : day_2_max,
              d2 + ' Min' : day_2_min,
              d3 + ' Max' : day_3_max,
              d3 + ' Min' : day_3_min,
              d4 + ' Max' : day_4_max,
              d4 + ' Min' : day_4_min,
              d5 + ' Max' : day_5_max,
              d5 + ' Min' : day_5_min,
              d6 + ' Max' : day_6_max,
              d6 + ' Min' : day_6_min,
              d7 + ' Max' : day_7_max,
              d7 + ' Min' : day_7_min})
