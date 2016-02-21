"""
Problem 2:
"""
import numpy as np

errors = np.random.randn(1000)
X = np.random.normal(loc=30, scale=100, size=1000)
Y = 275 + 41*X**2 + -3*np.sin(X) + errors

D = np.vstack([np.ones(len(X)), X**2, np.sin(X)]).T

data = np.vstack([X,Y]).T

print 275 + 41 + -3

np.savetxt("problem_2.txt", data, fmt='%s', delimiter=',')

print np.linalg.lstsq(D, Y)
