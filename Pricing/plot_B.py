import numpy as np
import matplotlib.pyplot as plt

def plot_B(hist_B):
    '''
    Input: 
    hist_B: a list of numpy arrays
    '''

    plt.figure(figsize=(10, 6))
    for i in range(len(hist_B)):
        plt.plot(hist_B[i],label = f'Iteration {i}')
    plt.xlabel('Time to maturity (tao)')
    plt.ylabel('Exercise Boundary B_tao')
    plt.legend()
    plt.title('Exercise Boundary over Iterations')
    plt.show()
