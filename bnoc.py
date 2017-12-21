#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BNOC (Benchmarking weighted bipartite network with overlapping community structures)
==========================

Copyright (C) 2017 Alan Valejo <alanvalejo@gmail.com> All rights reserved
Copyright (C) 2017 Fabiana Góes <fabii.goes@gmail.com> All rights reserved

BNOC is a realistic benchmark for weighted bipartite overlapping community
detection, that accounts for the heterogeneity of community size, noise and
overlapping structure. Detecting communities on this class of graphs is
a challenging task, as shown by applying well known community detection
algorithms.

This file is part of BNOC.

BNOC is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BNOC is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BNOC. If not, see <http://www.gnu.org/licenses/>.
"""

import random
import argparse
import numpy
import os
import sys
import csv
import copy
import logging
import json
import time

from timing import Timing
from datetime import datetime

__maintainer__ = 'Alan Valejo'
__author__ = 'Alan Valejo, Fabiana Góes'
__email__ = 'alanvalejo@gmail.com, fabii.goes@gmail.com'
__credits__ = ['Alan Valejo', 'Fabiana Góes', 'Maria Cristina Ferreira de Oliveira', 'Alneu de Andrade Lopes']
__homepage__ = 'https://github.com/alanvalejo/bnoc'
__license__ = 'GNU'
__docformat__ = 'markdown en'
__version__ = '0.1'
__date__ = '2017-10-01'

global max_itr
max_itr = 1000

def make_bipartite(vertices, communities, x, y, z, p1, p2, balanced, dispersion, mu, normalize, log):
	""" Create a unweighted bipartite network with community structure.

	Args:
		vertices (array<int>): Number of vertices in each layer
		x (int): Number of vertices from V1 that participate of overlaps
		y (int): Number of vertices from V2 that participate of overlaps
		z (int): Number of overlapping communities
		communities (int): Number of communities
		dispersion (double): Dispersion of gamma mixing distribution
		mu (double): Controls the range of weights, see Details [1].
		balanced (bool): Balancing flag
		p1 (array<float>): Probability of vertices in each community for layer 1
		p2 (array<float>): Probability of vertices in each community for layer 2
	Details:
		[1] This is an alternative parametrization (often used in ecology) is by the mean mu
			(see above), and size, the dispersion parameter, where prob = size / (size + mu).
			The variance is mu + mu ^ 2 / size in this parametrization.
	Return:
		A bipartite network, referene partition and overlapping vertices
	Example:
		> network = make_bipartite(40, 60, 10, 3, 5, 0.1, false, [0.1,0.8,0.2,0.2])
	"""

	# Distributions of vertices in communities
	if balanced or (p1 is None):
		average = float("{0:.20f}".format(1.0 / communities))
		p1 = communities * [average]
		p2 = communities * [average]
	for itr in range(max_itr + 1):
		membership_row = numpy.random.choice(communities, size=vertices[0], replace=True, p=p1)
		membership_row = sorted(membership_row)
		unique_row = numpy.unique(membership_row)
		if len(unique_row) == communities: break
		if itr == max_itr:
			log.warning('Warning: Convergence failure, reduce the number of communities or run again.')
			sys.exit(1)
	for itr in range(max_itr + 1):
		membership_col = numpy.random.choice(communities, size=vertices[1], replace=True, p=p2)
		membership_col = sorted(membership_col)
		unique_col = numpy.unique(membership_col)
		if len(unique_col) == communities: break
		if itr == max_itr:
			log.warning('Warning: Convergence failure, reduce the number of communities or run again.')
			sys.exit(1)

	# Create a cover
	cover_row = numpy.empty((communities, 0)).tolist()
	for vertex, comm in enumerate(membership_row):
		cover_row[comm].append(vertex)
	cover_col = numpy.empty((communities, 0)).tolist()
	for vertex, comm in enumerate(membership_col):
		cover_col[comm].append(vertices[0] + vertex)

	unique_comms = range(communities)

	# Select overlapping vertices
	if x is not None:
		overlap_row = numpy.random.choice(range(vertices[0]), x, replace=False)
		for vertex in overlap_row:
			comms = copy.copy(unique_comms)
			comms.remove(membership_row[vertex])
			random.shuffle(comms)
			# Update communities
			for comm in comms[:(z - 1)]:
				cover_row[comm].append(vertex)
	if y is not None:
		overlap_col = numpy.random.choice(range(vertices[0], (vertices[0] + vertices[1])), y, replace=False)
		for vertex in overlap_col:
			comms = copy.copy(unique_comms)
			comms.remove(membership_col[vertex - vertices[0]])
			random.shuffle(comms)
			# Update communities
			for comm in comms[:(z - 1)]:
				cover_col[comm].append(vertex)

	# Create a empty biparte
	matrix = numpy.zeros((vertices[0], vertices[1]), dtype=numpy.float64)

	# Connect all vertices in each module
	for comm in unique_comms:
		for u in cover_row[comm]:
			for v in cover_col[comm]:
				matrix[u, v - vertices[0]] = 1

	# Make a large negative binomial distribution
	num_samples = numpy.count_nonzero(matrix)
	# prob = dispersion / (dispersion + mu)
	# prob = ((mu + dispersion * mu ** 2) - mu) / (mu + dispersion * mu ** 2)
	# from scipy.stats import nbinom
	# distribution = nbinom.rvs(dispersion, prob, size=num_samples)
	distribution = numpy.random.negative_binomial(dispersion, 1 - mu, num_samples)
	if normalize:
		distribution = distribution / numpy.linalg.norm(distribution)
	matrix[matrix > 0] = distribution
	model = bipartite(matrix=matrix, cover_row=cover_row, cover_col=cover_col, overlap_row=overlap_row, overlap_col=overlap_col)

	return model

def add_noise(bipartite, noise):
	""" Insert a noise in adjacent matrix
		Noise or Threshold in (0,1]

	Args:
		bipartite (double matrix): Adjacent matrix
		noise (double): Noise
	Return:
		Adjacent matrix with a noise
	Example:
		> network = noise(network, 0.3)
	"""

	# Removing a fraction of inter-community edges [numpy.random.seed(1)]
	num_samples = numpy.count_nonzero(bipartite)
	A = [False]
	while not any(A): # while all elements are 'False'
		A = numpy.random.rand(num_samples) < noise
	B = bipartite[bipartite > 0]
	removed_weights = B[A]
	B[A] = 0
	bipartite[bipartite > 0] = B

	# Adding a fraction of intra-community edges
	num_samples = numpy.count_nonzero(bipartite == 0)
	A = [False]
	while not any(A): # while all elements are 'False'
		A = numpy.random.rand(num_samples) < noise
	B = bipartite[bipartite == 0]
	B[A] = numpy.random.choice(removed_weights, numpy.count_nonzero(A))
	bipartite[bipartite == 0] = B

	return bipartite

# Bipartite model
class bipartite:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

# BNOC app
class bnoc(object):

	def __init__(self):
		""" Initialize the bnoc app

		For help use:
			> python bnoc.py --help
		"""

		description = 'BNOC (Benchmarking weighted bipartite network with overlapping community structures).'
		self.parser = argparse.ArgumentParser(description=description, formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=150))
		self.parser._action_groups.pop()

		self.optional = self.parser.add_argument_group('optional arguments')
		self.optional.add_argument('-v', '--vertices', dest='vertices', action='store', default=[10, 10], nargs='+', type=int, metavar='int', help='number of vertices for each layer (default: %(default)s)')
		self.optional.add_argument('-dir', '--directory', dest='directory', action='store', type=str, metavar='DIR', default=None, help='directory of FILE if it is not current directory')
		self.optional.add_argument('-o', '--output', dest='output', action='store', type=str, metavar='FILE', default=None, help='name of the %(metavar)s to be save')
		self.optional.add_argument('-d', '--dispersion', dest='dispersion', action='store', default=0.1, type=float, metavar='float', help='dispersion of gamma mixing distribution (default: %(default)s)')
		self.optional.add_argument('-m', '--mu', dest='mu', action='store', default=4, type=float, metavar='float', help='dispersion or range of wieght values (default: %(default)s)')
		self.optional.add_argument('-c', '--communities', dest='communities', action='store', default=2, type=int, metavar='int', help='number of communities (default: %(default)s)')
		self.optional.add_argument('-n', '--noise', dest='noise', action='store', default=0.0, type=float, metavar='float', help='noise (default: %(default)s)')
		self.optional.add_argument('-x', '--x', dest='x', action='store', default=0, type=int, metavar='int', help='number of vertices from V1 that participate of overlaping (default: %(default)s)')
		self.optional.add_argument('-y', '--y', dest='y', action='store', default=0, type=int, metavar='int', help='number of vertices from V2 that participate of overlaping (default: %(default)s)')
		self.optional.add_argument('-z', '--z', dest='z', action='store', default=1, type=int, metavar='int', help='number of vertices of overlapping communities (default: %(default)s)')
		self.optional.add_argument('-p1', '--probabilities_1', dest='p1', action='store', default=None, nargs='+', type=float, metavar='float', help='probability of vertices in each community for layer 1')
		self.optional.add_argument('-p2', '--probabilities_2', dest='p2', action='store', default=None, nargs='+', type=float, metavar='float', help='probability of vertices in each community for layer 2')
		self.optional.add_argument('-b', '--balanced', dest='balanced', action='store_true', default=False, help='boolean balancing flag that suppresses -p parameter (default: %(default)s)')
		self.optional.add_argument('-u', '--unweighted', dest='unweighted', action='store_true', default=False, help='Unweighted networks (default: %(default)s)')
		self.optional.add_argument('-no', '--normalize', dest='normalize', action='store_true', default=False, help='Scale input vectors individually to unit norm (vector length) (default: %(default)s)')
		self.optional.add_argument('-cf', '--conf', dest='conf', action='store', type=str, metavar='FILE', default=None, help='name of the %(metavar)s to be loaded')
		self.optional.add_argument('-st', '--show_timing', dest='show_timing', action='store_true', default=False, help='show timing (default: %(default)s)')
		self.optional.add_argument('-stc', '--save_timing_csv', dest='save_timing_csv', action='store_true', default=False, help='save timing in csv (default: %(default)s)')
		self.optional.add_argument('-stj', '--save_timing_json', dest='save_timing_json', action='store_true', default=False, help='save timing in csv (default: %(default)s)')
		self.optional.add_argument('-uk', '--unique_key', dest='unique_key', action='store_true', default=False, help='output date and time as unique_key (default: %(default)s)')

		self.parser._action_groups.append(self.optional)
		self.log = logging.getLogger('BNOC')
		self.timing = Timing(['Snippet', 'Time [m]', 'Time [s]'])

	def run(self):
		""" Runs the application. """

		with self.timing.timeit_context_add('Pre-processing'):
			self.options = self.parser.parse_args()
			level = logging.WARNING
			logging.basicConfig(level=level, format="%(message)s")

			if self.options.conf:
				json_dict = json.load(open(self.options.conf))
				argparse_dict = vars(self.options)
				argparse_dict.update(json_dict)

			if self.options.directory is None:
				self.options.directory = os.path.dirname(os.path.abspath(__file__))
			else:
				if not os.path.exists(self.options.directory): os.makedirs(self.options.directory)
			if not self.options.directory.endswith('/'): self.options.directory += '/'
			if self.options.output is None:
				self.options.output = 'bipartite_network'
			if self.options.unique_key:
				now = datetime.now()
				options.output = options.output + '_' + now.strftime('%Y%m%d%H%M%S%f')

			if (self.options.p1 is None) and (self.options.p2 is not None):
				self.options.p1 = self.options.p2
			elif (self.options.p1 is not None) and (self.options.p2 is None):
				self.options.p2 = self.options.p1

			if self.options.p1 is not None:
				if sum(self.options.p1) != 1:
					self.log.warning('Warning: The sum of probabilities p1 must be equal to 1.')
					sys.exit(1)
				if sum(self.options.p2) != 1:
					self.log.warning('Warning: The sum of probabilities p2 must be equal to 1.')
					sys.exit(1)

			if self.options.communities == 0: self.options.communities = 1
			if self.options.communities > (self.options.vertices[0] + self.options.vertices[1]):
				self.log.warning('Warning: The number of communities must be less than the number of vertices.')
				sys.exit(1)
			if self.options.z > self.options.communities:
				self.log.warning('Warning: Number of vertices of overlapping communities must be less than the number of communities.')
				sys.exit(1)
			if (self.options.x or self.options.y) and (self.options.z is None):
				self.options.z = 2

		# Graph construction
		with self.timing.timeit_context_add('BNOC'):
			# Create a unweighted bipartite network with fully connected communities
			model = make_bipartite(self.options.vertices, self.options.communities, self.options.x, self.options.y, self.options.z, self.options.p1, self.options.p2, self.options.balanced, self.options.dispersion, self.options.mu, self.options.normalize, self.log)
			# Insert noise
			if self.options.noise > 0.0:
				model.matrix = add_noise(model.matrix, self.options.noise)

		# Save
		with self.timing.timeit_context_add('Save'):
			# Save json inf file
			output = self.options.directory + self.options.output
			with open(output + '-inf.json', 'w+') as f:
				d = {}
				d['output'] = self.options.output
				d['directory'] = self.options.directory
				d['extension'] = 'ncol'
				d['edges'] = numpy.count_nonzero(model.matrix)
				d['vertices'] = [self.options.vertices[0], self.options.vertices[1]]
				d['communities'] = self.options.communities
				d['x'] = self.options.x
				d['y'] = self.options.y
				d['z'] = self.options.z
				d['p1'] = self.options.p1
				d['p2'] = self.options.p2
				d['balanced'] = self.options.balanced
				d['d'] = self.options.dispersion
				d['mu'] = self.options.mu
				d['noise'] = self.options.noise
				d['unweighted'] = self.options.unweighted
				d['normalize'] = self.options.normalize
				d['conf'] = self.options.conf
				d['show_timing'] = self.options.show_timing
				d['save_timing_csv'] = self.options.save_timing_csv
				d['save_timing_json'] = self.options.save_timing_json
				d['unique_key'] = self.options.unique_key
				json.dump(d, f, indent=4)

			# Save overlap
			if len(model.overlap_row) > 0:
				with open(output + '.overrow', 'w+') as f:
					writer = csv.writer(f, delimiter=' ')
					writer.writerow(model.overlap_row)
			if len(model.overlap_col) > 0:
				with open(output + '.overcol', 'w+') as f:
					writer = csv.writer(f, delimiter=' ')
					writer.writerow(model.overlap_col)

			# Save cover
			with open(output + '.coverrow', 'w+') as f:
				writer = csv.writer(f, delimiter=' ')
				for values in model.cover_row:
					writer.writerow(values)
			with open(output + '.covercol', 'w+') as f:
				writer = csv.writer(f, delimiter=' ')
				for values in model.cover_col:
					writer.writerow(values)

			# Save bipartite network
			edgelist = ''
			for i in range(self.options.vertices[0]):
				for j in range(self.options.vertices[1]):
					if model.matrix[i, j] != 0:
						u = i
						v = j + self.options.vertices[0]
						if self.options.unweighted is False:
							weight = numpy.around(model.matrix[i, j], decimals=3)
							edgelist += '%s %s %s\n' % (u, v, weight)
						else:
							edgelist += '%s %s\n' % (u, v)

			with open(output + '.ncol', 'w+') as f:
				f.write(edgelist)

		print self.timing.get_seconds(item=1)
		if self.options.show_timing: self.timing.print_tabular()
		if self.options.save_timing_csv: self.timing.save_csv(output + '-timing.csv')
		if self.options.save_timing_json: self.timing.save_json(output + '-timing.csv')

def main():
	""" Main entry point for the application when run from the command line. """
	return bnoc().run()

if __name__ == "__main__":
	sys.exit(main())
