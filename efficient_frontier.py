import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 函数：计算投资组合回报率
def portfolio_return(weights, returns):
    return np.dot(weights, returns)

# 函数：计算投资组合波动率
def portfolio_volatility(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

# 函数：计算有效前沿
def efficient_frontier(returns, cov_matrix, num_points = 100):
    results = np.zeros((3, num_points))
    weights_record = []
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(len(returns)))
    initial_guess = len(returns) * [1. / len(returns)]
    for i in range(num_points):
        target_return = np.linspace(returns.min(), returns.max(), num_points)[i]
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: portfolio_return(x, returns) - target_return}
        )
        result = minimize(portfolio_volatility, initial_guess, args=(cov_matrix,),
                          method='SLSQP', bounds=bounds, constraints=constraints)
        
        results[0, i] = portfolio_volatility(result.x, cov_matrix)
        results[1, i] = target_return
        results[2, i] = (target_return - 0) / results[0, i]  # 假设无风险利率为0
        weights_record.append(result.x)
    
    return results, weights_record

def plot_efficient_frontier(returns, cov):

    results, weights = efficient_frontier(returns,cov)

    # 绘制有效前沿
    plt.figure(figsize=(10, 6))
    plt.plot(results[0, :], results[1, :], 'b--', linewidth=2)
    plt.title('Efficient Frontier')
    plt.xlabel('Volatility (Standard Deviation)')
    plt.ylabel('Expected Return')
    plt.show()
