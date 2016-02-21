"""
Problem 1:
"""
import numpy as np


mu = 1311
sigma = 23
n = 10000

data = np.random.normal(loc=mu, scale=sigma, size=n)

np.savetxt("problem_1.txt", data, fmt='%s')

print np.mean(data)/np.sqrt(np.var(data))

