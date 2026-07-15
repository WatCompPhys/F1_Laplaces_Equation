import numpy as np

N = 10
ansatz = np.zeros((N+1)*(N+1))

tolerance = 0.0001

# Boundary Conditions
T = 100
B = 100
L = 100
R = 100

# Top
m = 0
while m <= N:
    ansatz[m] = T
    m += 1


# Bottom
m = 0
while m <= N:
    ansatz[N*(N+1)+m] = B
    m += 1


# Left
n = 0
while n <= N:
    ansatz[n*(N+1)] = L
    n += 1


# Right
n = 0
while n <= N:
    ansatz[n*(N+1)+N] = R
    n += 1

x=np.linspace(N,N,128)
def T_0(X):
    return x