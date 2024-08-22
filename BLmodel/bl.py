import numpy as np
def market_implied_exreturn(delta, market_cap, cov_matrix):
    mc_sum = market_cap['market_cap'].sum()
    market_cap_weight = market_cap['market_cap']/mc_sum
    market_cap_weight = np.array(market_cap_weight)
    cov_matrix = np.array(cov_matrix)
    return delta*cov_matrix @ market_cap_weight

def get_market_implied_return(market_implied_exreturn,risk_free_rate=0.03):
    return market_implied_exreturn+risk_free_rate

def sample_prediction(n = 8, seed = 100):
    np.random.seed(seed)
    # suppose the stocks in our portfolio is in Q1 quantile (long)
    random_array = np.random.normal(0,0.002,8)
    Q = random_array
    P = np.identity(n)
    return P, Q

def get_default_omega(tau, P, cov_matrix):
    return np.diag(np.diag(tau * P @ cov_matrix @ P.T))

def get_user_omega(confidence_array,tau,P, cov_matrix, n=8):
    '''
    confidence_array: element must be between 0 and 1
    '''
    view_omegas = []
    for view_idx in range(n):
        conf = confidence_array[view_idx]

        if conf == 0:
            view_omegas.append(1e6)
            continue

        P_view = P[view_idx].reshape(1, -1)
        alpha = (1 - conf) / conf
        omega = tau * alpha * P_view @ cov_matrix @ P_view.T
        view_omegas.append(omega[0,0])
    return np.diag(view_omegas)
    
def calculate_bl_returns(tau,Sigma,P,Omega,Pi,Q):
    
    tau = np.array(tau)
    Sigma = np.array(Sigma)
    P = np.array(P)
    Omega = np.array(Omega)
    Pi = np.array(Pi)
    Q = np.array(Q)
    
    tau_Sigma_inv = np.linalg.inv(tau * Sigma)
    P_Omega_inv_P_inv = np.linalg.inv(P.T @ np.linalg.inv(Omega) @ P)
    P_Omega_inv_Q = P.T @ np.linalg.inv(Omega) @ Q
    
    expected_return = np.linalg.inv(tau_Sigma_inv + P_Omega_inv_P_inv) @ (tau_Sigma_inv @ Pi + P_Omega_inv_Q)
    
    return expected_return