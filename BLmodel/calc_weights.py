import numpy as np
import pandas as pd
from scipy.optimize import minimize

def negative_sharpe_ratio(weights, mu, Sigma, risk_free_rate=0.03):
    portfolio_return = np.dot(weights, mu)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(Sigma, weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std
    return -sharpe_ratio

def weights_max_sharpe(expected_ret, Sigma):
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(len(expected_ret)))
    initial_guess = len(expected_ret) * [1. / len(expected_ret)]

    result = minimize(negative_sharpe_ratio, initial_guess, args=(expected_ret, Sigma), method='SLSQP', bounds=bounds, constraints=constraints)

    # 最优权重
    optimal_weights = result.x

    return optimal_weights, -result.fun
