# -*- coding: utf-8 -*-
"""
Created on Fri May 19 10:28:04 2017

@author: Aian Fund
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import os
import numpy as np

from EODAnalysis import EOD_Analysis

class Trading_Analysis(EOD_Analysis):
    # Define futures contracts.
    number = '0123456789'
    SHFE = ['AL','CU','ZN','RU','FU','AU','RB',
            'WR','PB','AG','BU','HC','NI','SN']
    DCE = ['P','L','M','Y','A','C','B','PVC','J',
           'JM','I','JD','FB','BB','PP','CS']
    CZCE = ['TA','SR','WH','PM','CF','OI','RI',
            'MA','FG','RS','RM','ZC','JR','LR',
            'SF','SM']
    CFFEX = ['IF','IH','IC','T','TF']
    Contracts = {i:'SHFE' for i in SHFE}
    Contracts.update({i:'DCE' for i in DCE})
    Contracts.update({i:'CZCE' for i in CZCE})
    Contracts.update({i:'CFFEX' for i in CFFEX})
    
    '''
    
    '''
    
    def __init__(self, filepath, accountname, date_start, date_end):
        EOD_Analysis.__init__(self, filepath, accountname)
        self.date_start = date_start
        self.date_end = date_end
    
    def df_Prev_Position(self):
        '''
        This function is used to check the previous trading date position.
        
        Return raw data from EOD files.
        '''
        tmp_date = dt.datetime.strptime(self.date_start, '%Y-%m-%d')
        if tmp_date.isoweekday() == 1:
            prev_date = tmp_date - dt.timedelta(days=3)
        else:
            prev_date = tmp_date - dt.timedelta(days=1)
        try:
            i = str([i for i in self.filelist if i.find(str(prev_date).split(' ')[0]) != -1][0])
        except:
            i = self.filelist[0].split('.')[0].split('_')[1]
            print('No previous day record. \nStart with the first date: {}.'.format(str(i)))
        
        df_tmp = pd.read_excel(self.filelist[0], u'客户交易结算日报', header=None)
        try:
            df_Prev_Position= self.fetch_table(df_tmp, u'期货持仓汇总')
        except:
            df_Prev_Position = pd.DataFrame()
        
        return df_Prev_Position
    
    def df_Orders(self):
        '''
        This function is used to analyze Orders with its gain/loss, % win,
        and plot the open/close in candle-charts.
        Input:
            dataframe of orders from EODAnalysis.Trading_Orders 
                or Simulated Trading_Orders
            time_period = 'tick' or 'one minute'
        '''
        df_Orders = self.Trading_Orders(self.date_start, self.date_end)
        
        df_Orders['Timestamp'] = df_Orders.loc[:, u'实际成交日期'] + \
                                'T'+  df_Orders.loc[:, u'成交时间'] + \
                                '.000Z'
        df_Orders['Timestamp'] = df_Orders['Timestamp'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ'))
        
        # Change to minutes
        #df_Orders['Timestamp'] = df_Orders['Timestamp'].apply(lambda x:dt.datetime.strftime(x, "%Y-%m-%d %H:%M:00"))
        df_Orders.loc[:,u'买/卖']=df_Orders.loc[:,u'买/卖'].replace(u'买', 1)
        df_Orders.loc[:,u'买/卖']=df_Orders.loc[:,u'买/卖'].replace(u' 卖', -1)
        
        df_Orders.loc[:,u'开/平']=df_Orders.loc[:,u'开/平'].replace(u'开', 1)
        df_Orders.loc[:,u'开/平']=df_Orders.loc[:,u'开/平'].replace(u' 平', -1)
        
        return df_Orders
    
       
    def analysis(self, df_Contract):
        df_Position = self.df_Prev_Position().copy()
        if df_Position.size == 0:
            pass
        else: 
            df_Position = df_Position.drop(u'合计', axis=0)
        for i in list(set(df_Contract.index)):
            print(i)
            if i in list(set(self.df_Prev_Position().index)):
                print(df_Position.loc[i, :])
                df_Contract = df_Contract.groupby(['Timestamp', u'买/卖', u'开/平', u'成交价'])[u'手数'].sum().reset_index().set_index('Timestamp')
            else:                
                ### 买持仓 + 买开 - 卖平
                Long_Open = df_Contract.where((df_Contract.loc[:, u'买/卖']==1) & (df_Contract.loc[:, u'开/平'] == 1)).loc[:, u'手数'].sum()
                Short_Close = df_Contract.where((df_Contract.loc[:, u'买/卖']==-1) & (df_Contract.loc[:, u'开/平'] == -1)).loc[:, u'手数'].sum()
                
                ### 卖持仓 + 卖开 - 买平
                Short_Open = df_Contract.where((df_Contract.loc[:, u'买/卖']==-1) & (df_Contract.loc[:, u'开/平'] == 1)).loc[:, u'手数'].sum()
                Long_Close = df_Contract.where((df_Contract.loc[:, u'买/卖']==1) & (df_Contract.loc[:, u'开/平'] == -1)).loc[:, u'手数'].sum()
                
                print('买持仓：{}\n买开：{}\n卖平：{}'.format(np.NaN, Long_Open, Short_Close))
                print('卖持仓：{}\n卖开：{}\n买平：{}'.format(np.NaN, Short_Open, Long_Close))
                df_Contract = df_Contract.groupby(['Timestamp', u'买/卖', u'开/平', u'成交价'])[u'手数'].sum().reset_index().set_index('Timestamp')
        return df_Contract
    
    def get_contract_asset(self):
        '''
        Return all the underlying assets being traded without maturity month
        '''
        contract_orders = set(self.df_Orders().index)
        contract_asset_list = list(set([i.rstrip(self.number) for i in contract_orders]))
        return contract_asset_list
    
    def get_contract_asset_list(self):
        '''
        Return all the contracts lists with maturity month
        '''
        contract_orders = set(self.df_Orders().index)
        return contract_orders
    
    def backtest_trading(self, contract_asset, time_period='one minute'):
        '''
        This function is used to analyze the orders and trading results for one contract;
        
        Input:
            contract_asset: contract # e.g., i or I, rb or RB 
            
            
        Output:
            
        '''
        ####contract 提取交易手续费计算表格 历史行情数据对接等
        contract = []
        contract_asset = contract_asset.upper()
        contract_orders = self.get_contract_asset_list()
        contract_list = self.get_contract_asset()
        if not contract_asset in contract_list:
            print('{} contract is not traded. \
                  \nPlease re-enter the contract.'.format(contract_asset))
        else:
            for i in contract_orders:
                if i.rstrip(self.number) == contract_asset:
                    contract.append(str(i))
        print(contract)    
        for i in contract:
            df_tradings = self.analysis(self.df_Orders().loc[i,:])
            # 画图 连接数据库部分
            df_tradings = df_tradings.reset_index()
            df_tradings['Timestamp'] = df_tradings['Timestamp'].apply(lambda i: dt.datetime.strftime(i, "%Y-%m-%d %H:%M:00"))
            return df_tradings
        

if __name__ == '__main__':
    #filepath = r'C:\\Users\\Aian Fund\\Desktop\\王亚民'
    filepath = r'C:\\Users\\Aian Fund\\Desktop\\保证金监控中心'
    x = EOD_Analysis(filepath, u'九泰')
    x = Trading_Analysis(filepath, u'九泰', '2017-04-10', '2017-04-14')