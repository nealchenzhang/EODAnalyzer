# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 16:36:59 2017

@author: Aian Fund
"""

a = EOD_Analysis(os.getcwd())
df = a.fetch_table(tmp, '成交明细')
tmp
tmp.columns
tmp = pd.read_excel(os.listdir()[0], '成交明细', header=None)
tmp = pd.read_excel(os.listdir()[0], '客户交易结算月报', header=None)
df = a.fetch_table(tmp, '成交明细')
df = a.fetch_table(tmp, '期货成交汇总')
df.drop(axis=0, labels='合计', inplace=True)



for day in df.index.unique():
    tmp = df.loc[day].copy()


a1.drop(labels=['实际成交日期','成交序号','投机/套保'], axis=1, inplace=True)

a1=df.copy()
a1.reset_index(inplace=True)
a1.loc[:, '成交价'] = a1.loc[:,'成交价'].apply(np.float64)
a1.loc[:, '手数'] = a1.loc[:,'手数'].apply(np.float64)
a1.loc[:, '成交额'] = a1.loc[:,'成交额'].apply(np.float64)
a1.loc[:, '平仓盈亏'].replace('--', np.NaN, inplace=True)
a1.loc[:, '平仓盈亏'] = a1.loc[:,'平仓盈亏'].apply(np.float64)
col = list(a1.columns)
col[0] = '交易日期'
a1.columns = col
a1.loc[:, '交易日期'] = a1.loc[:,'交易日期'].apply(pd.to_datetime)
mm = a1.groupby(['合约', '交易日期','开/平','买/卖'])['成交额','手数', '平仓盈亏'].sum()
m = a1.groupby(['交易日期'])['手数', '平仓盈亏'].sum()
mm.sort_index(level='交易日期')
