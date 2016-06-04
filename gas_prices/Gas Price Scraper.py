#Run with python3

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import datetime

base_url = 'http://gasprices.aaa.com?state='
states= ['AZ', 'NV', 'CA', 'OR', 'WA', 'VA']
date=datetime.datetime.now().strftime("%m/%d/%Y")


def fetchPrices(state):
    #setup
    url=base_url+state
    req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_week = urlopen(req).read()
    soup = BeautifulSoup(html_week, 'html.parser')
    
    metroPrices=soup.find("div", {"class": "accordion-prices"})
    h3=metroPrices.select("h3")
    tables=metroPrices.select("table")
    
    #create dataframe
    rowList=[]
    for i in range(len(h3)):
        city=h3[i].text
        entries=tables[i*4+2].select("td")
        regular=entries[1].text[1:]
        mid=entries[3].text[1:]
        premium=entries[5].text[1:]
        diesel=entries[7].text[1:]
        rowList.append((date, state, city, diesel, regular, mid, premium))
    return rowList

rowList=[]
for state in states:
    print('fetching', state)
    rowList+=fetchPrices(state)
columns=['Date', 'State', 'City', 'Diesel', 'Regular', 'Mid', 'Premium']
gas_prices=pd.DataFrame(rowList, columns=columns)

gas_prices.to_csv("aaa-price.csv", index=False)




