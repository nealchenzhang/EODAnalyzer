# -*- coding: utf-8 -*-
"""
Created on Wed May 03 10:27:42 2017

@author: Neal Chen Zhang
"""
from __future__ import print_function
from __future__ import division

import sys
import os
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl

# zhfont_kai = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
# zhfont_song = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

#plt.title('楷体',fontproperties=zhfont_kai)
#plt.xlabel('$\lambda$')
#plt.ylabel('宋体',fontproperties=zhfont_song)
#plt.text( 0.35, 0.66, '这里是中文', fontproperties=zhfont_kai,fontsize=30,rotation=45)
#plt.show()

class EOD_Analysis(object):
    
    def __init__(self, filepath, accountname):
        os.chdir(filepath)
        self.filelist = os.listdir(filepath)
        self.account_name = accountname
        self.account_id = str(self.filelist[0].split('.')[0].split('_')[0])
        self.start_date = str(self.filelist[0].split('.')[0].split('_')[1])
        self.end_date = str(self.filelist[-1].split('.')[0].split('_')[1])
    
    def fetch_table(self, df_pdEOD, table_name):
        '''
        Input:
            df_pdEOD is pandas DataFrame for the 客户交易结算日报表格/成交明细
            table_name include:
                基本资料
                期货期权账户资金状况
                其它资金明细
                期货期权账户出入金明细
                其他资金明细
                期货成交明细
                期货持仓汇总
                成交明细
        
        Output:
            return df_table for particular table_name
        
        '''
        df_table = df_pdEOD.set_index([0])
        index_list = df_table.index
        table_start = 0
        table_end = 0
        if table_name == u'基本资料':
            table_start = index_list.get_loc(table_name)
            table_end = table_start + 3
            df_table = df_table.iloc[table_start:table_end + 1]
            df_table.columns = df_table.iloc[0,:]
            df_table = df_table.drop(df_table.index[0])
        elif table_name == u'期货期权账户资金状况':
            table_start = index_list.get_loc(table_name)
            table_end = table_start + 9
            df_table = df_table.iloc[table_start:table_end + 1]
            df_table.columns = df_table.iloc[0,:]
            df_table = df_table.drop(df_table.index[0])
        else:                
            for i in index_list:
                if str(i).startswith(table_name):
                    table_start = index_list.get_loc(i)
                    table_end = np.where(index_list[table_start:] == u'合计')[0][0] \
                                + table_start                
            df_table = df_table.iloc[table_start:table_end + 1]
            df_table.columns = df_table.iloc[1,:]
            df_table = df_table.drop(df_table.index[0:2])
        return df_table

    def Balance(self):
        '''
        账户资金情况汇总:
            期初权益；
            出入金；
            期末权益
        '''
        df_Balance = pd.DataFrame()
        Bal_index = []
        Beging_Bal = []
        Cash_Movement = []
        Ending_Bal = []
        Margin = []
        Margin2Equity = []
        Realized_GL = []
        for i in self.filelist:
            df_settlementfile = pd.read_excel(i, u'客户交易结算日报', header=None)
            tmp = self.fetch_table(df_settlementfile, u'期货期权账户资金状况')
            Beging_Bal.append(tmp.loc[u'上日结存'].iloc[1])
            Cash_Movement.append(tmp.loc[u'当日存取合计'].iloc[1])
            Ending_Bal.append(tmp.loc[u'上日结存'].iloc[6])
            Realized_GL.append(tmp.loc[u'平仓盈亏'].iloc[1])
            Margin.append(tmp.loc[u'当日结存'].iloc[6])
            Margin2Equity.append(float(tmp.iloc[7,6][:tmp.iloc[7,6].find('%')]))
            Bal_index.append(dt.datetime(*map(int, i.split('.')[0].split('_')[1].split('-'))))
        
        df_Balance = pd.DataFrame({'Beginning Balance': Beging_Bal, 
                                   'Cash Movement': Cash_Movement, 
                                   'Ending Balance': Ending_Bal,
                                   'Margin': Margin,
                                   'Margin to Equity': Margin2Equity,
                                   'Realized G/L': Realized_GL})
        df_Balance.index = Bal_index
#        
#        plt.figure()
#        ax1 = plt.subplot(2,1,1)
#        ax1.plot(df_Balance.index, df_Balance.loc[:,'Ending Balance'])
#        ax1.set_title('Ending Balance')
#        ax2 = plt.subplot(2,1,2, sharex=ax1)
#        ax2.bar(df_Balance.index, df_Balance.loc[:, 'Margin'])
#        ax2.set_title('Margin')
#        plt.xlabel('Date')
#        plt.title('Margin to Equity')
        return df_Balance
        

    def Trading_Orders(self, date_start, date_end):
        files_dates = [str(i.split('.')[0].split('_')[1]) for i in self.filelist]
        df_TradingOrders = pd.DataFrame()
        if date_start and date_end in files_dates:
            tradingfiles = self.filelist[files_dates.index(date_start):files_dates.index(date_end)+1]
            for i in tradingfiles:
                df_tradingfile = pd.read_excel(i, u'成交明细', header=None)
                tmp = self.fetch_table(df_tradingfile, u'成交明细')
                if tmp.index[-1] == u'合计':
                    tmp = tmp.drop(u'合计', axis=0)
                df_TradingOrders = df_TradingOrders.append(tmp)
        else: print('Please re-enter the period for analysis.')
        df_TradingOrders.loc[:, u'平仓盈亏'] = df_TradingOrders.loc[:, u'平仓盈亏'].replace(u'--', np.nan)
        df_TradingOrders.loc[:, [u'实际成交日期', u'成交时间']] = \
        df_TradingOrders.loc[:, [u'实际成交日期', u'成交时间']].astype(str)

        return df_TradingOrders
        

if __name__ == '__main__':
#    filepath = r'C:\\Users\\Aian Fund\\Desktop\\王亚民'
    filepath = r'C:\\Users\\Aian Fund\\Desktop\\御澜保证金监控中心'
#    filepath = '/media/nealcz/Data/Neal/EODAnalyzer/御澜保证金监控中心'
    x = EOD_Analysis(filepath, u'御澜')