#region imports
from AlgorithmImports import *
#endregion


class OLMAR:

    def __init__(self):
        self.window = 10
        self.eps = 10
        self.alpha = 0.2


    def eval(self, x, last_b, history):
        if len(history) < self.window + 1:
            x_pred = history.iloc[-1]
        else:
            h = history.iloc[-self.window :]
            x_pred = self.predict(x, h)
        b = self.update(last_b, x_pred, self.eps)
        return b


    def predict(self, x, hist):
        return hist.mean() / hist.iloc[-1, :]


    def update(self, b, x_pred, eps):
        x_pred_mean = np.mean(x_pred)
        excess_return = x_pred - x_pred_mean
        denominator = (excess_return * excess_return).sum()
        if denominator != 0:
            lam = max(0.0, (eps - np.dot(b, x_pred)) / denominator)
        else:
            lam = 0

        b = b + lam * (excess_return)

        return self.proj(b)


    def proj(self, y):
        m = len(y)
        bget = False
        s = sorted(y, reverse=True)
        tmpsum = 0.0
        for ii in range(m - 1):
            tmpsum = tmpsum + s[ii]
            tmax = (tmpsum - 1) / (ii + 1)
            if tmax >= s[ii + 1]:
                bget = True
                break
        if not bget:
            tmax = (tmpsum + s[m - 1] - 1) / m
        return np.maximum(y - tmax, 0.0)
