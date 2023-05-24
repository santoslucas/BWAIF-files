#!/usr/bin/env python
# coding: utf-8

#ECVA de Momentum baseada na implemetação encontrada em:
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH

import numpy as np
import pandas as pd
import talib as ta


def heuristicaMomentum( price, period, ma, thresholdupper, thresholdlower,symbol, start, end):
    #Retrieves and prepares the data.
    data = pd.read_csv('Csvs/' +  symbol +'.csv')

    data = data.dropna()
    data = data.set_index('Date')
    #print(data)
    data = data.loc[ start :  end]

    if  price == 'open':
        data['Price'] = data['Open']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    elif  price == 'high':
        data['Price'] = data['High']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    elif  price == 'low':
        data['Price'] = data['Low']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    else:
        data['Price'] = data['Close']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    data['return'] = np.log(data / data.shift(1))
    # Backtests the trading strategy.
    if  ma == 'KAMA':
        #data['position'] = np.sign(ta.SMA(data['return'],timeperiod =  period))
        data['ma'] = ta.KAMA(data['return'],timeperiod =  period)      
    elif  ma == 'EMA':
        #data['position'] = np.sign(ta.EMA(data['return'],timeperiod =  period))
        data['ma'] = ta.EMA(data['return'],timeperiod =  period)
    elif  ma == 'DEMA':
        #data['position'] = np.sign(ta.DEMA(data['return'],timeperiod =  period))
        data['ma'] = ta.DEMA(data['return'],timeperiod =  period)
    elif  ma == 'TEMA':
        #data['position'] = np.sign(ta.TEMA(data['return'],timeperiod =  period))
        data['ma'] = ta.TEMA(data['return'],timeperiod =  period)
    elif  ma == 'TRIMA':
        #data['position'] = np.sign(ta.TRIMA(data['return'],timeperiod =  period))
        data['ma'] = ta.TRIMA(data['return'],timeperiod =  period)
    else:
        #data['position'] = np.sign(ta.KAMA(data['return'],timeperiod =  period))
        data['ma'] = ta.SMA(data['return'],timeperiod =  period)
    #print(price,period,ma, thresholdupper, thresholdlower, symbol, start, end)
    #Criação dos sinais
    #Venda - Desempenho abaixo do limiar
    data['position'] = np.where(data['return'] <  -thresholdlower, -1,  np.nan)
    
    data['position'] = np.where(data['return'] > -thresholdlower, 0, data['position'])
    #Compra - Desempenho acima do limiar
    data['position'] = np.where(data['return'] >  thresholdupper , 1, data['position'])
   
    data['strategy'] = data['position'].shift(1) * data['return']
    # determine when a trade takes place
    data.dropna(inplace=True)
    trades = data['position'].diff().fillna(0) != 0
    data['creturns'] =  10000 * data['return'].cumsum().apply(np.exp)
    data['cstrategy'] =  10000 * \
        data['strategy'].cumsum().apply(np.exp)
    results = data
    # absolute performance of the strategy
    aperf =  results['cstrategy'].iloc[-1]
    # out-/underperformance of strategy
    operf = aperf -  results['creturns'].iloc[-1]
    
    return -round(operf, 2)


