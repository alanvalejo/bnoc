import os
import numpy as np

cset = ['greedy_seed_twohops']
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
d = 'result/'
v = 10000
v1 = str(v / 2)
v2 = str(v / 2)

for index, n in enumerate(np.arange(0.001, 0.5, 0.005)):
	f = 'dataset/' + str(index + 1) + '.ncol'
	for c in cset:
		for m in mset:
			for r in rset:
				o = c + '_' + str(v) + '_' + str(r).replace('.', '')
				print('python ../../mob/coarsening.py -f ' + f + ' -v ' + str(v1) + ' ' + str(v2) + ' -c ' + str(c) + ' -m ' + str(m) + ' -r ' + str(r) + ' -d ' + str(d) + ' -o ' + str(o) + ' --save_timing --save_source --save_ncol --save_conf')
				os.system('python ../../mob/coarsening.py -f ' + f + ' -v ' + str(v1) + ' ' + str(v2) + ' -c ' + str(c) + ' -m ' + str(m) + ' -r ' + str(r) + ' -d ' + str(d) + ' -o ' + str(o) + ' --save_timing --save_source --save_ncol --save_conf')
	exit()