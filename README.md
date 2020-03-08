# XGboost_Index-Enhancement-Strategy
A Index-Enhancement-Strategy based on XGboost, the code is written in Python, but the document is **written in Chinese.** This is a final project from Tsinghua 2019 *Quantitative Investment Theory* . This project is more like to give you a framework and inspiration. We can't upload all the factors because some of them belong to a leading stock company and some of them come from outstanding hedge fund. Thus, maybe you can change the data, and still use our framework.

## Data
I am sorry, due to copyright, I can only upload some part of the factors. These factors are really powerful, some part of them powered by tier-1 stock company in China, and some from Alpha 101, and some from GP learn's generation. 
<br/>
If you want to run the code, you only have to change the time of the backtest and the file path.

![image](https://github.com/Neural-Finance/XGboost_Index-Enhancement-Strategy/blob/master/image/data.png)

## train_model_weekly
We use XGboost to do a binary classification problem. The file save the XGboost model. Because it takes a lot of time, you can save the model and change the following parts when you do backtest. **Actually, there are a lot of important settings, including data clean, normalization and labelization, It's very very important!**. For further information you can read a sell-side equity report (written in Chinese), or you can read patiently about my code, or you can have a brief look at my descrption as following. 

1.

2.

3.In the same trading day, and in the same industry, the top 30% samples labeled as 1, the last 30% labeled as 0. We will abandon the rest 40% in the training sets. But you should do nothing with the testing set!!! Otherwise you have used some information from the future.


## xgb_test_weekly
Upload XGboost model, and predict the prob. in testing sets. It will produce the decision for each stocks. (Output: a array stock*time)

## Final Project
Backtest based on a good backtesting platform: http://www.digquant.com.cn/research/community/270
This platform will show all the professional assessment of your strategy.
![image](https://github.com/Neural-Finance/XGboost_Index-Enhancement-Strategy/blob/master/image/backtest1.png)
![image](https://github.com/Neural-Finance/XGboost_Index-Enhancement-Strategy/blob/master/image/backtest2.png)

**If you like it, please give me a star, thanks.**
