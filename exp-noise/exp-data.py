import os
import numpy as np

d = str(0.4)
m = str(0.4)
v = 3000
v1 = str(v / 2)
v2 = str(v / 2)
c = str(30)

dir = 'dataset'

if not os.path.exists(dir):
	os.makedirs(dir)

for index, n in enumerate(np.arange(0.1, 1.0, 0.1)):
	o = str(index + 1)
	n = "%.3f" % n
	command = ['python ../bnoc.py -v ', v1, ' ', v2, ' -d ', d, ' -m ', m, ' -c ', c, ' -b -n ', str(n), ' -dir ' + dir + ' -o ', o]
	command = ''.join(command)
	print command
	os.system(command)


	# output2.zip
	# d = str(0.4)
	# m = str(0.4)
	# v = 3000
	# v1 = str(v / 2)
	# v2 = str(v / 2)
	# c = str(30)
