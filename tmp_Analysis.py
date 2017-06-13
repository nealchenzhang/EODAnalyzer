# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:37:58 2017

@author: Aian Fund
"""
import sys
import os
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib

zhfont_kai = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
zhfont_song = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

from Sectors import Sector

sector = Sector()

sector.pairs_trading(1) = ['J','JM']
list2 = ['I', 'RB', 'HC']
list3 = ['IC', 'IF']
number = '0123456789'

df_Margin = pd.DataFrame(columns=['Margin_list1', 'Margin_list2', 'Margin_list3'], index=x.Balance().index)


for i in x.filelist:
    df_tmp = pd.read_excel(i, u'客户交易结算日报', header=None)
    df_tmp= x.fetch_table(df_tmp, u'期货持仓汇总')
    p = i.split('.')[0].split('_')[1]
    Margin_list1 = 0
    Margin_list2 = 0
    Margin_list3 = 0
    for m in range(df_tmp.index.size):
        if df_tmp.index[m].rstrip(number) in list1:
            a = df_tmp.iloc[m][u'交易保证金']
            Margin_list1 += a
            Margin_list2 += 0
            Margin_list3 += 0
        elif df_tmp.index[m].rstrip(number) in list2:
            a = df_tmp.iloc[m][u'交易保证金']
            Margin_list1 += 0
            Margin_list2 += a
            Margin_list3 += 0
        elif df_tmp.index[m].rstrip(number) in list3:
            a = df_tmp.iloc[m][u'交易保证金']
            Margin_list1 += 0
            Margin_list2 += 0
            Margin_list3 += a
        
    df_Margin.loc[p, 'Margin_list1'] = Margin_list1
    df_Margin.loc[p, 'Margin_list2'] = Margin_list2
    df_Margin.loc[p, 'Margin_list3'] = Margin_list3

df_Margin.loc[:,'Margin'] = df_Balance.loc[:,'Margin']

df_Margin.loc[:,'Margin1%'] = df_Margin.loc[:,'Margin_list1'] / df_Margin.loc[:,'Margin']
df_Margin.loc[:,'Margin2%'] = df_Margin.loc[:,'Margin_list2'] / df_Margin.loc[:,'Margin']
df_Margin.loc[:,'Margin3%'] = df_Margin.loc[:,'Margin_list3'] / df_Margin.loc[:,'Margin']

df_Margin.loc[:,'Margin4%'] = df_Margin.loc[:,'Margin1%'] + df_Margin.loc[:,'Margin2%']
df_Margin.loc[:,['Margin3%','Margin4%']].plot()
plt.title('板块保证金比例', fontproperties=zhfont_kai)



#############
filepath = 'C:\\Users\\Aian Fund\\Desktop\\御澜保证金监控中心'
x = EOD_Analysis(filepath, u'御澜')
x = Trading_Analysis(filepath, 'yl', x.start_date, x.end_date)
df_Orders = x.df_Orders()
df_Orders = df_Orders.reset_index()
df_Orders = df_Orders.rename(columns={0:'合约'})
df_analysis = df_Orders.groupby(['Timestamp', u'合约', u'买/卖', u'开/平', u'手数'])[u'成交价',u'平仓盈亏'].sum()
df_analysis = df_analysis.reset_index().set_index('Timestamp')
#df_analysis.loc[:, '累计盈亏'] = pd.rolling_sum(df_analysis.loc[:, '平仓盈亏'], 2)

len(list(set(df_analysis.loc[:,'合约'])))
df_a = df_analysis.loc['2017-04-24 09:00:04':,:]
df_a.sort()

df = df_Orders.where((df_Orders.loc[:, '合约']=='J1709') | (df_Orders.loc[:, '合约']=='JM1709'))
df = df.dropna(how='all')
df = df.groupby(['Timestamp', u'合约', u'买/卖', u'开/平', u'手数'])[u'成交价',u'平仓盈亏'].sum()
df = df.reset_index().set_index('Timestamp')

df1 = df_Orders.where((df_Orders.loc[:, '合约']=='J1709') | (df_Orders.loc[:, '合约']=='RB1710') | (df_Orders.loc[:, '合约']=='I1709'))
df1 = df1.dropna(how='all')
df1 = df1.groupby(['Timestamp', u'合约', u'买/卖', u'开/平', u'手数'])[u'成交价',u'平仓盈亏'].sum()
df1 = df1.reset_index().set_index('Timestamp')

df2 = df_Orders.where((df_Orders.loc[:, '合约']=='J1705') | (df_Orders.loc[:, '合约']=='RB1705') | (df_Orders.loc[:, '合约']=='I1705'))
df2 = df2.dropna(how='all')
df2 = df2.groupby(['Timestamp', u'合约', u'买/卖', u'开/平', u'手数'])[u'成交价',u'平仓盈亏'].sum()
df2 = df2.reset_index().set_index('Timestamp')

df3 = df_Orders.where((df_Orders.loc[:, '合约']=='J1705') | (df_Orders.loc[:, '合约']=='RB1705') | (df_Orders.loc[:, '合约']=='I1705') | (df_Orders.loc[:, '合约']=='J1709') | (df_Orders.loc[:, '合约']=='RB1710') | (df_Orders.loc[:, '合约']=='I1709'))
df3 = df3.dropna(how='all')
df3 = df3.groupby(['Timestamp', u'合约', u'买/卖', u'开/平', u'手数'])[u'成交价',u'平仓盈亏'].sum()
df3 = df3.reset_index().set_index('Timestamp')
df4 = df_Orders.where((df_Orders.loc[:, '合约']=='J1709') | (df_Orders.loc[:, '合约']=='JM1709') | (df_Orders.loc[:, '合约']=='J1705') | (df_Orders.loc[:, '合约']=='JM1705'))
df4 = df4.dropna(how='all')

df_bc = df4.groupby(['Timestamp', u'合约', u'买/卖', u'开/平', u'手数'])[u'成交价',u'平仓盈亏'].sum()
df_a = df4.groupby(['Timestamp', u'合约', u'买/卖', u'开/平', u'手数'])
df = df.groupby(['Timestamp',u'合约', u'买/卖', u'开/平', u'手数'])[u'平仓盈亏']
df4 = df4.reset_index().set_index('Timestamp')

