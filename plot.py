# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Created on Tue Jun 13 10:04:11 2017

# @author: nealcz @Aian_fund

# This program is personal trading platform desiged when employed in 
# Aihui Asset Management as a quantatitive analyst.
# 
# Contact: 
# Name: Chen Zhang (Neal)
# Mobile: (+86) 139-1706-0712
# E-mail: nealzc1991@gmail.com

###############################################################################

import pandas as pd
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import matplotlib.dates as mdates
import datetime as dt

### PP Data
os.chdir('D:\\Neal\\EODAnalyzer')
pp = pd.read_excel('PP1709.xlsx')
pp = pp.iloc[:, 0:5]
columns = ['Timestamp', 'Open', 'High', 'Low', 'Close']
pp.columns = columns
pp = pp.drop(pp.index[-2:])

ppp = pp.iloc[-300:]
ppp = ppp.set_index('Timestamp', drop=True)

### Orders 
df_Orders = x.backtest_trading('pp')

df_Orders.loc[:, 'Timestamp'] = df_Orders.loc[:, 'Timestamp'].apply(pd.Timestamp)
df_Orders = df_Orders.set_index('Timestamp', drop=True)

pd.merge(ppp, df_Orders, how='inner', on=[ppp.index])

Order_4_plot = pd.concat([ppp, df_Orders], axis=1, join='inner')
### Plot
Order_4_plot = Order_4_plot.reset_index()
Order_4_plot.loc[:, 'Time'] = Order_4_plot.loc[:,'Timestamp'].apply(mdates.date2num)
Prices = [(Order_4_plot.iloc[a,5], Order_4_plot.iloc[a,1], Order_4_plot.iloc[a,2], Order_4_plot.iloc[a,3], Order_4_plot.iloc[a,4]) for a in range(len(Order_4_plot.index))]


ppp = ppp.reset_index()
ppp.loc[:, 'Time'] = ppp.loc[:, 'Timestamp'].apply(mdates.date2num)
Prices2 = [(ppp.iloc[a,5], ppp.iloc[a,1], ppp.iloc[a,2], ppp.iloc[a,3], ppp.iloc[a,4]) for a in range(len(ppp.index))]

########################


fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.3)
#########
#OPEN = Order_4_plot.loc[:,'Open'][0:2]
#HIGH = Order_4_plot.loc[:,'High'][0:2]
#LOW = Order_4_plot.loc[:,'Low'][0:2]
#CLOSE = Order_4_plot.loc[:, 'Close'][0:2]
#mpf.candlestick2_ohlc(ax, OPEN, HIGH, LOW, CLOSE, width=2, colorup='r', colordown='g')
########
#ax.xaxis.set_major_locator
ax.set_xticks(ppp.loc[:,'Time'])
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:00'))

mpf.candlestick_ohlc(ax, Prices2, width=0.5)

##
#plt.gca()
#plt.plot(Order_4_plot.loc[:, 'Timestamp'], Order_4_plot.loc[:, u'成交价'], 'v')

ax.xaxis_date()

ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()
