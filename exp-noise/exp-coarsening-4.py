import os
import numpy as np

# cset = ['greedy_twohops', 'greedy_seed_twohops_group']
# rset = [0.5]
# mset = [1, 2, 3, 4, 5]
# d = 'network/'
# v = 3000
# v1 = str(v / 2)
# v2 = str(v / 2)
#
# for c in cset:
# 	for m in mset:
# 		for r in rset:
# 			for index, n in enumerate(np.arange(0.1, 1.0, 0.1)):
# 				f = 'dataset/' + str(index + 1) + '.ncol'
# 				n = "%.3f" % n
# 				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + '_' + n.replace('.', '')
# 				command = 'python ../../mob_exp/coarsening.py -f ' + f + ' -v ' + str(v1) + ' ' + str(v2) + ' -c ' + str(c) + ' -m ' + str(m) + ' -r ' + str(r) + ' -d ' + str(d) + ' -o ' + str(o) + ' --save_timing --save_source --save_ncol --save_conf'
# 				print command
# 				os.system(command)

cset = ['lpa_2']
rset = [0.5]
mset = [1, 2, 3, 4, 5]
itrset = [100, 300, 500]
d = 'network/'
v = 3000
v1 = str(v / 2)
v2 = str(v / 2)

for itr in itrset:
	for c in cset:
		for m in mset:
			for r in rset:
				for index, n in enumerate(np.arange(0.1, 1.0, 0.1)):
					f = 'dataset/' + str(index + 1) + '.ncol'
					n = "%.3f" % n
					o = c + '_' + str(itr) + '_' + str(v) + '_' + str(r).replace('.', '') + '_' + n.replace('.', '')
					command = 'python ../../mob_exp/coarsening.py -f ' + f + ' -v ' + str(v1) + ' ' + str(v2) + ' -i ' + str(itr) + ' -c ' + str(c) + ' -m ' + str(m) + ' -r ' + str(r) + ' -d ' + str(d) + ' -o ' + str(o) + ' --save_timing --save_source --save_ncol --save_conf'
					print command
					os.system(command)
