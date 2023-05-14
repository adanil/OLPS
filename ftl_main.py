from AlgorithmImports import *
import numpy as np
import pandas as pd
from olmar import OLMAR
from pamr import PAMR
from cmwr import CWMR
from rmr import RMR
from rprt import RPRT
from exponential import EXP
from bsf import BestSoFar
from unp import UP
from cpr import CRP
from wmamr import WMAMR
import equities

class ExponentialGradient(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1) 
        self.SetEndDate(2023,4,1)
        self.SetCash(1_000_000) 

        self.parallelPortfolios = []

        self.equities = {
            "MB" : equities.MichaelBurrySymbols,
            "WB" : equities.WarrenBuffetSymbols,
            "HM" : equities.HowardMarksSymbols,
        }
        
        self.activeEquitySet = "HM"

        self.nEquites = len(self.equities[self.activeEquitySet])

        self.weights = np.empty(self.nEquites)
        self.weights.fill(1/self.nEquites)
        self.weightEPS = 0.005

        self.S = np.ones(self.nEquites)

        self.EqPrices = np.zeros(self.nEquites)

        self.history = pd.DataFrame([])
        self.olmar = OLMAR()
        self.pamr = PAMR() 
        self.cwmr = CWMR() 
        self.rmr = RMR() 
        self.rprt = RPRT() 
        self.bsf = BestSoFar() 
        self.wmamr = WMAMR()

        for eq in self.equities[self.activeEquitySet]:
            self.AddEquity(eq, Resolution.Daily)

    def OnData(self, data: Slice):
        if not self.Portfolio.Invested:
            for i,eq in enumerate(self.equities[self.activeEquitySet]):
                self.SetHoldings(eq, self.weights[i])
                self.EqPrices[i] = self.Portfolio[eq].Price
                self.Log(str(i) + " : " + eq)
            return

        self.Log("New day")
        try:
            x = np.zeros(self.nEquites)
            for i, symbol in enumerate(self.equities[self.activeEquitySet]):
                x[i] = self.Portfolio[symbol].Price / self.EqPrices[i]
                self.EqPrices[i] = self.Portfolio[symbol].Price

            self.history = pd.concat([self.history, pd.DataFrame(x).T], axis=0)
            self.Log("Price: " + str(self.EqPrices))
            self.Log("x: " + str(x))
            self.Log("Weights: " + str(self.weights))

            targetWeights = self.wmamr.beval(x, self.weights, self.history)

            self.Log("Target weights: " + str(targetWeights))


            for i, symbol in enumerate(self.equities[self.activeEquitySet]):
                if not data.ContainsKey(symbol):
                    continue
                w = (self.Portfolio[symbol].Quantity * self.Portfolio[symbol].Price) /self.Portfolio.TotalPortfolioValue
                s = "Weight of " + symbol + " : " + str(w)
                self.Log(s)
                
                diffW = w - targetWeights[i]
                if diffW > self.weightEPS:
                    sellQuantity = self.Portfolio.TotalPortfolioValue * diffW//self.Portfolio[symbol].Price
                    self.Log("Sell " + str(sellQuantity) + " of " + symbol)
                    self.MarketOrder(symbol, -sellQuantity)
                
                elif diffW < -self.weightEPS:
                    buyQuantity = self.Portfolio.TotalPortfolioValue * -diffW//self.Portfolio[symbol].Price
                    self.Log("Buy " + str(buyQuantity) + " of " + symbol)
                    self.MarketOrder(symbol, buyQuantity)
                   
                self.weights[i] = (self.Portfolio[symbol].Quantity * self.Portfolio[symbol].Price) /self.Portfolio.TotalPortfolioValue
        except:
            self.Log("ERROR")
