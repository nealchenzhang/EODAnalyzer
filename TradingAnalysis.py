# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Created on Mon Jun 12 13:25:28 2017

# @author: nealcz @Aian_fund

# This program is personal trading platform desiged when employed in 
# Aihui Asset Management as a quantatitive analyst.
# 
# Contact: 
# Name: Chen Zhang (Neal)
# Mobile: (+86) 139-1706-0712
# E-mail: nealzc1991@gmail.com

###############################################################################
import numpy as np
import pandas as pd
import datetime as dt


from EODAnalysis import Tradings
from EODAnalysis import Positions

class Trading_Analysis(Tradings):
    
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
        
    def __init__(self, filepath):
        Tradings.__init__(self, filepath)
    
    def get_contract_asset(self):
        '''
        Return all the underlying assets being traded without maturity month
        '''
        contract_orders = set(self.Trading_Orders.index)
        contract_asset_list = list(set([i.rstrip(self.number) for i in contract_orders]))
        return contract_asset_list
    
    def get_contract_asset_list(self):
        '''
        Return all the contracts lists with maturity month
        '''
        contract_orders = list(set(self.Trading_Orders.index))
        return contract_orders
    
    def tradings(self, contract_asset):
        '''
        This function is used to analyze the orders and trading results for one contract;
        
        Input:
            contract_asset: contract # e.g., i or I, rb or RB 
            
        Output:
            df_tradings: normalized pandas dataframe of tradings for specific asset
            
        '''
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
        print(self.get_contract_asset_list())

        for i in contract:
            df_tradings = self.Trading_Orders.loc[i,:]
        ### 有些期货公司此处实际成交日期有误 待修改
        df_tradings['Timestamp'] = df_tradings.loc[:, '实际成交日期'] + \
                   'T'+  df_tradings.loc[:, '成交时间'] + '.000Z'
        df_tradings = df_tradings.reset_index()
        df_tradings.loc[:, 'Timestamp'] = (df_tradings.loc[:, 'Timestamp'].apply(pd.to_datetime)).values
        
        df_tradings.loc[:,u'买/卖'] = df_tradings.loc[:,u'买/卖'].replace(u'买', 1)
        df_tradings.loc[:,u'买/卖'] = df_tradings.loc[:,u'买/卖'].replace(u' 卖', -1)
        
        df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u'开', 1)
        df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u' 平', -1)

        return df_tradings
    
    def win_rate(self, df_tradings):
        df_tradings = df_tradings.sort_values(by='Timestamp')
        win_number = df_tradings.where((df_tradings.loc[:, '开/平']==-1) & (df_tradings.loc[:, '平仓盈亏']>0)).dropna(how='all').loc[:, '手数'].sum()
        close_number = df_tradings.where(df_tradings.loc[:, '开/平']==-1).dropna(how='all').loc[:, '手数'].sum()
        return win_number/close_number

if __name__ == '__main__':
    filepath = r'D:\\Neal\\EODAnalyzer\\保证金监控中心\\006580022168_2017-04-10.xls'
    x = Trading_Analysis(filepath)