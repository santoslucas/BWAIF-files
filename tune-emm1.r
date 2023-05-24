library(reticulate)
use_virtualenv("r-reticulate")
library(stats)
library(doParallel)
library(irace)

setwd('C:/Users/rrcpf/Desktop/TCC')

# py_install("numpy")
# py_install("pandas")
# py_install("yfinance")
# py_install("TA-Lib")
# py_install("matplotlib")
np <- import("numpy")
pd <- import("pandas")
yf <- import("yfinance")
ta <- import("talib")
plt <- import("matplotlib.pyplot")
mdates <- import("matplotlib.dates")

source_python('EMM1Csv.py')

#configuracao para a sintonia de parametros
parametros.tabela <- '
x0 "" c (open,close,low,high)
x1 "" i (2, 5)
x2 "" i (6, 9)
x3 "" r (0.01, 0.15)
x4 "" r (0.01, 0.15)
'

acoes <- c(
  'VALE3.SA', 
  'PETR3.SA'
  ,'ITUB3.SA',
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
)

adhoc <- numeric(length(acoes))
tuned <- numeric(length(acoes))
i <- 1
dt_start='2012-01-01'
dt_end='2014-12-31'

#le tabela para o irace
parameters <- readParameters(text = parametros.tabela)

#funcao para avaliar cada candidato de configuracao em uma instancia
target.runner <- function(experiment, scenario) {
  instance <- experiment$instance
  # print(instances)
  configuration <- experiment$configuration
  
  # #funcao objetivo
  # fn <- function(x) {
  #   # print(x)
  #   # print(instances$evaluate(x))
  #   n = 2
  #   f <- instance(n_var = n)
  #   return (instance$evaluate(x))
  # }
  
  #executa a estrategia no periodo de treinamento
  
  obj <- heuristicaEMM1(
    as.array(configuration[['x0']]),
     as.integer(configuration[['x1']]),
     as.integer(configuration[['x2']]),
     as.double(configuration[['x3']]),
     as.double(configuration[['x4']]),
     ticker = instance,
     inicio_periodo = dt_start,
     fim_periodo = dt_end
     )
  
  print(obj)
  return (list(cost = obj))
}

for (acao in acoes) {

  #configuracao do cenario para treino
  scenario <- list(targetRunner = target.runner,
                   instances = acao,
                   maxExperiments = 5000
                   )
  
  #verifica se o cenario e valido
  checkIraceScenario(scenario = scenario, parameters = parameters)
  
  #executa o irace
  tuned.confs <- irace(scenario = scenario, parameters = parameters)
  
  #apresentar os melhores conjuntos de parametros para a funcao objetivo
  sink(file = paste("LogsEMM1/parametros-emm1-configs-", acao, ".txt"))
  configurations.print(tuned.confs)
  sink(file = NULL)
  #testa as configuracoes
  dt_start = '2015-01-01'
  dt_end = '2021-12-31'

  test <- function(configuration)
  {
    res <- target.runner(experiment = list(instance = acao, configuration = configuration),scenario = scenario)
    return (res)
  }

  # executa uma vez so para cada acao
  #print('Inicio do teste adhoc')
  adhoc[i] <- test(data.frame(x0='close', x1=3, x2=6, x3=0.1, x4=0.1, ticker = acao, inicio_periodo = dt_start, fim_periodo = dt_end))
  #print('Inicio do teste tuned')
  tuned[i] <- test (removeConfigurationsMetaData(tuned.confs[1,]))
  #print(dt_start)
  i <- i + 1
  #print('Fim do teste')
  dt_start='2012-01-01'
  dt_end='2014-12-31'
}

#Gerador de gráfico e sumário dos resultados

#pdf(file='param-EMM1.pdf', width=4, height=4)
#tunedvector <- unlist(tuned)
#adhocvector <- unlist(adhoc)
#tunedvector <- tunedvector*(-1)
#adhocvector <- adhocvector*(-1)
#boxplot(list(adhoc=adhocvector, tuned=tunedvector),
#        names=c('Manual', 'Sintonizado'),
#        ylab='Lucro/Prejuízo (R$)',
#        main='EMM1: Sintonia')
#dev.off()

#sink(file = "parametros-emm1.txt")

#wilcox.test(adhocvector, tunedvector, paired = TRUE, alternative = "two.sided")
#cat("Lucro/Prejuízo:\n")
#cat("Manual:\n")
#for(i in 1:length(acoes)){
#  cat(paste(acoes[i], " (" , toString(adhocvector[i]), "), "))
#}
#cat("\n")
#summary(adhocvector)
#cat("Sintonizado:\n")
#for(i in 1:length(acoes)){
#  cat(paste(acoes[i], " (" , toString(tunedvector[i]), "), "))
#}
#cat("\n")
#summary(tunedvector)
#sink(file = NULL)