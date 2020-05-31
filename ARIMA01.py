from pandas import read_csv
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import fgod as fg
import functions_analyse as fa
'''
clean_meth = fg.isolation_forest_anomaly_detection
#clean_meth = fg.low_pass_filter_anomaly_detection



series=clean_meth(df=fg.cleaner(), column_name='VOL_ACT')
series.plot(figsize=(15, 6))
plt.show()
writer = pd.ExcelWriter('after_clean.xlsx', engine='xlsxwriter')
series.to_excel(writer, 'Лист1')
writer.save()
'''

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2, right=0.85)
newax = fig.add_axes(ax.get_position())
newax.patch.set_visible(False)
newax.yaxis.set_label_position('right')
newax.yaxis.set_ticks_position('right')
newax.spines['bottom'].set_position(('outward', 35))
ax.plot(range(10), 'r-')
ax.set_xlabel('Red X-axis', color='red')
ax.set_ylabel('Red Y-axis', color='red')
x = np.linspace(0, 6 * np.pi)
newax.plot(x, 0.001 * np.cos(x), 'g-')
newax.set_xlabel('Green X-axis', color='green')
newax.set_ylabel('Green Y-axis', color='green')
plt.show()