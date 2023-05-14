#region imports
from AlgorithmImports import *
from olmar import *
#endregion

class RMR(OLMAR):

    def __init__(self):
        self.window=5
        self.eps=10.0
        self.tau=0.001
        super().__init__()

    def norm(self, x):
        if isinstance(x, pd.Series):
            axis = 0
        else:
            axis = 1
        return np.sqrt((x ** 2).sum(axis=axis))

    def predict(self, x, history):
        y = history.mean()
        y_last = None
        while y_last is None or np.sqrt(self.norm(y - y_last)) / np.sqrt(self.norm(y_last))> self.tau:
            y_last = y
            d = np.sqrt(self.norm(history - y))
            y = history.div(d, axis=0).sum() / (1.0 / d).sum()
        return y / x
