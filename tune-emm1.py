from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer, Choice, Binary
from pymoo.core.mixed import MixedVariableMating, MixedVariableGA, MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.core.mixed import MixedVariableGA
from pymoo.optimize import minimize

import numpy as np

from EMM1Csv import *

class avalia_parametros_emm1(ElementwiseProblem):
    def __init__(self, ticker: str, dt_start: str, dt_end: str, **kwargs):
        self.ticker = ticker
        self.dt_start = dt_start
        self.dt_end = dt_end
        vars = {
            'x0': Choice(options=["open","close","low","high"]),
            'x1': Integer(bounds=[2, 5]),
            'x2': Integer(bounds=[6, 9]),
            'x3': Real(bounds=[0.01, 0.15]),
            'x4': Real(bounds=[0.01, 0.15])
        }
        super().__init__(vars=vars, n_obj=1, **kwargs)

    def _evaluate(self, X, out, *args, **kwargs):
        #parametros da EMM1 a ser sintonizada
        x0 = X['x0']
        x1 = X['x1']
        x2 = X['x2']
        x3 = X['x3']
        x4 = X['x4']

        #print(X)

        #executa EMM1
        res = heuristicaEMM1(
            x0, x1, x2, x3, x4,
            ticker=self.ticker,
            inicio_periodo=self.dt_start,
            fim_periodo=self.dt_end)

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
    problem = avalia_parametros_emm1(ticker, dt_start, dt_end)

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
    res = heuristicaEMM1(
            params[i]['x0'], 
            params[i]['x1'], 
            params[i]['x2'], 
            params[i]['x3'], 
            params[i]['x4'],
            ticker=tickers[i],
            inicio_periodo=dt_start,
            fim_periodo=dt_end)
    
    f.append(-res)
    print(res)
    
np.savetxt('objvls-emm1-ga-tuned.txt', f)