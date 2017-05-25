# -*- coding: utf-8 -*-
"""
Created on Wed May 3 12:40:25 2017

@author: ChenZhang
"""
import pandas as pd
import numpy as np

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

def EOD(df_settlementfile, str_accountname, str_atp_accountname):
    """
    df_settlementfile: pandas读取后的账户日结算单文件
    str_accountname：string格式账户名
    str_atp_accountname: string格式ATP账户名
    
    return df_bal_file, df_open_pos_file
    
    """
    # Initialize bal_file and open_pos_file
    df_bal_file = pd.DataFrame(columns=['NUCPT','CODEV','MTNCB'])
    pos_columns = ['NUCPT','COMAR','CODEV','NUCON','QTACH','QTVEN','CNACT',
                   'CSOPT','CMECHE','CAECH','DAECA','MTSNA','MTULP','MCCAL',
                   'MVCAL']
    df_open_pos_file = pd.DataFrame(columns=pos_columns)
    
    # Data cleaning for balance
    a = df_settlementfile.copy()
    a = df_settlementfile.set_index([0])
    a = df_settlementfile.iloc[a.index.get_loc(r'上日结存'):]
    equity = a.iloc[0, 7]
    

    dict_bal_file = {'NUCPT': [str_atp_accountname],
                     'CODEV': ['CNY'],
                     'MTNCB': [float(equity)]
                    }
    df_bal_file = df_bal_file.append(pd.DataFrame(dict_bal_file,columns=['NUCPT','CODEV','MTNCB']))
    
    # Data cleaning for open_pos
    a = df_settlementfile.copy()
    a = df_settlementfile.set_index([0])
    try:
        a = df_settlementfile.iloc[a.index.get_loc(r'期货持仓汇总'):]
        a = a.set_index([0])
        a = a.iloc[:a.index.get_loc(r'合计')]
        a = a[1:]
        a.rename(columns=a.iloc[0,:], inplace=True)
        a.drop(r'合约', axis=0, inplace=True)

        for m in range(len(a.index)):
            CNACT = a.index[m].rstrip(number)
            Time = a.index[m][len(CNACT):]
            if Time[0] != '1':
                Time = '1' + Time            ###对合约号码第一二位进行处理
            dict_open_pos_file = {'NUCPT': [str_atp_accountname],       #ATP账号
                                'COMAR': [Contracts[CNACT]],      #交易所
                                'CODEV': ['CNY'],                 #币种
                                'NUCON': [np.NaN],                #成交ID
                                'QTACH': [int(np.nan_to_num(a.iloc[m][r'买持仓']))],  #买量
                                'QTVEN': [int(np.nan_to_num(a.iloc[m][r'卖持仓']))],  #卖量
                                'CNACT': [CNACT],                 #品种
                                'CSOPT': [np.NaN],                #期权
                                'CMECHE': [Time[-2:]],            #到期月份
                                'CAECH': ['20'+Time[:2]],         #到期年份
                                'DAECA': [np.NaN],                #到期日
                                'MTSNA': [np.NaN],                #期权
                                'MTULP': [np.nan_to_num((a.iloc[m][r'买持仓'] / a.iloc[m][r'买持仓']) * float(a.iloc[m][r'买均价']))+
                                            np.nan_to_num((a.iloc[m][r'卖持仓'] / a.iloc[m][r'卖持仓']) * float(a.iloc[m][r'卖均价']))],
                                'MCCAL': [float(a.iloc[m][r'今结算价'])], #结算价格（今结算价格）
                                'MVCAL': [float(a.iloc[m][r'浮动盈亏'])]  #持仓盈亏 
                                }
            df_open_pos_file = df_open_pos_file.append(pd.DataFrame(dict_open_pos_file, columns=pos_columns))
    except:
        dict_open_pos_file = pd.DataFrame(columns=pos_columns)
        df_open_pos_file = df_open_pos_file.append(pd.DataFrame(dict_open_pos_file, columns=pos_columns))
    df_open_pos_file = df_open_pos_file.append(pd.DataFrame(dict_open_pos_file, columns=pos_columns))

    return df_bal_file, df_open_pos_file