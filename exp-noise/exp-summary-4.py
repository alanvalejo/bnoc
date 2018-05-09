import json
import numpy as np
import subprocess
import os

cset = ['greedy_twohops', 'greedy_seed_twohops_group']
rset = [0.5]
mset = [1, 2, 3, 4, 5]
d = 'network/'
v = 3000
v1 = str(v / 2)
v2 = str(v / 2)
ddata = 'dataset/'
dnet = 'network/'
dout = 'output/'

if not os.path.exists(ddata):
	os.makedirs(ddata)

if not os.path.exists(dnet):
	os.makedirs(dnet)

if not os.path.exists(dout):
	os.makedirs(dout)

for c in cset:
	for m in mset:
		m = [m] * 2
		for r in rset:
			summary = dout + 'summary_' + str(v) + '_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
			with open(summary, 'w+') as f:
				f.write('n,v,nmi,avg,mod,nmi\n')
				for index, n in enumerate(np.arange(0.1, 1.0, 0.1)):
					n = "%.3f" % n

					o = c + '_' + str(v) + '_' + str(r).replace('.', '') + '_' + n.replace('.', '')

					levels = str(m)
					config_file = dnet + o + levels + '.conf'
					conf = json.load(open(config_file))

					timing_file = dnet + o + str(m) + '.timing'
					timing = json.load(open(timing_file))
					timing_coarsening = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])

					levels = levels.replace('[', '\\[').replace(',', '\\,').replace(' ', '\\ ').replace(']', '\\]')
					filename = dnet + o + levels + '.ncol'
					command = 'python ../../mob_exp/statistic.py -f ' + filename
					proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
					(out, err) = proc.communicate()
					out = out.rstrip().split(' ')
					line = [n, str(conf['vertices']), out[0], out[1]]

					coarsest_file = dnet + o + levels + '.ncol'
					command = 'python ../../mob_exp/lpa.py -f ' + coarsest_file + ' -c'
					print command
					proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
					(out, err) = proc.communicate()
					out = out.strip().split(' ')
					line.append(out[1])
					line.append(out[2])

					f.write(','.join(line) + '\n')
					f.flush()

cset = ['lpa_2']
rset = [0.5]
mset = [1, 2, 3, 4, 5]
itrset = [100, 300, 500]
d = 'network/'
v = 3000
v1 = str(v / 2)
v2 = str(v / 2)
ddata = 'dataset/'
dnet = 'network/'
dout = 'output/'

if not os.path.exists(ddata):
	os.makedirs(ddata)

if not os.path.exists(dnet):
	os.makedirs(dnet)

if not os.path.exists(dout):
	os.makedirs(dout)

for itr in itrset:
	for c in cset:
		for m in mset:
			m = [m] * 2
			for r in rset:
				summary = dout + 'summary_' + str(v) + '_' + c + '_' + str(itr) + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
				with open(summary, 'w+') as f:
					f.write('n,v,nmi,avg,mod,nmi\n')
					for index, n in enumerate(np.arange(0.1, 1.0, 0.1)):
						n = "%.3f" % n

						o = c + '_' + str(itr) + '_' + str(v) + '_' + str(r).replace('.', '') + '_' + n.replace('.', '')

						levels = str(m)
						config_file = dnet + o + levels + '.conf'
						conf = json.load(open(config_file))

						timing_file = dnet + o + str(m) + '.timing'
						timing = json.load(open(timing_file))
						timing_coarsening = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])

						levels = levels.replace('[', '\\[').replace(',', '\\,').replace(' ', '\\ ').replace(']', '\\]')
						filename = dnet + o + levels + '.ncol'
						command = 'python ../../mob_exp/statistic.py -f ' + filename
						proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
						(out, err) = proc.communicate()
						out = out.rstrip().split(' ')
						line = [n, str(conf['vertices']), out[0], out[1]]

						coarsest_file = dnet + o + levels + '.ncol'
						command = 'python ../../mob_exp/lpa.py -f ' + coarsest_file + ' -c'
						print command
						proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
						(out, err) = proc.communicate()
						out = out.strip().split(' ')
						line.append(out[1])
						line.append(out[2])

						f.write(','.join(line) + '\n')
						f.flush()
