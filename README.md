# Reproducing and Comparing American Option Pricing Models

In this project, I analyze and reproduce the iterative method purposed in the paper A Simple Iterative Method for the Valuation of American Options. <br>

The method was derived from the Black-Scholes model and Little et al. (2000)’s idea of representing the value of American option (put) with European option of the same underlying asset and a single integral involving the exercise boundary. By estimating the Exercise Boundary using iterative numerical method, the option value can be easily calculated. <br> 

After reproducing the iterative method, I compare it with the commonly used Binomial Tree method for option pricing. Then, I used the AAPL put option real-world example to examine the effectiveness of the two option pricing methods.<br>  

In [pricing.ipynb](https://github.com/yfang82/Option_pricing/blob/main/Pricing/pricing.ipynb), I analyzed the method, demonstrated the method setup and used class I wrote to implement the iterative method and calculate the put option price. <br> 

pyfiles:<br> 
[IterativePricing.py](https://github.com/yfang82/Option_pricing/blob/main/Pricing/IterativePricing.py): set up iterative method, calculate exercise boundary, calculate put price at tau = T. <br> 
[plot_B.py](https://github.com/yfang82/Option_pricing/blob/main/Pricing/plot_B.py): plot iterations in calculating exercise boundary B and show the convergence of the method. <br> 
[Binomial.py](https://github.com/yfang82/Option_pricing/blob/main/Pricing/Binomial.py): implement binomial tree method as shown in the ipynb file. <br> 

Reference:<br> 
In Joon Kim, et al. “A Simple Iterative Method for the Valuation of American Options.” Quantitative Finance, vol. 13, no. 6, 1 June 2013, pp. 885–895, https://doi.org/10.1080/14697688.2012.696780.<br> 
“Pricing an American Option: 3 Period Binomial Tree Model.” Www.youtube.com, www.youtube.com/watch?v=35n7TICJbLc. Accessed 13 Jan. 2023.<br> 
