import preprocessing
import bl
import numpy as np
import calc_weights
df_marketcap = preprocessing.market_cap_df()
df_ret = preprocessing.exreturn_adclose_df()
cov = np.array(preprocessing.get_cov_matrix(df_ret))
delta = preprocessing.get_delta(risk_free_rate=0.03)
market_implied_exreturn = bl.market_implied_exreturn(delta,df_marketcap,cov)
market_implied_return = bl.get_market_implied_return(market_implied_exreturn, risk_free_rate=0.03)
P, Q = bl.sample_prediction(seed = 10)
tau = 0.025
# omega = bl.get_default_omega(tau,P,np.array(cov))
omega = bl.get_user_omega([0.8,0.8,0.9,0.8,0.7,0.8,0.8,0.9],tau,P,cov)
print(omega)
bl_ret = bl.calculate_bl_returns(tau,cov,P,omega,market_implied_return,Q)
print(bl_ret)
optimal_weights, sharpe_rt = calc_weights.weights_max_sharpe(bl_ret,np.array(cov))
# 输出结果
print("Optimal Weights:", optimal_weights)
print("Maximum Sharpe Ratio:", sharpe_rt)

