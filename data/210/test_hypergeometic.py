from scipy.stats import hypergeom
n = 13
N = 20287
K = 105
k = 12

prb = hypergeom.cdf(k, N, n, K)
print(prb)
