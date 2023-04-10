from AlgorithmImports import *
import numpy as np

class UniversalPortfolio(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  # Set Start Date
        self.SetEndDate(2023,1,1)
        self.SetCash(1_000_000)  # Set Strategy Cash

        self.MichaelBurrySymbols = ["BKI","GEO","WWW","BABA","COHR","MGM","JD","SKYW","QRTEA"]

        self.WarrenBuffetSymbols = ["AAPL","BAC","CVX","KO","AXP","KHC","OXY","MCO","TSM",
        "ATVI","HPQ","DVA","BK","USB","VRSN","VIAC","C","KR","V","GM","MA","AON","CHTR","FWONA",
        "MCK","AMZN","CE","SNOW","TMUS"]

        self.HowardMarksSymbols = ["TRMD","CHK","VST","SBLK","STR","RWAY","EGLE","WFRD","STKL",
        "INFN","ALLY","VALE","PCG","ITUB","AU","NMIH","FYBR","HTZ","FCX","CBL","IBN","PBR","KRC",
        "ALVO","CX","BAP","BRY","VIST","BBD","LBTYA","FTAI","OCSL","AZUL","BATL","TOL","VVR",
        "PHM","GTX","VAL","PAM","CVT"]

        self.RussianMarketSymbols = ["IRAO","GAZP","SNGS","SNGSP","SBER","VTBR","ALRS","RUAL","MOEX",
        "NLMK","TATN","MTSS","ROSN","NVTK","LKOH","POLY","CHMF","VKCO","FIVE","YNDX","TCSG",
        "PHOR","MGNT","OZON","GMKN","PLZL",]

        self.equities = {"MB" : self.MichaelBurrySymbols,
                        "WB" : self.WarrenBuffetSymbols,
                        "HM" : self.HowardMarksSymbols,
                        "RM" : self.RussianMarketSymbols}
        
        self.eqName = "RM"

        self.nEquites = len(self.equities[self.eqName])

        self.weights = np.empty(self.nEquites)
        self.weights.fill(1/self.nEquites)
        self.weightEPS = 0.005

        self.S = np.ones(self.nEquites)

        self.EqPrices = np.zeros(self.nEquites)

        for eq in self.equities[self.eqName]:
            self.AddEquity(eq, Resolution.Daily)


    def OnData(self, data: Slice):
        if not self.Portfolio.Invested:
            for i,eq in enumerate(self.equities[self.eqName]):
                self.SetHoldings(eq, self.weights[i])
                self.EqPrices[i] = self.Portfolio[eq].Price
                self.Log(str(i) + " : " + eq)
            return

        self.Log("New day")

        x = np.zeros(self.nEquites)
        for i, symbol in enumerate(self.equities[self.eqName]):
            x[i] = self.Portfolio[symbol].Price / self.EqPrices[i]
            self.EqPrices[i] = self.Portfolio[symbol].Price

        self.Log("S: " + str(self.S))
        self.Log("Price: " + str(self.EqPrices))
        self.Log("x: " + str(x))
        self.Log("Weights: " + str(self.weights))

        self.S = np.multiply(self.S, self.weights * x.T)
        b = self.weights.T * self.S
        targetWeights = b / sum(b)

        self.Log("Target weights: " + str(targetWeights))
        # self.weights = targetWeights


        for i, symbol in enumerate(self.equities[self.eqName]):
            w = (self.Portfolio[symbol].Quantity * self.Portfolio[symbol].Price) /self.Portfolio.TotalPortfolioValue
            s = "Weight of " + symbol + " : " + str(w)
            self.Log(s)

            diffW = w - targetWeights[i]
            if self.Portfolio[symbol].Price < 0.00005:
                continue
            if diffW > self.weightEPS:
                sellQuantity = self.Portfolio.TotalPortfolioValue * diffW//self.Portfolio[symbol].Price
                self.MarketOrder(symbol, -sellQuantity)
                self.Log("Sell " + str(sellQuantity) + " of " + symbol)
            
            elif diffW < -self.weightEPS:
                buyQuantity = self.Portfolio.TotalPortfolioValue * -diffW//self.Portfolio[symbol].Price
                self.MarketOrder(symbol, buyQuantity)
                self.Log("Buy " + str(buyQuantity) + " of " + symbol)
            
            self.weights[i] = (self.Portfolio[symbol].Quantity * self.Portfolio[symbol].Price) /self.Portfolio.TotalPortfolioValue

