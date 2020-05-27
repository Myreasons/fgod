import matplotlib.pyplot as plt
import warnings
import itertools
import statsmodels.api as sm
import numpy as np
import pandas as pd
import fgod as fg
from datetime import datetime, date, time


def P_clean(series,dater):
    bornline = dater-pd.offsets.Day(30)
    deadline = dater+pd.offsets.Day(30)
    s=series.loc[bornline:deadline]
    s = s[lambda x: x['Filter_Anomaly'] == False]
    s['weekday']=s.index.values
    s['weekday']=s['weekday'].dt.dayofweek
    s = s[lambda x: x['weekday'] == date.weekday(pd.Timestamp(dater))]
    i = len(s)
    sm = pd.to_numeric(s['VOL_ACT'], errors='coerce').sum()
    sm = sm/i
    return sm


def average_day(num,dater,series):
    bornline = dater - pd.offsets.Day(80)
    deadline = dater - pd.offsets.Day(6)
    s = series.loc[bornline:deadline]
    s = s[lambda x: x['Filter_Anomaly'] == False]
    s['weekday'] = s.index.values
    s['weekday']=s['weekday'].dt.dayofweek
    s = s[lambda x: x['weekday'] == num]
    i = len(s)
    sm = pd.to_numeric(s['VOL_Clear'], errors='coerce').sum()
    sm = sm/i
    return sm

def average_day_of_week(number,df,date_start):
    dw = average_day(num=number,dater=date_start, series= df)
    return dw

def average_week_of_month(month_start, ws,wn):
    wn+=1
    ws = ws.loc[month_start:]
    ws['week_num'] = (ws.index.values)
    ws['week_num'] = ws['week_num'].dt.day // 7 + 1
    ws = ws[lambda x: x['week_num'] == wn]
    i = len(ws)
    sm = pd.to_numeric(ws['VOL_Clear'], errors='coerce').sum()
    sm = sm / i
    #print(ws)
    return sm
def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)