#region imports
from AlgorithmImports import *
#endregion


# Your New Python File

class PAMR:

    def eval(self, x, last_b, history):
        b = self.update(last_b, x, 0.5, 500)
        return b


    def update(self, b, x, eps, C):
        x_mean = np.mean(x)
        le = max(0.0, np.dot(b, x) - eps)
        lam = le / np.linalg.norm(x - x_mean) ** 2
        lam = min(100000, lam)
        b = b - lam * (x - x_mean)
        return b


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


