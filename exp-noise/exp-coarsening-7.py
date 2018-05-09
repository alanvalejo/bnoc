import os
import numpy as np

c = 'greedy_seed_twohops_group'
rset = [0.5]
mset = [1]
d = 'network/'
v = 1000
v1 = str(v / 2)
v2 = str(v / 2)

for m in mset:
	for r in rset:
		for index, n in enumerate(np.arange(0.1, 0.5, 0.01)):
			f = 'dataset/' + str(index + 1) + '.ncol'
			n = "%.3f" % n
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + '_' + n.replace('.', '')
			command = 'python ../../mob_exp/coarsening.py -f ' + f + ' -v ' + str(v1) + ' ' + str(v2) + ' -c ' + str(c) + ' -m ' + str(m) + ' -r ' + str(r) + ' -d ' + str(d) + ' -o ' + str(o) + ' --save_timing --save_source --save_ncol --save_conf'
			print command
			os.system(command)
