import warnings
import itertools
import statsmodels.api as sm
import numpy as np
import pandas as pd
import functions_analyse as fa
from datetime import datetime, date, time
import sklearn as sk
from sklearn.ensemble import IsolationForest
import sesd
from sklearn.svm import OneClassSVM

pd.options.mode.chained_assignment = None



def starter(path):
    #file = 'datas.xlsx'
    file = path
    y = pd.read_excel(file, index_col=0)
    y = y.fillna(y.bfill())
    return y
'''
def cleaner():
    file = '2clean.xlsx'
    y = pd.read_excel(file, index_col=0)
    return y

'''
"""
Простой фильтр нижних частот: взятие скользящего среднего и устранение аномалий на основе Z-показателя
"""
def low_pass_filter_anomaly_detection(event, df,
                                      column_name):

    """
    Implement a low-pass filter to detect anomalies in a time series, and save the filter outputs
    (True/False) to a new column in the dataframe.
    Arguments:
        df: Pandas dataframe
        column_name: string. Name of the column that we want to detect anomalies in
        number_of_stdevs_away_from_mean: float. Number of standard deviations away from
        the mean that we want to flag anomalies at. For example, if
        number_of_stdevs_away_from_mean=2,
        then all data points more than 2 standard deviations away from the mean are flagged as
        anomalies.
    Outputs:
        df: Pandas dataframe. Dataframe containing column for low pass filter anomalies
        (True/False)
    """

    number_of_stdevs_away_from_mean = 3
    #60-day rolling average
    df[column_name+'_Rolling_Average']=df[column_name].rolling(window=60, center=True).mean()
    #60-day standard deviation
    df[column_name+'_Rolling_StDev']=df[column_name].rolling(window=60, center=True).std()
    #Detect anomalies by determining how far away from the mean (in terms of standard deviation)
    #each data point is
    df['Filter_Anomaly']=(abs(df[column_name]-df[
                                column_name+'_Rolling_Average'])>(
                                number_of_stdevs_away_from_mean*df[
                                column_name+'_Rolling_StDev']))
    #df['Cleaned']=np.where(df['VOL_ACT_Low_Pass_Filter_Anomaly'] == True, datetime(2019,2,2),df['VOL_ACT'])
    df['Clear '+column_name]=df[column_name]
    for ind in df.index.values:
        if df['Filter_Anomaly'].loc[ind]  == True:
            df['Clear '+column_name].loc[ind] = fa.P_clean(df, ind, column_name)

    df = df.drop([column_name+'_Rolling_StDev',column_name+'_Rolling_Average'], axis = 1)


    print(df)
    return df

"""Изоляция Леса"""

def isolation_forest_anomaly_detection(event, df,
                                       column_name):
    """
    In this definition, time series anomalies are detected using an Isolation Forest algorithm.
    Arguments:
        df: Pandas dataframe
        column_name: string. Name of the column that we want to detect anomalies in
        outliers_fraction: float. Percentage of outliers allowed in the sequence.
    Outputs:
        df: Pandas dataframe with column for detected Isolation Forest anomalies (True/False)
    """
    outliers_fraction = .04
    #Scale the column that we want to flag for anomalies
    min_max_scaler = sk.preprocessing.StandardScaler()
    np_scaled = min_max_scaler.fit_transform(df[[column_name]])
    scaled_time_series = pd.DataFrame(np_scaled)
    # train isolation forest
    model = IsolationForest(contamination = outliers_fraction, behaviour='new')
    model.fit(scaled_time_series)
    #Generate column for Isolation Forest-detected anomalies
    isolation_forest_anomaly_column = 'Filter_Anomaly'
    df[isolation_forest_anomaly_column] = model.predict(scaled_time_series)
    df[isolation_forest_anomaly_column] = df[isolation_forest_anomaly_column].map( {1: False, -1: True} )
    df['Clear '+column_name] = df[column_name]
    for ind in df.index.values:
        if df['Filter_Anomaly'].loc[ind]  == True:
            df['Clear '+column_name].loc[ind] = fa.P_clean(df,ind,column_name)


    return df
