#!/usr/bin/env python
# -*- coding: utf-8 -*-

import igraph
import argparse
import sys
import os
import numpy
import random
import matplotlib.pyplot as plt

from itertools import izip

def load(filename, vertices):
	"""
	Load ncol npartite graph and generate special attributes
	"""

	data = numpy.loadtxt(filename, skiprows=0, dtype='string')
	dict_edges = dict()
	for row in data:
		dict_edges[(int(row[0]), int(row[1]))] = float(row[2])
	edges, weights = izip(*dict_edges.items())
	graph = igraph.Graph(sum(vertices), list(edges)) # edge_attrs={'weight': weights}
	graph.es['weight'] = weights
	graph.vs['weight'] = 1
	types = []
	for i in range(len(vertices)):
		types += [i] * vertices[i]
	graph.vs['type'] = types
	graph['vertices'] = vertices
	# Not allow direct graphs
	if graph.is_directed(): graph.to_undirected(combine_edges=None)

	return graph

if __name__ == '__main__':

	# Parse options command line
	parser = argparse.ArgumentParser()
	usage = 'usage: python %prog [options] args ...'
	parser.add_argument('-f', '--filename', action='store', dest='filename', type=str, help='[Bipartite Graph]')
	parser.add_argument('-d', '--directory', action='store', dest=None, type=str, help='[Output directory]')
	parser.add_argument('-o', '--output', action='store', dest=None, type=str, help='[Output filename]')
	parser.add_argument('-v', '--vertices', dest='vertices', nargs='+', type=int, help='[Number of vertices for each layer (default: None)]')
	parser.add_argument('-b', '--bbox', dest='bbox', action='store', nargs='+', type=int, default=[1000, 300], help='[The bounding box of the plot]')
	parser.add_argument('-w', '--weighted', dest='weighted', help='Weighted matrix', action='store_true', default=False)
	parser.add_argument('-e', '--format', action='store', dest='format', type=str, default='pdf', help='[Bipartite Graph]')
	parser.add_argument('-s', '--save', dest='save', help='Save image', action='store_true', default=False)
	options = parser.parse_args()

	# Read and pre-process
	if options.filename is None:
		parser.error('required -f [filename] arg.')
	if options.vertices is None:
		parser.error('required -v [Number of vertices for each layer] arg.')
	if options.directory is None:
		options.directory = os.path.dirname(os.path.abspath(options.filename)) + '/'
	else:
		if not os.path.exists(options.directory): os.makedirs(options.directory)
	if not options.directory.endswith('/'): options.directory += '/'
	filename, extension = os.path.splitext(os.path.basename(options.filename))
	if options.output is None:
		options.output = options.directory + filename + '.' + options.format
	else:
		options.output = options.directory + options.output + '.' + options.format

	# Create bipartite graph
	graph = load(options.filename, options.vertices)
	for vertex in graph.vs(): vertex['membership'] = set()

	# Plot
	A = graph.get_adjacency()
	A = numpy.array(A.data)
	A = A[:graph['vertices'][0], graph['vertices'][1]:]
	if options.weighted is True:
		A[A > 0] = graph.es['weight']

	plt.imshow(A, cmap='Greys', interpolation='nearest')
	if options.save is True:
		plt.savefig(options.output, bbox_inches='tight')
	else:
		plt.show()
