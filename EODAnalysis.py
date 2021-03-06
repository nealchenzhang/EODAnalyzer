# -*- coding: utf-8 -*-
#!/usr/bin/env python3
###############################################################################
#
# Created on Wed Jun 21 13:23:08 2017

# @author: nealcz @Aian_fund

# This program is personal trading platform desiged when employed in 
# Aihui Asset Management as a quantatitive analyst.
# 
# Contact: 
# Name: Chen Zhang (Neal)
# Mobile: (+86) 139-1706-0712
# E-mail: nealzc1991@gmail.com

###############################################################################
import sys
import os
import numpy as np
import pandas as pd
import datetime as dt

# zhfont_kai = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
# zhfont_song = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

class EOD_Analysis(object):
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def fetch_table(self, df_pdEOD, table_name):
        '''
        Input:
            df_pdEOD is pandas DataFrame for the 客户交易结算日报表格/成交明细/成交汇总（融航）核算信息
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
    
class Balance(EOD_Analysis):
    '''
    期货期权账户资金状况
    '''
    def __init__(self, filepath):
        EOD_Analysis.__init__(self, filepath)
        
        df_settlementfile = pd.read_excel(self.filepath, u'客户交易结算日报', header=None)
        #df_settlementfile = pd.read_excel(self.filepath, u'客户交易结算月报', header=None)
        tmp = self.fetch_table(df_settlementfile, u'期货期权账户资金状况')
        dic = {'Beging_Bal': tmp.loc[u'上日结存'].iloc[1],
               'Cash_Movement': tmp.loc[u'当日存取合计'].iloc[1],
               'Ending_Bal': tmp.loc[u'上日结存'].iloc[6],
#                'Realized_GL': tmp.loc[u'当日盈亏'].iloc[1],
               'Realized_GL': tmp.loc[u'平仓盈亏'].iloc[1],
               'Margin': tmp.loc[u'当日结存'].iloc[6],
               'Margin2Equity': float(tmp.iloc[7,6][:tmp.iloc[7,6].find('%')]),
               'Date': dt.datetime(*map(int, self.filepath.split('.')[0].split('_')[1].split('-')))}
        for i in dic.keys():
            setattr(self, i, dic[i])
    
class Tradings(EOD_Analysis):
    '''
    成交明细
    '''
    def __init__(self, filepath):
        EOD_Analysis.__init__(self, filepath)
        
        df_TradingOrders = pd.DataFrame()
        try:
            tmp = pd.read_excel(self.filepath, u'成交明细', header=None)
            pass
        except:
            tmp = pd.read_excel(self.filepath, u'成交汇总', header=None)
        try:
            df_TradingOrders = self.fetch_table(tmp, u'成交明细')
            pass
#            print('Error')
        except:
#            print('True')
#            print(tmp.columns)
            tmp.drop([0], axis=1, inplace=True)
#            tmp['Unnamed: 1'].apply(lambda x: x.upper() if x[0].isalpha)
            a = tmp.set_index([1])
            table_start = a.index.get_loc('合约')
            table_end = a.index.get_loc('合计')
            df_TradingOrders = a.iloc[table_start+1:table_end+1]
            df_TradingOrders.columns = ['成交序号', '成交时间', '买/卖',
                                        '投机/套保','成交价', '手数',
                                        '成交额','开/平', '手续费',
                                        '平仓盈亏', '资金账户报单编号',
                                       '实际成交日期']
            df_TradingOrders.index = [i.upper() for i in df_TradingOrders.index]
            df_TradingOrders.loc[:, u'实际成交日期'] = df_TradingOrders.loc[:, u'实际成交日期'].apply(pd.to_datetime)
#==============================================================================
#             
#==============================================================================
        if df_TradingOrders.index[-1] == u'合计':
            df_TradingOrders = df_TradingOrders.drop(u'合计', axis=0)
        
        df_TradingOrders.loc[:, u'平仓盈亏'] = df_TradingOrders.loc[:, u'平仓盈亏'].replace(u'--', np.nan)
        df_TradingOrders.loc[:, [u'实际成交日期', u'成交时间']] = \
        df_TradingOrders.loc[:, [u'实际成交日期', u'成交时间']].astype(str)
        
#        df_TradingOrders = df_TradingOrders.set_index('合约')
    
        setattr(self, 'Trading_Orders', df_TradingOrders)
    
class Positions(EOD_Analysis):
    '''
    持仓汇总
    '''
    def __init__(self, filepath):
        EOD_Analysis.__init__(self, filepath)
        
        df_Positions = pd.DataFrame()
        tmp = pd.read_excel(self.filepath, u'客户交易结算日报', header=None)
        #tmp = pd.read_excel(self.filepath, u'客户交易结算月报', header=None)
        try:
            df_Positions = self.fetch_table(tmp, u'期货持仓汇总')
            if df_Positions.index[-1] == u'合计':
                df_Positions = df_Positions.drop(u'合计', axis=0)
        except:
            df_Positions = pd.DataFrame()
        
        setattr(self, 'Positions', df_Positions)

class Asset_Summary(EOD_Analysis):
    '''
    品种汇总
    '''
    def __init__(self, filepath):
        EOD_Analysis.__init__(self, filepath)
        
        df_Asset_Summary = pd.DataFrame()
        tmp = pd.read_excel(self.filepath, u'品种汇总', header=None)
        try:
            df_Asset_Summary = self.fetch_table(tmp, u'品种汇总')
            if df_Asset_Summary.index[-1] == u'合计':
                df_Asset_Summary = df_Asset_Summary.drop(u'合计', axis=0)
        except:
            df_Asset_Summary = pd.DataFrame()
        
        df_Asset_Summary = df_Asset_Summary.dropna(axis=1, how='all')
        
        setattr(self, 'Asset_Summary', df_Asset_Summary)

if __name__ == '__main__':
    folderpath = 'C:\\Users\\Aian Fund\\Desktop\\程序化\\祥泽6号\\保证金监控中心'
    folderpath = 'C:/Users/Aian Fund/Desktop/结算单/椰海/保证金监控中心'
    folderpath = 'C:/Users/Aian Fund/Desktop/李岩-杨斯同'
#    folderpath = 'C:/Users/Aian Fund/Desktop/结算单/元鼎2/保证金监控中心'
#    folderpath = 'C:/Users/Aian Fund/Desktop/陈晓丹'
    folderpath = 'C:/Users/Aian Fund/Desktop/yst'
    os.chdir(folderpath)
    os.listdir(folderpath)
#    x = EOD_Analysis(filepath)
#    x = Balance(filepath)
#    x = Tradings(filepath)
#    x = Positions(filepath)
#    x = Asset_Summary(filepath)
    ###
    df_Balance = pd.DataFrame()
    Bal_index = []
    Beging_Bal = []
    Cash_Movement = []
    Ending_Bal = []
    Margin = []
    Margin2Equity = []
    Realized_GL = []
    for i in os.listdir(folderpath):
        a = Balance(folderpath+'\\'+i)
        Beging_Bal.append(a.Beging_Bal)
        Cash_Movement.append(a.Cash_Movement)
        Ending_Bal.append(a.Ending_Bal)
        Realized_GL.append(a.Realized_GL)
        Margin.append(a.Margin)
        Margin2Equity.append(a.Margin2Equity)
        Bal_index.append(a.Date)
    
    df_Balance = pd.DataFrame({'Beginning Balance': Beging_Bal, 
                               'Cash Movement': Cash_Movement, 
                               'Ending Balance': Ending_Bal,
                               'Margin': Margin,
                               'Margin to Equity': Margin2Equity,
                               'Realized G/L': Realized_GL})
    df_Balance.index = Bal_index
    
    df_Balance.plot(x=df_Balance.index, y='Margin to Equity',)
    df_Balance.plot(x=df_Balance.index, y='Realized G/L')
    
    df_Balance.plot(x=df_Balance.index, y='Ending Balance')
    
    df_Balance['return'] = (df_Balance['Realized G/L'] / df_Balance['Ending Balance'].shift(1))
              
#    df_Balance['cum_return'] = np.cumprod((df_Balance['return']+1)[1:])
#    df_Balance['cum_return'].plot()
    df_Balance.to_excel('单账户.xlsx')
#    Assetmin = []
#    Assetmax = []
#    for i in os.listdir(folderpath):
#        a = Asset_Summary(folderpath+'\\'+i).Asset_Summary['平仓盈亏']
#        amin = a.argmin()
#        amax = a.argmax()
#        Assetmin.append(amin)
#        Assetmax.append(amax)
