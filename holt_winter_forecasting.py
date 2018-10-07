import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

sales_tg = pd.read_csv('forecasting/SalesTG/Variant Report.csv', dtype={'Variant SKU': 'str'}, parse_dates=['Issued At'])
sales_2010 = sales_tg[(sales_tg['Customer Type'] == 'consumer') & (sales_tg['Variant SKU'] == '2010')][['Customer Name', 'Quantity', 'Issued At', 'Location Name']].reset_index().sort_values('Issued At')
sales_2010.head(20)

sales_2010[sales_2010['Issued At'] < '2017-01-01']['Quantity'].sum()

sales_2010_month = sales_2010.set_index('Issued At').resample('M').sum().drop('index', axis =1)

sales_2010_month.plot()

holt_model = ExponentialSmoothing(endog=sales_2010_month, seasonal_periods=12).fit(smoothing_level=0.6)
import datetime
holt_model.predict(123, start=datetime.date(2016, 6,1), end = '2017-12-31')
