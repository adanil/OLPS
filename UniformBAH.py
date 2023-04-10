# region imports
from AlgorithmImports import *
# endregion

class UniformBAH(QCAlgorithm):

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
        
        self.baseWeight = 1/self.nEquites

        for eq in self.equities[self.eqName]:
            self.AddEquity(eq, Resolution.Daily)

    def OnData(self, data: Slice):
        if not self.Portfolio.Invested:
            for eq in self.equities[self.eqName]:
                self.SetHoldings(eq, self.baseWeight)