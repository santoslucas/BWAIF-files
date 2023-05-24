#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import yfinance as yf
import talib as ta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# In[24]:


def heuristicaEMM2(x0,x1,x2,x3,x4,x5,x6,x7,x8,x9, ticker, inicio_periodo, fim_periodo):
    # x e a variavel de controle
    # x[0]: preco: categorico {'open', 'close', 'low', 'high'}
    # x[1]: periodo da exponencial rápida int
    # x[2]: periodo da exponencial média int
    # x[3]: periodo da exponencial lenta int
    # x[4]: limiar de compra c1_2 float
    # x[5]: limiar de venda v1_2 float
    # x[6]: limiar de compra c1_3 float
    # x[7]: limiar de venda v1_3 float
    # x[8]: limiar de compra c2_3 float
    # x[9]: limiar de venda v2_3 float

    data = pd.read_csv('Csvs/' + ticker +'.csv')

    data = data.dropna()
    data = data.set_index('Date')
    #print(data)
    data = data.loc[inicio_periodo : fim_periodo]

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

    # x[1] < x[2] < x[3]
    tempo_curto = x1
    tempo_medio = x2
    tempo_longo = x3

    data['EMA_curta'] = ta.EMA(data['Price'], timeperiod=tempo_curto)
    ema_curta = data['EMA_curta'].to_numpy()
    data['EMA_media'] = ta.EMA(data['Price'], timeperiod=tempo_medio)
    ema_media = data['EMA_media'].to_numpy()
    data['EMA_longa'] = ta.EMA(data['Price'], timeperiod=tempo_longo)
    ema_longa = data['EMA_longa'].to_numpy()
    
    #print(data)

    delta_c1_2 = x4
    delta_v1_2 = x5
    delta_c1_3 = x6
    delta_v1_3 = x7
    delta_c2_3 = x8
    delta_v2_3 = x9
    vacumulado1_2 = 0
    vacumulado1_3 = 0
    vacumulado2_3 = 0

    comprado1_2 = False
    comprado1_3 = False
    comprado2_3 = False

    t_compra1_2 = []
    t_venda1_2 = []
    t_compra1_3 = []
    t_venda1_3 = []
    t_compra2_3 = []
    t_venda2_3 = []
    #falta configurar compra inicial

    datas = data.index
    
    for d in datas:
        #print(d.to_numpy())
        if data.loc[d]['EMA_curta'] > data.loc[d]['EMA_media'] + delta_c1_2 and not comprado1_2:
            #print('{} Compra 1_2: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_compra1_2.append(d)
            comprado1_2 = True
            vacumulado1_2 -= 100*data.loc[d]['Price']
        elif data.loc[d]['EMA_curta'] < data.loc[d]['EMA_media'] - delta_v1_2 and comprado1_2:
            #print('{} Venda 1_2: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_venda1_2.append(d)
            comprado1_2 = False
            vacumulado1_2 += 100*data.loc[d]['Price']  
            
        if data.loc[d]['EMA_curta'] > data.loc[d]['EMA_longa'] + delta_c1_3 and not comprado1_3:
            #print('{} Compra 1_3: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_compra1_3.append(d)
            comprado1_3 = True
            vacumulado1_3 -= 100*data.loc[d]['Price']
        elif data.loc[d]['EMA_curta'] < data.loc[d]['EMA_longa'] - delta_v1_3 and comprado1_3:
            #print('{} Venda 1_3: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_venda1_3.append(d)
            comprado1_3 = False
            vacumulado1_3 += 100*data.loc[d]['Price'] 
            
        if data.loc[d]['EMA_media'] > data.loc[d]['EMA_longa'] + delta_c2_3 and not comprado2_3:
            #print('{} Compra 2_3: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_compra2_3.append(d)
            comprado2_3 = True
            vacumulado2_3 -= 100*data.loc[d]['Price']
        elif data.loc[d]['EMA_media'] < data.loc[d]['EMA_longa'] - delta_v2_3 and comprado2_3:
            #print('{} Venda 2_3: R$ {:.2f}'.format(d, data.loc[d]['Price']))
            t_venda2_3.append(d)
            comprado2_3 = False
            vacumulado2_3 += 100*data.loc[d]['Price'] 
    
    if comprado1_2:
        #print('{} Venda Forçada: R$ {:.2f}'.format(datas[-1], data['Price'][-1]))
        vacumulado1_2 += 100*data['Price'][-1]
        comprado1_2 = False
    if comprado1_3:
        #print('{} Venda Forçada: R$ {:.2f}'.format(datas[-1], data['Price'][-1]))
        vacumulado1_3 += 100*data['Price'][-1]
        comprado1_3 = False
    if comprado2_3:
        #print('{} Venda Forçada: R$ {:.2f}'.format(datas[-1], data['Price'][-1]))
        vacumulado2_3 += 100*data['Price'][-1]
        comprado2_3 = False
    
    vacumulado = vacumulado1_2 + vacumulado1_3 + vacumulado2_3
    #print('Valor acumulado 1_2: R$ {:.2f}'.format(vacumulado1_2))
    #print('Valor acumulado 1_3: R$ {:.2f}'.format(vacumulado1_3))
    #print('Valor acumulado 2_3: R$ {:.2f}'.format(vacumulado2_3))
    #print('Valor acumulado total: R$ {:.2f}'.format(vacumulado))
    return -1*vacumulado


# In[25]:


#heuristica2treino('close', 3, 6, 9, 0.1, 0.1 , 0.1, 0.1, 0.1, 0.1, 'VALE3.SA', "2012-01-01", "2014-12-31")


# In[ ]:




