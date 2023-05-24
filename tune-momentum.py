from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer, Choice, Binary
from pymoo.core.mixed import MixedVariableMating, MixedVariableGA, MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.core.mixed import MixedVariableGA
from pymoo.optimize import minimize

import numpy as np

from Momentum import *

class avalia_parametros_momentum(ElementwiseProblem):
    def __init__(self, symbol: str, dt_start: str, dt_end: str, **kwargs):
        self.symbol = symbol
        self.dt_start = dt_start
        self.dt_end = dt_end
        vars = {
            'price': Choice(options=['open','close','low','high']),
            'period': Integer(bounds=[3, 9]),
            'ma': Choice(options=['SMA', 'EMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA']),
            'thresholdupper': Real(bounds=[0, 0.05]),
            'thresholdlower': Real(bounds=[0, 0.05])
        }
        super().__init__(vars=vars, n_obj=1, **kwargs)

    def _evaluate(self, X, out, *args, **kwargs):
        #parametros da Revsersao a ser sintonizada
        price = X['price']
        period = X['period']
        ma = X['ma']
        thresholdupper = X['thresholdupper']
        thresholdlower = X['thresholdlower']

        #print(X)

        #executa Reversao
        res = heuristicaMomentum(
            price, 
            period, 
            ma, 
            thresholdupper, 
            thresholdlower,
            symbol=self.symbol,
            start=self.dt_start,
            end=self.dt_end)

        out['F'] = res

# main

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

# parameters configuration
dt_start='2012-01-01'
dt_end='2014-12-31'

params=[]
for ticker in tickers:
    problem = avalia_parametros_momentum(ticker, dt_start, dt_end)

    algorithm = MixedVariableGA(
        pop_size=20, 
        sampling=MixedVariableSampling(),
        mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination()),
        eliminate_duplicates=MixedVariableDuplicateElimination())
        
    res = minimize(problem,
                algorithm,
                termination=('n_evals', 5000),
                #    seed=1,
                verbose=False)

    params.append(res.X)
    print(res.X)
    
# tickers evaluation
print('-----------------------------------------')
dt_start = '2015-01-01'
dt_end = '2021-12-31'

f = []
for i in range(40):
    res = heuristicaMomentum(
            params[i]['price'], 
            params[i]['period'], 
            params[i]['ma'], 
            params[i]['thresholdupper'], 
            params[i]['thresholdlower'],
            symbol=tickers[i],
            start=dt_start,
            end=dt_end)
    
    f.append(-res)
    print(res)
    
np.savetxt('objvls-momentum-ga-tuned.txt', f)