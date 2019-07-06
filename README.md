# XGboost_Index-Enhancement-Strategy
A Index-Enhancement-Strategy based on XGboost, the code is written in Python, but the document is **written in Chinese**
<br/>
This is a final project from Tsinghua 2019 *Quantitative Investment Theory* , and here is our work.
<br/>
This project is more like to give you a structure and inspiration. We can't upload all the factors, thus, maybe you can change the data, and still use our structure.
<br/>
<br/>
**Data**
<br/>
I am sorry, due to copyright, I can only upload some part of the factors. These factors are really powerful, some part of them powered by tier-1 stock company in China, and some from Alpha 101, and some from GP learn's generation. 
<br/>
If you want to run the code, you only have to change the time of the backtest and the file path.
![image](https://github.com/Blabala/XGboost_Index-Enhancement-Strategy/blob/master/image/data.png)
<br/>
<br/>
**train_model_weekly.py**
<br/>
We use XGboost to do a binary classification problem. In the same industry, the top 30% labeled as 1, the last 30% labeled as 0. We will abandon the rest 40% in the training sets. The file save the XGboost model. Because it takes a lot of time, you can save the model and change the following parts when you do backtest.
<br/>
<br/>
**xgb_test_weekly.py**
<br/>
Upload XGboost model, and predict the prob. in testing sets. It will produce the decision for each stocks. (Output: a array stock*time)
<br/>
<br/>
**Final Project.py**
<br/>
Backtest based on a good backtesting platform: http://www.digquant.com.cn/research/community/270
This platform will show all the professional assessment of your strategy.
![image](https://github.com/Blabala/XGboost_Index-Enhancement-Strategy/blob/master/image/backtest1.png)
![image](https://github.com/Blabala/XGboost_Index-Enhancement-Strategy/blob/master/image/backtest2.png)
