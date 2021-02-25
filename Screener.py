import os
import time
import yfinance as yf
import dateutil.relativedelta
from datetime import date
import datetime
import numpy as np
import sys
from tqdm import tqdm
from joblib import Parallel, delayed, parallel_backend
import multiprocessing
import ftplib


STANDARD_DEV = 10
stocks = []

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'tickers.txt')) as t:
    for stock in t:
        stocks.append(stock.strip())

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def get_volume(ticker):
    currentDate = datetime.date.today() + datetime.timedelta(days=1)
    pastDate = currentDate - \
        dateutil.relativedelta.relativedelta(months=3)
    data = yf.download(ticker, pastDate, currentDate)
    return data['Volume']

def find_unusual_volume(volume_list):
    unusual_dates = []
    unusual_volumes = []
    indices = volume_list.index
    standard_deviation = np.std(volume_list)
    mean = np.mean(volume_list)
    unusual = mean + standard_deviation*STANDARD_DEV
    volume_list = volume_list.tail()
    for volume in range(len(volume_list)):
        
        if volume_list.iloc[volume]>=unusual:
            unusual_volumes.append(volume_list.iloc[volume])

            unusual_dates.append(indices[volume])
    return (unusual_dates, unusual_volumes)

def date_difference(date1):
    date2 = datetime.date.today()

    year, month, day = (str(date1)[:-9]).split('-')
    date1 = datetime.date(int(year), int(month), int(day) )
    return date2-date1

def find_unusual_stocks(stock_list):
    unusual_stocks_list = []
    unusual_date_list = []
    for stock in stock_list:
        print(stock)
        date, stocks = find_unusual_volume(get_volume(stock))
        if len(date) > 0 and date_difference(date[-1]).days < 7:
            print(f'Found Stock: {stock}')
            unusual_stocks_list.append(stock)
            unusual_date_list.append(date)
    return unusual_stocks_list



#blockPrint()
print(find_unusual_stocks(stocks))
#enablePrint()




