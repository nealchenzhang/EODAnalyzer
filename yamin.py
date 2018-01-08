# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:52:27 2017

@author: Aian Fund
"""
import pandas as pd
import os

Advisors = ['泰然1号']
for i in Advisors:
    print(i)
    folderpath = 'C:/Users/Aian Fund/Desktop/结算单/'+ str(i)+'/保证金监控中心'
    os.chdir(folderpath)
    os.listdir(folderpath)
    df_trading = pd.read_excel(folderpath.split('结算单')[0]+'/结算单/'+i+'/'+'I.xlsx')
    