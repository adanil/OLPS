#region imports
from AlgorithmImports import *
from pamr import PAMR
#endregion


class WMAMR(PAMR):

    def __init__(self, window=5):
        self.window = window

    def eval(self, x, last_b, history):
        xx = history[-self.window :].mean()
        b = self.update(last_b, xx, self.eps, self.C)
        return b
