# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Final Project
   Author :        朱天磊、方颉
   date：          2019/06/24
-------------------------------------------------

"""


from atrader import *
import numpy as np
import pandas as pd
import sys


# %%
def init(context):
    set_backtest(initial_cash=1e6)
    reg_kdata('week', 1)
    context.levels = 2  #针对29个一级行业，对每个行业分context.levels层


def on_data(context):
    asset = positions = context.account().cash['total_asset'].values
    #指数成分
    index = get_code_list('hs300')[['code','weight']].values
    data = get_reg_kdata(reg_idx=context.reg_kdata[0], length=2, fill_up=True, df=True)
    if data['close'].isna().any():
        return
    time = data['time'][0].strftime('%Y-%m-%d')[:10] #当前时间


    factors = pd.read_csv('factors.csv')[['NO','SIZE','INDUSTRY',time]].values    #因子值
    idx = [(i in index[:,0]) for i in factors[:,0]]
    factors = factors[idx,:]
    #按照行业、市值排序
    idx = np.lexsort([factors[:,1],factors[:,2]])
    factors = factors[idx, :]
    #目标仓位
    target = np.zeros(index.shape[0])

    for i in range(29): #行业数
        factors_industry = factors[factors[:,2]==i,:]
        nlevel = int(np.ceil(factors_industry.shape[0]/context.levels))
        for j in range(context.levels): #分层数
            factors_level = factors_industry[j*nlevel : (j+1)*nlevel,:]
            if factors_level.shape[0] >0:
                #选中股票权重为该层所有权重和
                weight = 0
                for k in factors_level[:,0]:
                    weight += index[index[:,0]==k,1]
                target[index[:, 0] == factors_level[np.argmin(factors_level[:, 3]), 0]] = weight

    #计算个股资金份额
    target *= asset[0]
    #根据份额调仓
    for i in range(len(target)):
        order_target_value(account_idx=0, target_idx=i, target_value=target[i], side=1,order_type=2, price=0)

if __name__ == '__main__':
    run_backtest(strategy_name='Final Project', file_path='Final Project.py', target_list=get_code_list('hs300')['code'],
                 frequency='week', fre_num=1, begin_date='2018-03-31', end_date='2019-03-31', fq=1)


