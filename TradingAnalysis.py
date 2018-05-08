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
import os


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
        
    def __init__(self, filepath, basis='daily', futures_broker=None):
        Tradings.__init__(self, filepath)
        self.basis = basis
        self.futures_broker = futures_broker
    
    def get_contract_asset(self):
        '''
        Return all the underlying assets being traded without maturity month
        '''
        if self.basis == 'daily':
            contract_orders = set(self.Trading_Orders.index)
        else:
            contract_orders = set(self.Trading_Orders.loc[:,'合约'])
        contract_asset_list = list(set([i.rstrip(self.number) for i in contract_orders]))
        return contract_asset_list
    
    def get_contract_asset_list(self):
        '''
        Return all the contracts lists with maturity month
        '''
        if self.basis == 'daily':
            contract_orders = list(set(self.Trading_Orders.index))
        else:
            contract_orders = list(set(self.Trading_Orders.loc[:,'合约']))
        
        return contract_orders
    
    def date_adjust(self, timestp):
        if timestp.hour >= 20:
            if timestp.isoweekday() == 1:
                return (timestp - dt.timedelta(days=3))
            else:
                return (timestp - dt.timedelta(days=1))
        else:
            return timestp   
    
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
        df_tradings = pd.DataFrame()
        if not contract_asset in contract_list:
            pass
#            print('{} contract is not traded. \
#                  \nPlease re-enter the contract.'.format(contract_asset))
        else:
            for i in contract_orders:
                if i.rstrip(self.number) == contract_asset:
                    contract.append(str(i))
#            print(contract)
#            print(self.get_contract_asset_list())
                
            for i in contract:
                Trading_Orders = self.Trading_Orders.copy()
                if self.basis == 'daily':
                    tmp = Trading_Orders.loc[i,:]
                else:
                    Trading_Orders.set_index('合约', inplace=True)
                    Trading_Orders.index.name = '合约'
                    tmp = Trading_Orders.loc[i,:]
                if type(tmp) == pd.Series:
                    df_tradings = df_tradings.append(pd.DataFrame(tmp).T)
                else:
                    df_tradings = df_tradings.append(tmp)

            df_tradings['Timestamp'] = df_tradings.loc[:, '实际成交日期'] + \
                       'T'+  df_tradings.loc[:, '成交时间'] + '.000Z'
            df_tradings = df_tradings.reset_index()
            df_tradings.loc[:, 'Timestamp'] = (df_tradings.loc[:, 'Timestamp'].apply(pd.to_datetime)).values
            ### 可增加期货公司list
            if self.futures_broker in ['华鑫', '国投', '国海', '东证']:
                 df_tradings.loc[:, 'Timestamp'] =  df_tradings.loc[:, 'Timestamp'].apply(self.date_adjust)
            else: pass
            try:
                    
                df_tradings.loc[:,u'买/卖'] = df_tradings.loc[:,u'买/卖'].replace(u'买', 1)
                df_tradings.loc[:,u'买/卖'] = df_tradings.loc[:,u'买/卖'].replace(u' 卖', -1)
                df_tradings.loc[:,u'买/卖'] = df_tradings.loc[:,u'买/卖'].replace(u'卖', -1)
                
                df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u'开', 1)
                df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u' 平', -1)
                df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u'开仓', 1)
                df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u'平仓', -1)
                df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u'平昨', -1)
                df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u'平今', -1)
                pass
            except:
                df_tradings.loc[:,u'买/卖'] = df_tradings.loc[:,u'买/卖'].replace(u'买', 1)
                df_tradings.loc[:,u'买/卖'] = df_tradings.loc[:,u'买/卖'].replace(u' 卖', -1)
                
                df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u'开', 1)
                df_tradings.loc[:,u'开/平'] = df_tradings.loc[:,u'开/平'].replace(u' 平', -1)
                
        return df_tradings
    
    def win_rate(self, df_tradings):
        df_tradings = df_tradings.sort_values(by='Timestamp')
    
        if 'index' in df_tradings.columns:
            df_tradings.drop('index', axis=1, inplace=True)
        else:
            pass
        df_tradings.reset_index(inplace=True, drop=True)
        win_number = df_tradings.loc[:, '手数'].where((df_tradings.loc[:, '开/平']==-1) & (df_tradings.loc[:, '平仓盈亏']>0)).dropna(how='all').sum()
        close_number = df_tradings.loc[:, '手数'].where(df_tradings.loc[:, '开/平']==-1).dropna(how='all').sum()
        if close_number == 0:
            return '未平仓'
        else:
            return win_number/close_number

