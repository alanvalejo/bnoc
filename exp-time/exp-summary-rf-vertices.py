import json
import os

c = 'rm'
m = [1] * 2
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-rf-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(m[0]).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('v,rf\n')
		for r in rset:
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['vertices']), str(r)]
			f.write(','.join(line) + '\n')

c = 'hem'
m = [1] * 2
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-rf-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(m[0]).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('v,rf\n')
		for r in rset:
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['vertices']), str(r)]
			f.write(','.join(line) + '\n')

c = 'lem'
m = [1] * 2
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-rf-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(m[0]).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('v,rf\n')
		for r in rset:
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['vertices']), str(r)]
			f.write(','.join(line) + '\n')

c = 'greedy_twohops'
m = [1] * 2
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-rf-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(m[0]).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('v,rf\n')
		for r in rset:
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['vertices']), str(r)]
			f.write(','.join(line) + '\n')

c = 'greedy_seed_twohops'
m = [1] * 2
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-rf-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(m[0]).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('v,rf\n')
		for r in rset:
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['vertices']), str(r)]
			f.write(','.join(line) + '\n')

c = 'greedy_seed_modularity'
m = [1] * 2
rset = [0.1, 0.2, 0.3, 0.4, 0.5]
dresult = 'result-rf-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(m[0]).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('v,rf\n')
		for r in rset:
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['vertices']), str(r)]
			f.write(','.join(line) + '\n')

c = 'greedy_seed_modularity_group'
m = [1] * 2
rset = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
dresult = 'result-rf-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(m[0]).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('v,rf\n')
		for r in rset:
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['vertices']), str(r)]
			f.write(','.join(line) + '\n')

c = 'lpa_modularity'
m = [1] * 2
rset = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
dresult = 'result-rf-vertices'
dnet = 'network/'
if not os.path.exists(dresult):
	os.makedirs(dresult)

for index, v in enumerate([10000, 50000, 100000]):
	summary = dresult + '/summary_levels_vertices_' + c + '_' + str(m[0]).replace('.', '') + '_' + str(v) + '.csv'
	with open(summary, 'w+') as f:
		f.write('v,rf\n')
		for r in rset:
			o = c + '_' + str(v) + '_' + str(r).replace('.', '') + str(m)
			config_file = dnet + o + '.conf'
			conf = json.load(open(config_file))
			timing_file = dnet + '/' + o + '.timing'
			timing = json.load(open(timing_file))
			timing = float(timing['Coarsening'][0] * 60) + float(timing['Coarsening'][1])
			line = [str(conf['vertices']), str(r)]
			f.write(','.join(line) + '\n')
