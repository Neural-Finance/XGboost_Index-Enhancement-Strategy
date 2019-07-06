#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import warnings
import scipy
warnings.filterwarnings('ignore')
import pickle
import os
import xgboost as xgb
import time

n_iter = 1

#i_year_params = pd.read_csv('i_year_params_regress.csv', header=None)
class Para():
    method = 'XGBR' 
    train_interval = 280
    data_index = None
    percent_select = [0.33, 0.33]  
    path_data = './data_weekly_new/'
    return_column = 'norm_return_20'
    modelPath = 'model_weekly/' + return_column + '/'
    fac_begin = 'EP'
    #fac_end = 'alpha110'
    fac_end = 'bias'
    day_test = None
    day_test_start = 3161#5145

para = Para()
factor_list = ['day','month','stock', 'status','norm_return_20', 'norm_return_10', 'norm_return_5']
fac_name = pd.read_csv('fac_name.csv',header = None)
for i in range(len(fac_name)):
    factor_list.append(fac_name.iloc[i][0])

def label_data1(data, para):
    data = data.sort_values(by=para.return_column, ascending=False)
    n_stock_select = np.multiply(para.percent_select, data.shape[0])
    n_stock_select = np.around(n_stock_select).astype(int)        
    data['return_bin'] = np.nan
    data.iloc[0:n_stock_select[0], -1] = 1
    data.iloc[-n_stock_select[1]:, -1] = 0
    data=data.dropna(axis=0)
    return data

def load_data_train(para, data_in_sample):
    train_end_day = para.data_index.index(para.day_test)
    day_train = para.data_index[train_end_day - para.train_interval:train_end_day]
    day_train = day_train[0::4]
    #day_train = day_train[:-1]
    print(day_train)
    print(para.day_test)

    if para.day_test == para.day_test_start:
        for i_day in day_train:        
            file_name = para.path_data + str(i_day) + '.mat'
            mat = scipy.io.loadmat(file_name)
            data_curr_day = pd.DataFrame(mat['Output'], columns = factor_list)
            data_curr_day.stock = data_curr_day.index
            data_curr_day = data_curr_day.dropna(axis=0)
            data_curr_day = label_data1(data_curr_day, para)           
            data_in_sample = data_in_sample.append(data_curr_day)
        return data_in_sample
    else:
        date_set = set(data_in_sample.day.unique().astype(int))
        day_train_set = set(day_train)
        
        for i_day in date_set-day_train_set:
            data_in_sample = data_in_sample[data_in_sample.day!=i_day]
        for i_day in day_train_set-date_set:
            file_name = para.path_data + str(i_day) + '.mat'
            mat = scipy.io.loadmat(file_name)
            data_curr_day = pd.DataFrame(mat['Output'], columns = factor_list)
            data_curr_day.stock = data_curr_day.index
            data_curr_day = data_curr_day.dropna(axis=0)
            data_curr_day = label_data1(data_curr_day, para)           
            data_in_sample = data_in_sample.append(data_curr_day)
        return data_in_sample


def get_train_day_list(para):
    import os
    data_index = []
    for day in os.listdir(para.path_data):
        day_num = int(day[:-4])
        data_index.append(day_num)
    
    print(len(data_index))
    return data_index

para.data_index = get_train_day_list(para)
day_test_list = para.data_index[para.data_index.index(para.day_test_start):]
print(len(para.data_index))
print(len(day_test_list))
time.sleep(10) 
#------------------------------------------------------------#
for i in range(0,n_iter):
    if not os.path.exists(para.modelPath + str(i) + '/'):
        os.mkdir(para.modelPath + str(i) + '/')
        
    para.colsample_bylevel = 0.1
    para.learning_rate = 0.1
    para.subsample = 0.8
    para.max_depth = 3

    data_in_sample = pd.DataFrame()
    for day_test in day_test_list:
        para.day_test = day_test
    
        data_in_sample = load_data_train(para, data_in_sample)
        
        
        X_in_sample = data_in_sample.loc[:, para.fac_begin:para.fac_end]
        y_in_sample = data_in_sample.loc[:, para.return_column]

        if para.method == 'XGBR':
            params = {'tree_mothod':'gpu_hist', 
                      'predictor':'gpu_predictor', 
                      #'n_gpus': -1,
                      'seed' : i,
                      'booster':'dart',
                      'learning_rate' : para.learning_rate,
                      'colsample_bylevel' : para.colsample_bylevel,
                      'subsample' :  para.subsample,
                      'max_depth' : para.max_depth
                      #'objective' : general_loss
                  }
                  
            model = xgb.XGBRegressor(**params)     
            model.fit(X_in_sample, y_in_sample)

        file = para.modelPath + str(i) + '/' + str(day_test) + ".sav"
        pickle.dump(model, open(file, 'wb'))
        print('Iter', i, ', Month', day_test, ',', 'Model saved')
        
