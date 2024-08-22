import numpy as np

def binomial_option_pricing(T,sigma,r,N,K,S):
    # Binomial Tree method
    N = 1000  # number of periods or number of time steps. Same as the paper

    deltaT = T/N  # Delta t
    u = np.exp(sigma * np.sqrt(deltaT))  # up factor
    d = np.exp(-sigma * np.sqrt(deltaT))

    p = (np.exp(r*deltaT) - d) / (u - d)  # risk neutral up probability
    q = 1 - p  # risk neutral down probability

    V = np.zeros(N + 1)  # vector to store values at each time step
    # Use binomial theorem to get all terminal nodes on the tree
    S_T = np.array([(S * u**j * d **(N - j)) for j in range(N + 1)]) 

    V[:] = np.maximum(K - S_T, 0)

    for i in range(N-1,-1,-1):
        # N time intervals in total, so calculate recursively N times
        # the value vector is updated at each time step. Only the first i+1 value is valid after each update. 
        V[:-1] = np.exp(-r*deltaT)*(p * V[1:] + q * V[:-1])
        
        S_T = S_T * u  # calculate the price at the previous time step by backward 'going up' tree branches by one time step. Each time one value at the end will be invalid, but we can disregard that.

        V = np.maximum(V, K - S_T)

    return V[0]
