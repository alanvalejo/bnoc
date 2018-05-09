import os

cset = ['lpa']
rset = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
itrset = [50, 500]
d = 'network/'

if not os.path.exists(d):
	os.makedirs(d)

for itr in itrset:
	for index, v in enumerate(range(1000, 101000, 1000)):
		v1 = (v / 2)
		v2 = (v / 2)
		f = 'dataset/' + str(index + 1) + '.ncol'
		for c in cset:
			for m in mset:
				for r in rset:
					o = c + '_' + str(itr) + '_' + str(v) + '_' + str(r).replace('.', '')
					command = 'python ../../mob_exp/coarsening.py -f ' + f + ' -v ' + str(v1) + ' ' + str(v2) + ' -i ' + str(itr) + ' -c ' + str(c) + ' -m ' + str(m) + ' -r ' + str(r) + ' -d ' + str(d) + ' -o ' + str(o) + ' --save_timing --save_source --save_ncol --save_conf'
					print(command)
					os.system(command)
