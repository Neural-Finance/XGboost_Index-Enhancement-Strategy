# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 10:27:45 2018

@author: Wz
"""

# generate x,y

import pandas as pd
import numpy as np
import scipy.io
import glob
import pickle
import xgboost as xgb
import matplotlib.pyplot as plt
from scipy import stats
import scipy as sp


class Para(object):
    def __init__(self):
        self.path_data = './data_weekly_new/'           
        self.return_column = 'norm_return_20'
        self.seed = None
        self.model_path = None#'model/' + self.return_column + '/' + str(self.seed) + '/'
        self.fac_path = None#'result/' + self.return_column + '/fac_' + str(self.seed) + '.csv'
        self.date_path = None#'result/' + self.return_column + '/trade_date_' + str(self.seed) + '.csv'
        self.offset = None
        self.fac_begin = 'EP'
        self.fac_end = 'alpha110'
        self.num_stock = 3700
        self.day_test_start = 3161
      
#get factor_list
factor_list = ['day','month','stock', 'status','norm_return_20', 'norm_return_10', 'norm_return_5']
fac_name = pd.read_csv('fac_name.csv',header = None)
for i in range(len(fac_name)):
    factor_list.append(fac_name.iloc[i][0])
    
def get_train_day_list(para):
    import os
    data_index = []
    for day in os.listdir(para.path_data):
        day_num = int(day[:-4])
        data_index.append(day_num)
    return data_index
    
def load_data2(para, day_test):
    data_in_sample = pd.DataFrame()
    
    file_name = para.path_data + str(day_test) + '.mat'
    mat = scipy.io.loadmat(file_name)
    data_in_sample = pd.DataFrame(mat['Output'], columns = factor_list)

    return data_in_sample
    
def predict(para, day_test, model):
    dfTestRaw = load_data2(para, day_test)
    dfTestRaw.stock = dfTestRaw.index           
    dfTestX = dfTestRaw.loc[:,para.fac_begin:para.fac_end]
    dfTestX = dfTestX.dropna(axis=0)
    arPredictedCScore = model.predict(dfTestX) 

    fac_1.loc[dfTestX.index,day_test_list.index(day_test)] =  arPredictedCScore
    return 
    
    
def rankIC(para,fac_1):
    ic_list = []
    for k in day_test_list: 
        #print(k)
        fac = fac_1.iloc[:,day_test_list.index(k)]
        #fac = fac.dropna()        
        file_name = para.path_data + str(k) + '.mat'
        mat = scipy.io.loadmat(file_name)
        data_df = pd.DataFrame(mat['Output'], columns = factor_list)#index = stock_list, 
        #data_df['stock'] = data_df.index        
        #data_df = data_df.dropna()
        true_return =  data_df.loc[:,'norm_return_20']
        #数据合并
        pred_true = pd.concat([fac, true_return], axis=1)
        pred_true = pred_true.dropna()
   # fac data_df index需要一致     
        ic_list.append(stats.spearmanr(pred_true.iloc[:,0], pred_true.iloc[:,1])[0] )
    result_df = pd.DataFrame()
    result_df['IC'] = ic_list
    result_df.plot()
    plt.show()
    IC = np.mean(result_df)
    IR = np.mean(result_df)/np.std(result_df)
    print(IC)
    print(IR)
    return IC,IR


for k in range(0,1):
    para = Para()
    para.seed = k
    para.model_path = 'model_weekly/' + para.return_column + '/' + str(para.seed) + '/'
    para.fac_path = 'result_weekly/' + para.return_column + '/fac_' + str(1) + '.csv'
    para.date_path = 'result_weekly/' + para.return_column + '/trade_date_' + str(1) + '.csv'
    
    
    data_index = get_train_day_list(para)
    para.offset = data_index.index(para.day_test_start)
    day_test_list = data_index[para.offset:] 
    #fac_1 = pd.DataFrame(index = range(0,para.num_stock), columns=range(day_test_list[-1]))
    fac_1 = pd.DataFrame(index = range(para.num_stock), columns=range(len(day_test_list)))
    
    for j in day_test_list:
        name = para.model_path + '%s' %j +'.sav'
        model = pickle.load(open(name, 'rb'))
        predict(para, j, model)
        print(str(j) + ' day OK')
        del model
    
    IC,IR =rankIC(para,fac_1)  
    date_mat_file = 'dailyinfo_dates.mat'
    date_mat_type = 'dailyinfo_dates'
    date_mat = sp.io.loadmat(date_mat_file)[date_mat_type]
    date_mat = np.append(date_mat, 737593)
    trade_date_df = pd.DataFrame(np.nan * np.zeros((2,len(day_test_list))))
    
    j = 0
    for i in day_test_list:
        trade_date_df.iloc[0,j] = date_mat[i-1]
        trade_date_df.iloc[1,j] = date_mat[i]
        j+=1
      
    fac_1.to_csv(para.fac_path, header=False,index=False)
    trade_date_df.to_csv(para.date_path,header=False,index=False)