import numpy as np
import time
import matplotlib.pyplot as plt

t = []
for n in range(0, 1000):
	average = []
	for i in range(0, 10):
		start = time.time()
		np.random.negative_binomial(1, 0.1, n)
		average.append(time.time() - start)

	t.append(sum(average) / len(average))

plt.ylabel('runtime')
plt.xlabel('samples')
plt.plot(t)
plt.show()
