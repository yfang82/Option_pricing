import numpy as np
from scipy.stats import norm
from scipy.integrate import quad
import math

class IterativePricing:
    def __init__(self, r, sigma, K, T, num_nodes):
        self.r = r
        self.sigma = sigma
        self.K = K
        self.T = T
        self.B0 = np.repeat(K, num_nodes)
        self.taos = np.linspace(0, T, num_nodes)
        self.num_nodes = num_nodes

    def d1(self, S, tao, B):
        return (np.log(S / B) + (self.r + 0.5 * self.sigma ** 2) * tao) / (self.sigma * np.sqrt(tao))

    def d2(self, S, tao, B):
        return self.d1(S, tao, B) - self.sigma * np.sqrt(tao)

    def European_put_value(self, S, tao):
        d1 = self.d1(S, tao, self.K)
        d2 = self.d2(S, tao, self.K)
        return self.K * np.exp(-self.r * tao) * norm.cdf(-d2) - S * norm.cdf(-d1)

    def polynomial_interpolation_B(self, t, B_current):
        x_points = self.taos
        y_points = B_current

        def divided_differences(x, y):
            n = len(y)
            coef = np.zeros([n, n])
            coef[:, 0] = y
            for j in range(1, n):
                for i in range(n - j):
                    coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (x[i + j] - x[i])
            return coef[0, :]

        coef = divided_differences(x_points, y_points)
        n = len(coef)
        polynomial = coef[0]
        for i in range(1, n):
            term = coef[i]
            for j in range(i):
                term *= (t - x_points[j])
            polynomial += term
        return polynomial

    def first_iteration(self):
        B1 = [self.K]
        for i in range(1, self.num_nodes):
            tao_i = self.taos[i]
            d1_val = self.d1(self.K, tao_i, self.K)
            d2_val = self.d2(self.K, tao_i, self.K)

            B = (self.K * np.sqrt(self.r) / (self.sigma * np.sqrt(2)) *
                 math.erf(np.sqrt(self.r * tao_i)) *
                 np.exp(-tao_i * (self.sigma ** 2 - 2 * self.r) ** 2 / (8 * self.sigma ** 2)))

            B += (1 / (self.sigma * np.sqrt(2 * np.pi * tao_i)) *
                  self.K * np.exp(-(self.r * tao_i + 0.5 * d2_val ** 2)))

            B /= (norm.cdf(d1_val) +
                  1 / (self.sigma * np.sqrt(2 * np.pi * tao_i)) *
                  np.exp(-0.5 * d1_val ** 2))
            
            B1.append(B)
        return np.array(B1)

    def single_iteration(self, B_current):
        B_next = [self.K]
        for i in range(1, self.num_nodes):
            tao_i = self.taos[i]
            def f_for_integral(t):
                d2_val = self.d2(B_current[i], tao_i-t, self.polynomial_interpolation_B(t, B_current))
                return (1 / (np.sqrt((tao_i - t))) *
                       np.exp(-self.r * (tao_i - t) - 0.5 * d2_val ** 2))

            integral_result = quad(f_for_integral, a=0, b=tao_i, epsabs=1e-9, epsrel=1e-9)[0]
            d1_val = self.d1(B_current[i], tao_i, self.K)
            d2_val = self.d2(B_current[i], tao_i, self.K)

            B = (self.r * self.K /(self.sigma*np.sqrt(2*np.pi)) * integral_result +
                 1 / (self.sigma * np.sqrt(2 * np.pi * tao_i)) *
                 self.K * np.exp(-(self.r * tao_i + 0.5 * d2_val ** 2)))

            B /= (norm.cdf(d1_val) +
                  1 / (self.sigma * np.sqrt(2 * np.pi * tao_i)) *
                  np.exp(-0.5 * d1_val ** 2))
         
            B_next.append(B)
        return np.array(B_next)
    
    def calc_put_value(self,S,B):
        ep = self.European_put_value(S,self.T)
        def f_for_integral(t):
            d2_val = self.d2(S, self.T-t, self.polynomial_interpolation_B(t, B))
            return np.exp(-self.r*(self.T-t))*norm.cdf(-d2_val)

        integral_result = quad(f_for_integral, a=0, b=self.T, epsabs=1e-9, epsrel=1e-9)[0]
        ap = ep+self.r*self.K*integral_result
        return ap
    
    

