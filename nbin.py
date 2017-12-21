import numpy as np
import sys

dispersion, prob = float(sys.argv[1]), float(sys.argv[2])
# prob = ((mu + dispersion * mu ** 2) - mu) / (mu + dispersion * mu ** 2)
dist = np.random.negative_binomial(dispersion, 1 - prob, 1000)
print dist
print np.count_nonzero(dist)
print min(dist), '-', max(dist)
