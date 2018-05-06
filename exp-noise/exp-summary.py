import json
import numpy as np
import os

# c = 'rm'
# rset = [0.1, 0.2, 0.3, 0.4, 0.5]
# mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# d = 'result/'
# v = 10000
# v1 = str(v / 2)
# v2 = str(v / 2)
#
# with open('summary_' + c + '.csv', 'w+') as f:
# 	f.write('alg,m,r,v0,v,v1,v2,e,t\n')
# 	for index, n in enumerate(np.arange(0.001, 0.5, 0.005)):
#
# 		for r in rset:
# 			for m in mset:
# 				m = [m] * 2
# 				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
# 				config_file = d + o + '.conf'
# 				conf = json.load(open(config_file))
# 				timing_file = d + o + '.timing'
# 				timing = json.load(open(timing_file))
# 				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
# 				filename = d + o + '.ncol'
# 				filename = filename.replace('[', '\\[')
# 				filename = filename.replace(',', '\\,')
# 				filename = filename.replace(' ', '\\ ')
# 				filename = filename.replace(']', '\\]')
# 				print 'python ../../mob_exp/statistic.py -f ' + filename
# 				os.system('python ../../mob_exp/statistic.py -f ' + filename)
# 				line = [c, str(m), str(r), str(v), str(conf['vertices']), str(conf['v0']), str(conf['v1']), str(conf['edges']), str(timing)]
# 				f.write(','.join(line) + '\n')
# 		exit()

# c = 'greedy_twohops'
# rset = [0.1, 0.2, 0.3, 0.4, 0.5]
# mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# d = 'result/'
# v = 10000
# v1 = str(v / 2)
# v2 = str(v / 2)
#
# with open('summary_' + c + '.csv', 'w+') as f:
# 	f.write('alg,m,r,v0,v,v1,v2,e,t\n')
# 	for index, n in enumerate(np.arange(0.001, 0.5, 0.005)):
#
# 		for r in rset:
# 			for m in mset:
# 				m = [m] * 2
# 				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
# 				config_file = d + o + '.conf'
# 				conf = json.load(open(config_file))
# 				timing_file = d + o + '.timing'
# 				timing = json.load(open(timing_file))
# 				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
# 				filename = d + o + '.ncol'
# 				filename = filename.replace('[', '\\[')
# 				filename = filename.replace(',', '\\,')
# 				filename = filename.replace(' ', '\\ ')
# 				filename = filename.replace(']', '\\]')
# 				print 'python ../../mob_exp/statistic.py -f ' + filename
# 				os.system('python ../../mob_exp/statistic.py -f ' + filename)
# 				line = [c, str(m), str(r), str(v), str(conf['vertices']), str(conf['v0']), str(conf['v1']), str(conf['edges']), str(timing)]
# 				f.write(','.join(line) + '\n')
# 		exit()

c = 'greedy_seed_twohops'
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
d = 'result/'
v = 10000
v1 = str(v / 2)
v2 = str(v / 2)

with open('summary_' + c + '.csv', 'w+') as f:
	f.write('alg,m,r,v0,v,v1,v2,e,t\n')
	for index, n in enumerate(np.arange(0.001, 0.5, 0.005)):

		for r in rset:
			for m in mset:
				m = [m] * 2
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				config_file = d + o + '.conf'
				conf = json.load(open(config_file))
				timing_file = d + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				filename = d + o + '.ncol'
				filename = filename.replace('[', '\\[')
				filename = filename.replace(',', '\\,')
				filename = filename.replace(' ', '\\ ')
				filename = filename.replace(']', '\\]')
				print 'python ../../mob_exp/statistic.py -f ' + filename
				os.system('python ../../mob_exp/statistic.py -f ' + filename)
				line = [c, str(m), str(r), str(v), str(conf['vertices']), str(conf['v0']), str(conf['v1']), str(conf['edges']), str(timing)]
				f.write(','.join(line) + '\n')
		exit()

# c = 'greedy_seed_modularity_group'
# rset = [0.1, 0.2, 0.3, 0.4, 0.5]
# mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# d = 'result/'
# v = 10000
# v1 = str(v / 2)
# v2 = str(v / 2)
#
# with open('summary_' + c + '.csv', 'w+') as f:
# 	f.write('alg,m,r,v0,v,v1,v2,e,t\n')
# 	for index, n in enumerate(np.arange(0.001, 0.5, 0.005)):
#
# 		for r in rset:
# 			for m in mset:
# 				m = [m] * 2
# 				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
# 				config_file = d + o + '.conf'
# 				conf = json.load(open(config_file))
# 				timing_file = d + o + '.timing'
# 				timing = json.load(open(timing_file))
# 				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
# 				filename = d + o + '.ncol'
# 				filename = filename.replace('[', '\\[')
# 				filename = filename.replace(',', '\\,')
# 				filename = filename.replace(' ', '\\ ')
# 				filename = filename.replace(']', '\\]')
# 				print 'python ../../mob_exp/statistic.py -f ' + filename
# 				os.system('python ../../mob_exp/statistic.py -f ' + filename)
# 				line = [c, str(m), str(r), str(v), str(conf['vertices']), str(conf['v0']), str(conf['v1']), str(conf['edges']), str(timing)]
# 				f.write(','.join(line) + '\n')
# 		exit()
