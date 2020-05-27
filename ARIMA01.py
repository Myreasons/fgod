from pandas import read_csv
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import fgod as fg
import functions_analyse as fa

clean_meth = fg.isolation_forest_anomaly_detection
#clean_meth = fg.low_pass_filter_anomaly_detection



series=clean_meth(df=fg.cleaner(), column_name='VOL_ACT')
series.plot(figsize=(15, 6))
plt.show()
writer = pd.ExcelWriter('after_clean.xlsx', engine='xlsxwriter')
series.to_excel(writer, 'Лист1')
writer.save()
