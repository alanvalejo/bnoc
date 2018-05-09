import json
import numpy as np
import subprocess
import os

c = 'lpa'
rset = [0.5]
mset = [1]
d = 'network/'
v = 1000
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

for m in mset:
	m = [m] * 2
	for r in rset:
		summary = dout + 'summary_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('n,v,nmi,avg,mod\n')
			for index, n in enumerate(np.arange(0.1, 0.5, 0.01)):
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
				f.write(','.join(line) + '\n')
				f.flush()
