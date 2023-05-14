#region imports
from AlgorithmImports import *
import scipy.stats
from numpy import diag, log, sqrt, trace
from numpy.linalg import inv 
#endregion


class CWMR:

    def eval(self, x, last_b, history):
        confidence=0.95
        self.theta = scipy.stats.norm.ppf(confidence)
        m = history.shape[1]
        self.sigma = np.matrix(np.eye(m) / m ** 2)
        m = len(x)
        mu = np.matrix(last_b).T
        sigma = self.sigma
        theta = self.theta
        eps = -0.95 
        x = np.matrix(x).T 
        M = mu.T * x
        V = x.T * sigma * x
        x_upper = sum(diag(sigma) * x) / trace(sigma)
        mu, sigma = self.update(x, x_upper, mu, sigma, M, V, theta, eps)
        mu = self.proj(mu)
        sigma = sigma / (m ** 2 * trace(sigma))
        self.sigma = sigma
        return mu

    def update(self, x, x_upper, mu, sigma, M, V, theta, eps):
        foo = (
            V - x_upper * x.T * np.sum(sigma, axis=1)
        ) / M ** 2 + V * theta ** 2 / 2.0
        a = foo ** 2 - V ** 2 * theta ** 4 / 4
        b = 2 * (eps - log(M)) * foo
        c = (eps - log(M)) ** 2 - V * theta ** 2
        a, b, c = a[0, 0], b[0, 0], c[0, 0]
        lam = max(0, (-b + sqrt(b ** 2 - 4 * a * c)) / (2.0 * a), (-b - sqrt(b ** 2 - 4 * a * c)) / (2.0 * a))
        lam = min(lam, 1e7)
        U_sqroot = 0.5 * (-lam * theta * V + sqrt(lam ** 2 * theta ** 2 * V ** 2 + 4 * V))
        mu = mu - lam * sigma * (x - x_upper) / M
        sigma = inv(inv(sigma) + theta * lam / U_sqroot * diag(x) ** 2)
        return mu, sigma

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
