#region imports
from AlgorithmImports import *
#endregion

class BestSoFar:

    def init_weights(self, columns):
        m = len(columns)
        return np.ones(m) / m

    def eval(self, x, last_b, history):
        hist = history.iloc[-self.n :] if self.n else history
        p = hist.prod()
        p += 1e-10 * np.random.randn(len(p))
        return (p == p.max()).astype(float)
