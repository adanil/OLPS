#region imports
from AlgorithmImports import *
#endregion

class RPRT:

    def __init__(self, window=5, eps=50, theta=0.8):
        self.window = window
        self.eps = eps
        self.theta = theta
        self.phi = np.array([])

    def eval(self, x, last_b, history):
        if len(history)< 5:
            return last_b
        if len(history) == 5:
            self.phi = history.iloc[1,:] / history.iloc[0,:]
        x_pred = self.predict(history.iloc[-self.window :])
        D_pred = np.diag(np.array(x_pred))
        last_phi = self.phi
        last_price_relative = history.iloc[-1, :] / history.iloc[-2, :]
        gamma_pred = (self.theta * last_price_relative / (self.theta * last_price_relative + last_phi))
        phi_pred = gamma_pred + np.multiply(1 - gamma_pred, np.divide(last_phi, last_price_relative))
        self.phi = phi_pred
        b = self.update(b=last_b, phi_pred=phi_pred, D_pred=D_pred)
        return b

    def predict(self, hist):
        return hist.mean() / hist.iloc[-1, :]

    def update(self, b, phi_pred, D_pred):
        phi_pred_mean = np.mean(phi_pred)
        if np.linalg.norm(phi_pred - phi_pred_mean) ** 2 == 0:
            lam = 0
        else:
            lam = max(0.0, (self.eps - np.dot(b, phi_pred)) / np.linalg.norm(phi_pred - phi_pred_mean) ** 2)
        if lam != 0:
            b_ = b + lam * np.dot(D_pred, (phi_pred - phi_pred_mean))
        else:
            b_ = b
        b_ = np.clip(b_, -1e10, 1e10)
        return self.proj(y=b_)

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
