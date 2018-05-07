import json
import os

c = 'rm'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-vertices-time'
dnet = 'network'

for m in mset:
	m = [m] * 2
	for r in rset:
		if not os.path.exists(dresult):
			os.makedirs(dresult)
		summary = dresult + '/summary_vertices_time_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('v,t\n')
			for index, v in enumerate(range(1000, 10100, 1000)):
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				timing_file = dnet + '/' + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				line = [str(v), str(timing)]
				f.write(','.join(line) + '\n')

c = 'hem'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-vertices-time'
dnet = 'network'

for m in mset:
	m = [m] * 2
	for r in rset:
		if not os.path.exists(dresult):
			os.makedirs(dresult)
		summary = dresult + '/summary_vertices_time_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('v,t\n')
			for index, v in enumerate(range(1000, 10100, 1000)):
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				timing_file = dnet + '/' + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				line = [str(v), str(timing)]
				f.write(','.join(line) + '\n')

c = 'lem'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-vertices-time'
dnet = 'network'

for m in mset:
	m = [m] * 2
	for r in rset:
		if not os.path.exists(dresult):
			os.makedirs(dresult)
		summary = dresult + '/summary_vertices_time_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('v,t\n')
			for index, v in enumerate(range(1000, 10100, 1000)):
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				timing_file = dnet + '/' + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				line = [str(v), str(timing)]
				f.write(','.join(line) + '\n')

c = 'greedy_twohops'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-vertices-time'
dnet = 'network'

for m in mset:
	m = [m] * 2
	for r in rset:
		if not os.path.exists(dresult):
			os.makedirs(dresult)
		summary = dresult + '/summary_vertices_time_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('v,t\n')
			for index, v in enumerate(range(1000, 10100, 1000)):
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				timing_file = dnet + '/' + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				line = [str(v), str(timing)]
				f.write(','.join(line) + '\n')

c = 'greedy_seed_twohops'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-vertices-time'
dnet = 'network'

for m in mset:
	m = [m] * 2
	for r in rset:
		if not os.path.exists(dresult):
			os.makedirs(dresult)
		summary = dresult + '/summary_vertices_time_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('v,t\n')
			for index, v in enumerate(range(1000, 10100, 1000)):
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				timing_file = dnet + '/' + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				line = [str(v), str(timing)]
				f.write(','.join(line) + '\n')

c = 'greedy_seed_modularity'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-vertices-time'
dnet = 'network'

for m in mset:
	m = [m] * 2
	for r in rset:
		if not os.path.exists(dresult):
			os.makedirs(dresult)
		summary = dresult + '/summary_vertices_time_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('v,t\n')
			for index, v in enumerate(range(1000, 10100, 1000)):
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				timing_file = dnet + '/' + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				line = [str(v), str(timing)]
				f.write(','.join(line) + '\n')

c = 'greedy_seed_modularity_group'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rset = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
dresult = 'result-vertices-time'
dnet = 'network'

for m in mset:
	m = [m] * 2
	for r in rset:
		if not os.path.exists(dresult):
			os.makedirs(dresult)
		summary = dresult + '/summary_vertices_time_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('v,t\n')
			for index, v in enumerate(range(1000, 10100, 1000)):
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				timing_file = dnet + '/' + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				line = [str(v), str(timing)]
				f.write(','.join(line) + '\n')

c = 'lpa_modularity'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rset = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
dresult = 'result-vertices-time'
dnet = 'network'

for m in mset:
	m = [m] * 2
	for r in rset:
		if not os.path.exists(dresult):
			os.makedirs(dresult)
		summary = dresult + '/summary_vertices_time_' + c + '_' + str(m[0]) + '_' + str(r).replace('.', '') + '.csv'
		with open(summary, 'w+') as f:
			f.write('v,t\n')
			for index, v in enumerate(range(1000, 10100, 1000)):
				o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
				timing_file = dnet + '/' + o + '.timing'
				timing = json.load(open(timing_file))
				timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
				line = [str(v), str(timing)]
				f.write(','.join(line) + '\n')
