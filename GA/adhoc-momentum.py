import numpy as np

from Momentum import *

tickers=[
  'VALE3.SA', 
  'PETR3.SA',
  'ITUB3.SA',
  'BBDC3.SA',
  'B3SA3.SA',
  'ELET3.SA',
  'ABEV3.SA',
  'RENT3.SA',
  'BBAS3.SA',
  'WEGE3.SA',
  'ITSA3.SA',
  'SUZB3.SA',
  'EQTL3.SA',
  'GGBR3.SA',
  'JBSS3.SA',
  'LREN3.SA',
  'RADL3.SA',
  'PRIO3.SA',
  'ENEV3.SA',
  'HYPE3.SA',
  'CSAN3.SA',
  'SBSP3.SA',
  'VIVT3.SA',
  'TOTS3.SA',
  'CMIG3.SA',
  'BRFS3.SA',
  'KLBN3.SA',
  'UGPA3.SA',
  'CCRO3.SA',
  'MGLU3.SA',
  'ENGI3.SA',
  'SANB3.SA',
  'AMER3.SA',
  'CPLE3.SA',
  'EGIE3.SA',
  'TIMS3.SA',
  'BRKM3.SA',
  'EMBR3.SA',
  'TAEE3.SA',
  'CSNA3.SA'
]
 
# tickers evaluation
dt_start = '2015-01-01'
dt_end = '2021-12-31'

f = []
for i in range(40):
    res = heuristicaMomentum('close', 5, 'SMA', 0.01, 0.01, tickers[i], dt_start, dt_end)
    f.append(-res)
    
np.savetxt('objvls-momentum-adhoc.txt', f)