if __name__ == '__main__':
#    filepath = r'D:\\Neal\\EODAnalyzer\\保证金监控中心\\011927800042_2017-07-31.xls'
#    x = Trading_Analysis(filepath)
#    folderpath = 'C:\\Users\\Aian Fund\\Desktop\\远澜保证金监控中心\\保证金监控中心'
   
    def fortnight(advisor, folderpath):
        filelist = os.listdir(folderpath)
        trading_asset = []
        if advisor == '益菁汇':
            broker = '东证'
        else:
            broker = None
        
        for i in filelist:
            a = Trading_Analysis(folderpath+'\\'+i, futures_broker=broker)
            trading_asset.extend(a.get_contract_asset())

        for i in list(set(trading_asset)):
            trading = pd.DataFrame()
            for j in filelist:
                tmp = pd.DataFrame()
                a = Trading_Analysis(folderpath+'\\'+j, futures_broker=broker)
                tmp = a.tradings(i)
                trading = trading.append(tmp)
            trading.to_excel(folderpath.split('结算单')[0]+'/结算单/'+advisor+'/'+'{}.xlsx'.format(i))
            print(i, trading['平仓盈亏'].sum(), a.win_rate(trading), trading['手数'].sum())
    
    def monthly(advisor, folderpath, basis='monthly'):
        if advisor == 'RB':
            broker = '大地'
        else:
            broker = None
        filelist = os.listdir(folderpath)
        trading_asset = []
        for i in filelist:
            a = Trading_Analysis(folderpath+'\\'+i, basis, futures_broker=broker)
            trading_asset.extend(a.get_contract_asset())

        for i in list(set(trading_asset)):
            trading = pd.DataFrame()
            for j in filelist:
                tmp = pd.DataFrame()
                a = Trading_Analysis(folderpath+'\\'+j, basis, futures_broker=broker)
                tmp = a.tradings(i)
                trading = trading.append(tmp)
            trading.to_excel(folderpath.split('结算单')[0]+'/结算单/'+advisor+'/'+'{}.xlsx'.format(i))
            print(i, trading['平仓盈亏'].sum(), a.win_rate(trading), trading['手数'].sum())
        
    
#    Advisors = ['爱凡哲', '泰然2号', '登隐2号', '泰然1号', '新朴', '蓝天9号濡伸', '祥泽6号鲁证', '祥泽6号东证',
#                '祥泰1号爱凡哲', '祥寅2号熠道', '双犀']
#    Advisors = ['祥寅1号', '方宜', '和正', '康腾', '橡杉', '稳健2号张福健004', '稳健2号张福健006']
#    Advisors = ['登隐2号', '泰然1号', '新朴','祥泽6号']

    Advisors = ['祥寅1号', '祥泽6号鲁证', '祥泽6号东证', '祥泰1号康腾银河','祥泰1号康腾鲁证',
                '泰然6号橡杉', '泰然6号双犀', '泰然5号熠道', '泰然2号', '泰然1号', '蓝天9号濡伸', '和正']
    Advisors = ['爱晖佳实']
    Advisors = ['祥泽6号鲁证', '祥泽6号东证','泰然6号橡杉', '泰然6号双犀',
                '泰然5号熠道', '泰然2号', '泰然1号', '蓝天9号濡伸', '和正',
                '爱晖佳实']
    for i in Advisors:
        print(i)
#        folderpath = 'C:/Users/Aian Fund/Desktop/结算单/'+ str(i)+'/保证金监控中心'
        folderpath = 'C:/Users/Aian Fund/Desktop/结算单/'+ str(i)+'/保证金监控中心'
#        folderpath = 'C:/Users/Aian Fund/Desktop/'+ str(i)+'/保证金监控中心'
        os.chdir(folderpath)
        os.listdir(folderpath)
        fortnight(i, folderpath)
#        monthly(i, folderpath)
    
    
    
