import matplotlib.pyplot as plt
import warnings
import itertools
import statsmodels.api as sm
import numpy as np
import pandas as pd
import fgod as fg
from datetime import datetime, date, time
plt.style.use('fivethirtyeight')

def P_clean(series,dater, param):
    bornline = dater-pd.offsets.Day(30)
    deadline = dater+pd.offsets.Day(30)
    s=series.loc[bornline:deadline]
    s = s[lambda x: x['Filter_Anomaly'] == False]
    s['weekday']=s.index.values
    s['weekday']=s['weekday'].dt.dayofweek
    s = s[lambda x: x['weekday'] == date.weekday(pd.Timestamp(dater))]
    i = len(s)
    sm = pd.to_numeric(s[param], errors='coerce').sum()
    sm = sm/i
    return sm

def average_day(num,dater,series, ms1):
    bornline = dater - pd.offsets.Day(80)
    deadline = dater - pd.offsets.Day(6)
    s = series.loc[bornline:deadline]
    s = s[lambda x: x['Filter_Anomaly'] == False]
    s['weekday'] = s.index.values
    s['weekday']=s['weekday'].dt.dayofweek
    s = s[lambda x: x['weekday'] == num]
    i = len(s)
    sm = pd.to_numeric(s[ms1], errors='coerce').sum()
    sm = sm/i
    return sm

def average_day_of_week(number,df,date_start,ms):
    dw = average_day(num=number,dater=date_start, series= df,ms1=ms)
    return dw

def average_week_of_month(month_start, ws,wn, ms):
    wn+=1
    ws = ws.loc[month_start:]
    ws['week_num'] = (ws.index.values)
    ws['week_num'] = ws['week_num'].dt.day // 7 + 1
    ws = ws[lambda x: x['week_num'] == wn]
    i = len(ws)
    sm = pd.to_numeric(ws[ms], errors='coerce').sum()
    sm = sm / i
    return sm

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

def kdf(y, ttl):
    test = sm.tsa.adfuller(y)
    print('adf: ', test[0])
    print('p-value: ', test[1])
    print('Critical values: ', test[4])
    if test[0] > test[4]['5%']:
        rez = ('Есть единичные корни, ряд не стационарен')
    else:
        rez = ('Единичных корней нет, ряд стационарен')
    #y.plot(figsize=(15, 6), title= rez + ': ' + ttl)
    #plt.show()
    return(rez)

def anti_stac(otg):
    otg1diff = otg.diff(periods=1).dropna()
    return (otg1diff)