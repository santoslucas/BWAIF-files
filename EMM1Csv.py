#!/usr/bin/env python
# coding: utf-8




import numpy as np
import pandas as pd
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates





def heuristicaEMM1(x0,x1,x2,x3,x4, ticker, inicio_periodo, fim_periodo):
    # x0: preco: categorico {'open', 'close', 'low', 'high'}
    # x1: periodo da exponencial rápida int
    # x2: periodo da exponencial lenta int
    # x3: limiar de compra float
    # x4: limiar de venda float
    
    
    data = pd.read_csv('Csvs/' + ticker +'.csv')

    data = data.dropna()
    data = data.set_index('Date')
    #print(data)
    data = data.loc[inicio_periodo : fim_periodo]
    #print(data) 
    if x0 == 'open':
        data['Price'] = data['Open']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    elif x0 == 'high':
        data['Price'] = data['High']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    elif x0 == 'low':
        data['Price'] = data['Low']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)
    else:
        data['Price'] = data['Close']
        data = data.drop(['Open' ,'Close', 'Low','High', 'Adj Close', 'Volume'], axis=1)

    
    if(x1 > x2):
        tempo_curto = x2
        tempo_longo = x1
    else:
        tempo_curto = x1
        tempo_longo = x2
    
    
    data['EMA_curta'] = ta.EMA(data['Price'], timeperiod=tempo_curto)
    ema_curta = data['EMA_curta'].to_numpy()
    data['EMA_longa'] = ta.EMA(data['Price'], timeperiod=tempo_longo)
    ema_longa = data['EMA_longa'].to_numpy()
    
    #print(data)

    delta_c = x3
    delta_v = x4
    
    vacumulado = 0
    

    comprado = False

    t_compra = []
    t_venda = []
    
    
    datas = data.index
    
    for d in datas:
        #print(d.to_numpy())
        if data.loc[d]['EMA_curta'] > data.loc[d]['EMA_longa'] + delta_c and not comprado:
            #print('{} Compra: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_compra.append(d)
            comprado = True
            vacumulado -= 100*data.loc[d]['Price']
        elif data.loc[d]['EMA_curta'] < data.loc[d]['EMA_longa'] - delta_v and comprado:
            #print('{} Venda: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_venda.append(d)
            comprado = False
            vacumulado += 100*data.loc[d]['Price']

    if comprado:
        #print('{} Venda Forçada: R$ {:.2f}'.format(datas[-1], data['Price'][-1]))
        vacumulado += 100*data['Price'][-1]
        comprado = False
    
    #print('Valor acumulado: R$ {:.2f}'.format(vacumulado))
    return -1*vacumulado




