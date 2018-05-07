import os
import numpy as np

d = str(0.2)
m = str(0.8)
v = 1000
v1 = str(v / 2)
v2 = str(v / 2)
c = str(10)

for index, n in enumerate(np.arange(0.001, 0.5, 0.01)):
	o = str(index + 1)
	n = "%.2f" % n
	print 'python ../bnoc.py -v ' + v1 + ' ' + v2 + ' -d ' + d + ' -m ' + m + ' -c ' + c + ' -b -n ' + str(n) + ' -dir dataset -o ' + o
	os.system('python ../bnoc.py -v ' + v1 + ' ' + v2 + ' -d ' + d + ' -m ' + m + ' -c ' + c + ' -b -n ' + str(n) + ' -dir dataset -o ' + o)
