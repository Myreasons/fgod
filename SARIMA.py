import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import fgod as fg
import functions_analyse as fa
#from datetime import datetime, date, time
import datetime as dt
import calendar

plt.style.use('fivethirtyeight')

count_of_forecast_steps = 1

clean_meth = fg.isolation_forest_anomaly_detection
#clean_meth = fg.low_pass_filter_anomaly_detection

y=clean_meth(df=fg.starter(), column_name='VOL_ACT')

y.plot(figsize=(15, 6))
#plt.show()
sz = 0


dw_ind=[0,0,0,0,0,0,0]
while sz <= 6:
    dw_ind[sz]= fa.average_day_of_week(number=sz, df=y, date_start=dt.datetime(2019,12,1))
    sz+=1
dw_ind_avg = sum(dw_ind)/len(dw_ind)
sz = 0
while sz <= 6:
    dw_ind[sz]= dw_ind[sz]/dw_ind_avg
    sz+=1
print(dw_ind)

wm_ind=[0,0,0,0,0]
szm = 0
while szm < 5:
    print(szm)
    wm_ind[szm]= fa.average_week_of_month(wn=szm, ws=y, month_start=dt.datetime(2019,12,1))
    szm+=1

wm_ind_avg = sum(wm_ind)/len(wm_ind)
sz = 0
while sz <= 4:
    wm_ind[sz]= wm_ind[sz]/wm_ind_avg
    sz+=1

print(wm_ind)
forecast_date_start = dt.datetime(2019,12,1)
k=calendar.monthrange(forecast_date_start.year,forecast_date_start.month)




forecast_month  = pd.DataFrame(index= pd.date_range(forecast_date_start, periods=k[1]).tolist() )
forecast_month['week_num'] = (forecast_month.index.values)
forecast_month['week_num'] = forecast_month['week_num'].dt.day // 7 + 1
forecast_month['week_day']=forecast_month.index.values
forecast_month['week_day'] = forecast_month['week_day'].dt.dayofweek





y = y['VOL_Clear'].resample('MS').sum()
print(y)

y.plot(figsize=(15, 6))
plt.show()

# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

warnings.filterwarnings("ignore") # specify to ignore warning messages

best_aic = 10000
new_aic = 0
best_param = (1,1,1)
best_sparam = (1,1,12)

for param in pdq:
   for param_seasonal in seasonal_pdq:
       try:
           mod = sm.tsa.statespace.SARIMAX(y,
                                           order=param,
                                           seasonal_order=param_seasonal,
                                           enforce_stationarity=False,
                                           enforce_invertibility=False)

           results = mod.fit()

           print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
           new_aic = results.aic
           if new_aic <= best_aic:
               best_param = param
               best_sparam = param_seasonal
               best_aic = new_aic
       except:
           continue


#(1,1,1)(1,1,1,12) заменены на best_ в соответствии со сравнением aic по наименьшему результату

print('BEST ARIMA{}x{}12 - AIC:{}'.format(best_param, best_sparam, best_aic))
mod = sm.tsa.statespace.SARIMAX(y,
                               order=best_param,
                               seasonal_order=best_sparam,
                               enforce_stationarity=False,
                               enforce_invertibility=False)

results = mod.fit()

print(results.summary().tables[1])

#Этот метод очень привередлив к параметру lags. Установил как 6, но, мб придется изменить. Какой-то баг SARIMAX.
results.plot_diagnostics(figsize=(15, 12), lags=6)
plt.show()

pred = results.get_prediction(start=pd.to_datetime('2019-01-01'), dynamic=False)
pred_ci = pred.conf_int()

ax = y['2017':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

ax.fill_between(pred_ci.index,
               pred_ci.iloc[:, 0],
               pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Date')
ax.set_ylabel('VOL_Clear')
plt.legend()
#plt.show()

y_forecasted = pred.predicted_mean
y_truth = y['2019':]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

pred_dynamic = results.get_prediction(start=pd.to_datetime('2019-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()

ax = y['2017':].plot(label='observed', figsize=(20, 15))
pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)

ax.fill_between(pred_dynamic_ci.index,
               pred_dynamic_ci.iloc[:, 0],
               pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)

ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2017'), y.index[-1],
                alpha=.1, zorder=-1)

ax.set_xlabel('Date')
ax.set_ylabel('VOL_Clear')

plt.legend()
plt.show()

# Extract the predicted and true values of our time series
y_forecasted = pred_dynamic.predicted_mean
y_truth = y['2019':]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

# Get forecast for some steps ahead in future
pred_uc = results.get_forecast(steps=count_of_forecast_steps)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()

ax = y.plot(label='observed', figsize=(20, 15))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
               pred_ci.iloc[:, 0],
               pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('VOL_Clear')

plt.legend()
plt.show()

print('XAXAXAXAXAXAXAXAXXAXAXAXAXA')
print(pred_ci)




#а тут мои приколы

month_vol_average = (pred_ci['lower VOL_Clear']+pred_ci['upper VOL_Clear'])/2
mva = pd.to_numeric(month_vol_average.values, errors='coerce').sum()

print('aaaaa')
print(mva)
print('aaaaa')
forecast_month['Volume']= mva / len(forecast_month)

forecast_month['week_day_ind']=1
forecast_month['week_num_ind']=1

for ind in forecast_month.index.values:
    forecast_month['week_day_ind'].loc[ind]=dw_ind[(forecast_month['week_day'].loc[ind])]
    forecast_month['week_num_ind'].loc[ind]=wm_ind[(forecast_month['week_num'].loc[ind])-1]

forecast_month['Volume']=forecast_month['Volume']*forecast_month['week_day_ind']*forecast_month['week_num_ind']

print(forecast_month)
forecast_month.plot(figsize=(15, 6))
plt.show()
