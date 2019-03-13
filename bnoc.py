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
import numpy
import sys
import csv
import copy
import json
import igraph
import inspect
import os
import math

import models372.args as args
import models372.helper as helper
import models372.helperigraph as helperigraph

from itertools import izip
from models372.timing import Timing

__maintainer__ = 'Alan Valejo and Luzia Romanetto'
__email__ = 'alanvalejo@gmail.com, luziaromanetto@gmail.com'
__author__ = 'Alan Valejo, Luzia Romanetto, Fabiana Góes'
__credits__ = ['Alan Valejo', 'Luzia Romanetto', 'Fabiana Góes', 'Maria Cristina Ferreira de Oliveira', 'Alneu de Andrade Lopes']
__homepage__ = 'https://github.com/alanvalejo/bnoc'
__license__ = 'GNU'
__docformat__ = 'markdown en'
__version__ = '0.1'
__date__ = '2017-10-01'

global max_itr
max_itr = 1000

# BNOC app
class bnoc(object):

	def __init__(self):
		""" Initialize the bnoc app

		For help use:
			> python bnoc.py --help
		"""

		self.timing = Timing(['Snippet', 'Time [m]', 'Time [s]'])
		with self.timing.timeit_context_add('Pre-processing'):
			# Setup parse options command line
			current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
			parser = args.setup_parser(current_path + '/args/bnoc.json')
			self.options = parser.parse_args()
			args.update_json(self.options)
			args.check_output(self.options)
			self.log = helper.initialize_logger(dir='log', output='log')

			if self.options.save_arff and (self.options.x is not None):
				self.log.warning('Warning: Arff format does not allow overlap in the first layer (parameter x). Please use --save_arff=False or supress x parameter.')
				sys.exit(1)

			self.layers = len(self.options.vertices)

			self.start_end = []
			for layer in range(self.layers):
				start = sum(self.options.vertices[0:layer])
				end = sum(self.options.vertices[0:layer + 1]) - 1
				self.start_end.append([start, end])

			for p in self.options.p:
				if str(sum(p)) != str(1.0):
					self.log.warning('Warning: The sum of probabilities p1 must be equal to 1.')
					sys.exit(1)

			if self.options.p is None or self.options.balanced is True:
				self.generate_balanced_probabilities()

			if len(self.options.communities) == None:
				self.options.communities = [1] * len(self.options.vertices)

			for layer, comm in enumerate(self.options.communities):
				if comm == 0:
					self.log.warning('The number of communities must be greater than zero.')
					sys.exit(1)
				if self.options.communities[layer] > self.options.vertices[layer]:
					self.log.warning('Warning: The number of communities must be less than the number of vertices.')
					sys.exit(1)
				if self.options.z[layer] > self.options.communities[layer]:
					self.log.warning('Warning: Number of vertices of overlapping communities must be less than the number of communities in all layers.')
					sys.exit(1)

			if self.options.x is not None and self.options.z is not None:
				if sum(self.options.x) > 0 and sum(self.options.z) == 0:
					self.options.z = [2] * len(self.options.x)

	def add_noise(self, matrix, noise):
		""" Insert a noise in adjacent matrix
			Noise or Threshold in (0,1]
		"""

		# Removing a fraction of inter-community edges [numpy.random.seed(1)]
		num_samples = numpy.count_nonzero(matrix)
		A = [False]
		while not any(A): # while all elements are 'False'
			A = numpy.random.rand(num_samples) < noise
			# A = numpy.random.uniform(0.0, 1.0, num_samples) < noise
		B = matrix[matrix > 0]
		removed_weights = B[A]
		B[A] = 0
		if self.options.hard:
			matrix[matrix > 0] = B

		# Adding a fraction of intra-community edges
		num_samples = numpy.count_nonzero(matrix == 0)
		A = [False]
		while not any(A): # while all elements are 'False'
			# A = numpy.random.rand(num_samples) < noise
			A = numpy.random.uniform(0.0, 1.0, num_samples) < noise
		B = matrix[matrix == 0]
		_mean = numpy.mean(removed_weights, dtype=numpy.float64)
		# _mean = numpy.median(removed_weights)
		if not self.options.hard:
			removed_weights = [_mean] * len(removed_weights)
		removed_weights = list(removed_weights) + ([0] * (numpy.count_nonzero(A) - len(removed_weights)))
		B[A] = numpy.random.choice(removed_weights, numpy.count_nonzero(A))
		matrix[matrix == 0] = B

		return matrix

	def generate_balanced_probabilities(self):
		""" Generates a list of probabilities for each class when the probabilities
		are not given by the user or the balanced flag is on.
		"""

		for layer, p in enumerate(self.options.p):
			avg = float("{0:.2f}".format(1.0 / self.options.communities[layer]))
			self.options.p[layer] = [avg] * self.options.communities[layer]
			self.options.p[layer][-1] = float("{0:.2f}".format(1.0 - sum(self.options.p[layer][:-1])))

	def create_vertices_and_communities(self):
		""" Creates a list that gives the class for each element in the positioning
		order for one type of element
		"""

		self.membership = [[] for i in range(self.layers)]
		for layer in range(self.layers):
			for itr in range(max_itr):
				self.membership[layer] = numpy.random.choice(self.options.communities[layer], size=self.options.vertices[layer], replace=True, p=self.options.p[layer])
				self.membership[layer] = sorted(self.membership[layer])
				unique_row = numpy.unique(self.membership[layer])
				if len(unique_row) == self.options.communities[layer]:
					break
				if itr == max_itr:
					self.log.warning('Warning: Convergence failure, reduce the number of communities or run again.')
					sys.exit(1)

	def create_cover(self):
		""" Creates a list of list that maps from each community to the nodes in it """

		self.unique_comms = [0] * self.layers
		self.cover = [[] for i in range(self.layers)]
		for layer in range(self.layers):
			self.unique_comms[layer] = range(self.options.communities[layer])
			self.cover[layer] = numpy.empty((self.options.communities[layer], 0)).tolist()
			for vertex, comm in enumerate(self.membership[layer]):
				self.cover[layer][comm].append(vertex + self.start_end[layer][0])

	def select_overlapping_vertices(self):
		""" Select x vertices to be member of z communities, as expected by model """

		self.overlap = [[] for i in range(self.layers)]
		if self.options.x is not None or sum(self.options.x) > 0:
			for layer in range(self.layers):
				self.overlap[layer] = numpy.random.choice(range(self.start_end[layer][0], self.start_end[layer][1] + 1), self.options.x[layer], replace=False)
				for vertex in self.overlap[layer]:
					comms = copy.copy(self.unique_comms[layer])
					comms.remove(self.membership[layer][vertex - self.start_end[layer][0]])
					random.shuffle(comms)
					# Update communities
					for comm in comms[:(self.options.z[layer] - 1)]:
						self.cover[layer][comm].append(vertex)

	def create_biadj_matrix(self, l0, l1, dispersion, mu):
		""" Create an unweighted adjacenty matrix with community structure. """

		# Create a empty biparte
		matrix = numpy.zeros((self.options.vertices[l0], self.options.vertices[l1]), dtype=numpy.float64)
		unique_comms = [self.unique_comms[l0], self.unique_comms[l1]]
		_max = unique_comms.index(max(unique_comms, key=len))
		_min = unique_comms.index(min(unique_comms, key=len))
		# Connect all vertices in each module
		multiplier = math.ceil(len(unique_comms[_max]) / float(len(unique_comms[_min])))
		unique_comms[_min] = unique_comms[_min] * int(multiplier)
		unique_comms[_min] = unique_comms[_min][:len(unique_comms[_max])]

		for index in range(len(unique_comms[_max])):
			for u in self.cover[l0][unique_comms[0][index]]:
				for v in self.cover[l1][unique_comms[1][index]]:
					matrix[u - self.start_end[l0][0], v - self.start_end[l1][0]] = 1

		# Make a large negative binomial distribution
		num_samples = numpy.count_nonzero(matrix)
		# prob = dispersion / (dispersion + mu)
		# prob = ((mu + dispersion * mu ** 2) - mu) / (mu + dispersion * mu ** 2)
		# from scipy.stats import nbinom
		# distribution = nbinom.rvs(dispersion, prob, size=num_samples)
		distribution = numpy.random.negative_binomial(dispersion, 1 - mu, num_samples)
		if self.options.normalize:
			distribution = distribution / numpy.linalg.norm(distribution)
		# numpy.set_printoptions(threshold=numpy.nan)
		# print distribution
		matrix[matrix > 0] = distribution

		return matrix

	def build(self):
		""" Runs the application. """

		# Graph construction
		with self.timing.timeit_context_add('Build BNOC'):
			self.create_vertices_and_communities()
			self.create_cover()
			self.select_overlapping_vertices()
			self.matrices = []
			for index, e in enumerate(self.options.schema):
				matrix = self.create_biadj_matrix(e[0], e[1], self.options.dispersion[index], self.options.mu[index])
				if self.options.noise[index] > 0.0:
					matrix = self.add_noise(matrix, self.options.noise[index])
				self.matrices.append(matrix)

		# Save
		with self.timing.timeit_context_add('Save'):
			# Save json inf file
			output = self.options.output
			with open(output + '-inf.json', 'w+') as f:
				d = {}
				d['output'] = self.options.output
				d['directory'] = self.options.directory
				d['extension'] = 'ncol'
				d['vertices'] = self.options.vertices
				d['communities'] = self.options.communities
				d['x'] = self.options.x
				d['z'] = self.options.z
				d['p'] = self.options.p
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
				d['edges'] = 0
				for matrix in self.matrices:
					d['edges'] += numpy.count_nonzero(matrix)
				json.dump(d, f, indent=4)

			# Save type
			if self.options.save_type:
				with open(output + '.type', 'w+') as f:
					for layer in range(self.layers):
						for i in range(self.options.vertices[layer]):
							f.write(str(layer) + '\n')

			# Save overlap
			if self.options.save_overlap:
				for layer in range(self.layers):
					if len(self.overlap[layer]) > 0:
						with open(output + '.overrow', 'w+') as f:
							writer = csv.writer(f, delimiter=' ')
							writer.writerow(self.overlap[layer])

			# Save cover
			if self.options.save_cover:
				for layer in range(self.layers):
					with open(output + '-layer-' + str(layer) + '.cover', 'w+') as f:
						writer = csv.writer(f, delimiter=' ')
						for values in self.cover[layer]:
							writer.writerow(values)

			# Save membership
			if self.options.save_membership:
				with open(output + '.membership', 'w+') as f:
					writer = csv.writer(f, delimiter=' ')
					for layer in range(self.layers):
						cl = igraph.Cover(self.cover[layer])
						for sublist in cl.membership:
							if sublist:
								writer.writerow(sublist)

			# Save bipartite network
			if self.options.save_ncol or self.options.save_gml or self.options.save_arff:
				edgelist = ''
				dict_edges = dict()
				for key, matrix in enumerate(self.matrices):
					l0 = self.options.schema[key][0]
					l1 = self.options.schema[key][1]
					for i in range(matrix.shape[0]):
						for j in range(matrix.shape[1]):
							if matrix[i, j] != 0:
								u = i + self.start_end[l0][0]
								v = j + self.start_end[l1][0]
								if self.options.unweighted is False:
									weight = numpy.around(matrix[i, j], decimals=3)
								else:
									weight = 1.0
								edgelist += '%s %s %s\n' % (u, v, weight)
								dict_edges[(u, v)] = float(weight)

			# Save ncol
			if self.options.save_ncol:
				with open(output + '.ncol', 'w+') as f:
					f.write(edgelist)

			# Save gml
			if self.options.save_gml:
				edges, weights = izip(*dict_edges.items())
				graph = igraph.Graph(sum(self.options.vertices), list(edges))
				graph['vertices'] = list(map(str, self.options.vertices))
				graph.es['weight'] = weights
				graph.write(output + '.gml', format='gml')

			# Save arff
			if self.options.save_arff:
				self.log.warning('Arff format still under development.')
				sys.exit(1)

		if self.options.show_timing:
			self.timing.print_tabular()
		if self.options.save_timing_csv:
			self.timing.save_csv(output + '-timing.csv')
		if self.options.save_timing_json:
			self.timing.save_json(output + '-timing.csv')

def main():
	""" Main entry point for the application when run from the command line. """
	return bnoc().build()


if __name__ == "__main__":
	sys.exit(main())
