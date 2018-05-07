import json
import os

c = 'rm'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
r = 0.5
dresult = 'result-levels-edges'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(r).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('e,l\n')
		for m in mset:
			m = [m] * 2
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['edges']), str(m[0])]
			f.write(','.join(line) + '\n')

c = 'hem'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
r = 0.5
dresult = 'result-levels-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(r).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('e,l\n')
		for m in mset:
			m = [m] * 2
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['edges']), str(m[0])]
			f.write(','.join(line) + '\n')

c = 'lem'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
r = 0.5
dresult = 'result-levels-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(r).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('e,l\n')
		for m in mset:
			m = [m] * 2
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['edges']), str(m[0])]
			f.write(','.join(line) + '\n')

c = 'greedy_twohops'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
r = 0.5
dresult = 'result-levels-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(r).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('e,l\n')
		for m in mset:
			m = [m] * 2
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['edges']), str(m[0])]
			f.write(','.join(line) + '\n')

c = 'greedy_seed_twohops'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
r = 0.5
dresult = 'result-levels-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(r).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('e,l\n')
		for m in mset:
			m = [m] * 2
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['edges']), str(m[0])]
			f.write(','.join(line) + '\n')

c = 'greedy_seed_modularity'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
r = 0.5
dresult = 'result-levels-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(r).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('e,l\n')
		for m in mset:
			m = [m] * 2
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['edges']), str(m[0])]
			f.write(','.join(line) + '\n')

c = 'greedy_seed_modularity_group'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
r = 0.5
dresult = 'result-levels-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(r).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('e,l\n')
		for m in mset:
			m = [m] * 2
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['edges']), str(m[0])]
			f.write(','.join(line) + '\n')

c = 'lpa_modularity'
mset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
r = 0.5
dresult = 'result-levels-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(r).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('e,l\n')
		for m in mset:
			m = [m] * 2
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['edges']), str(m[0])]
			f.write(','.join(line) + '\n')
