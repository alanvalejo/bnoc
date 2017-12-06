#!/usr/bin/env python
# -*- coding: utf-8 -*-

import igraph
import argparse
import sys
import os
import numpy
import random

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

def remap(x, oMin, oMax, nMin, nMax):

	# Range check
	if oMin == oMax: return None
	if nMin == nMax: return None

	# Check reversed input range
	reverseInput = False
	oldMin = min(oMin, oMax)
	oldMax = max(oMin, oMax)
	if not oldMin == oMin:
		reverseInput = True

	# Check reversed output range
	reverseOutput = False
	newMin = min(nMin, nMax)
	newMax = max(nMin, nMax)
	if not newMin == nMin:
		reverseOutput = True

	portion = (x - oldMin) * (newMax - newMin) / (oldMax - oldMin)
	if reverseInput:
		portion = (oldMax - x) * (newMax - newMin) / (oldMax - oldMin)

	result = portion + newMin
	if reverseOutput:
		result = newMax - portion

	return result

def plot_homogeneous(graph, save, output, membership, bbox, comms, overlapping):

	graph.vs['color'] = 'black'
	colors = []
	vertex_color = ['#FFFFFF'] * graph.vcount()
	for i in range(0, comms + 1):
		colors.append('%06X' % random.randint(0, 0xFFFFFF))
		colors = ['809743', '406599', 'DF90D3']
	for vertex in graph.vs():
		membership = graph.vs[vertex.index]['membership']
		if len(membership) == 1:
			index = membership.pop()
			vertex_color[vertex.index] = str('#') + colors[index]
		else:
			vertex_color[vertex.index] = '#FF0000' # overlapping vertices
	graph.vs['color'] = vertex_color

	bondary_edges = []
	edge_color = []
	for edge in graph.es():
		if vertex_color[edge.tuple[0]] != vertex_color[edge.tuple[1]]:
			bondary_edges.append(edge)
			edge_color.append('gray')
		else:
			edge_color.append('black')
	gcopy = graph.copy()
	gcopy.delete_edges(bondary_edges)
	layout = gcopy.layout('kk')

	visual_style = {}

	old_min = min(graph.es['weight'])
	old_max = max(graph.es['weight'])
	new_min = 0.01
	new_max = 7
	edge_width = []
	for w in graph.es['weight']:
		edge_width.append(remap(w, old_min, old_max, new_min, new_max))

	graph.vs['vertex_size'] = 12
	graph.vs[overlapping]['vertex_size'] = 15
	graph.vs['vertex_shape'] = graph['vertices'][0] * ['circle'] + graph['vertices'][1] * ['triangle-up'] # rectangle, circle, hidden, triangle-up, triangle-down
	graph.vs[overlapping]['vertex_shape'] = 'rectangle'

	visual_style['edge_label'] = None
	visual_style['edge_color'] = edge_color
	visual_style['edge_width'] = edge_width

	visual_style['vertex_shape'] = graph.vs['vertex_shape']
	visual_style['vertex_size'] = graph.vs['vertex_size']
	visual_style['vertex_label'] = None
	visual_style['vertex_label_color'] = 'white'
	visual_style['vertex_color'] = graph.vs['color']
	visual_style['vertex_label_dist'] = -1
	visual_style['vertex_frame_color'] = 'white'
	visual_style['vertex_frame_width'] = 1

	visual_style['layout'] = layout
	visual_style['bbox'] = bbox
	visual_style['margin'] = 8

	if save is True:
		igraph.plot(graph, output, **visual_style)
	else:
		igraph.plot(graph, **visual_style)

def plot_communities(graph, save, output, membership, bbox, comms, overlapping):

	graph.vs['color'] = 'black'
	colors = []
	vertex_color = ['#FFFFFF'] * graph.vcount()
	for i in range(0, comms + 1):
		colors.append('%06X' % random.randint(0, 0xFFFFFF))
		colors = ['809743', '406599', 'DF90D3']
	for vertex in graph.vs():
		membership = graph.vs[vertex.index]['membership']
		if len(membership) == 1:
			index = membership.pop()
			vertex_color[vertex.index] = str('#') + colors[index]
		else:
			vertex_color[vertex.index] = '#FF0000' # overlapping vertices
	graph.vs['color'] = vertex_color

	visual_style = {}

	old_min = min(graph.es['weight'])
	old_max = max(graph.es['weight'])
	new_min = 0.01
	new_max = 7
	edge_width = []
	for w in graph.es['weight']:
		edge_width.append(remap(w, old_min, old_max, new_min, new_max))

	graph.vs['vertex_size'] = 12
	graph.vs[overlapping]['vertex_size'] = 15
	graph.vs['vertex_shape'] = graph['vertices'][0] * ['circle'] + graph['vertices'][1] * ['circle'] # rectangle, circle, hidden, triangle-up, triangle-down
	graph.vs[overlapping]['vertex_shape'] = 'rectangle'

	visual_style['edge_label'] = None
	visual_style['edge_color'] = 'black'
	visual_style['edge_width'] = edge_width

	visual_style['vertex_shape'] = graph.vs['vertex_shape']
	visual_style['vertex_size'] = graph.vs['vertex_size']
	visual_style['vertex_label'] = None
	visual_style['vertex_label_color'] = 'white'
	visual_style['vertex_color'] = graph.vs['color']
	visual_style['vertex_label_dist'] = -1
	visual_style['vertex_frame_color'] = 'white'
	visual_style['vertex_frame_width'] = 1

	visual_style['layout'] = graph.layout('bipartite')
	visual_style['bbox'] = bbox
	visual_style['margin'] = 8

	if save is True:
		igraph.plot(graph, output, **visual_style)
	else:
		igraph.plot(graph, **visual_style)

def plot_graph(graph, save, output, bbox):

	visual_style = {}

	old_min = min(graph.es['weight'])
	old_max = max(graph.es['weight'])
	new_min = 0.1
	new_max = 7
	edge_width = []
	for w in graph.es['weight']:
		edge_width.append(remap(w, old_min, old_max, new_min, new_max))

	vertex_size = 10

	visual_style['edge_label'] = None
	visual_style['edge_color'] = 'black'
	visual_style['edge_width'] = edge_width

	visual_style['vertex_shape'] = graph['vertices'][0] * ['circle'] + graph['vertices'][1] * ['triangle-up']
	visual_style['vertex_size'] = vertex_size
	visual_style['vertex_label'] = None
	visual_style['vertex_label_color'] = 'white'
	visual_style['vertex_color'] = 'black'
	visual_style['vertex_label_dist'] = -1
	visual_style['vertex_frame_color'] = 'white'
	visual_style['vertex_frame_width'] = 1

	visual_style['layout'] = graph.layout('bipartite')
	visual_style['bbox'] = bbox
	visual_style['margin'] = 5

	if save is True:
		igraph.plot(graph, output, **visual_style)
	else:
		igraph.plot(graph, **visual_style)

if __name__ == '__main__':

	# Parse options command line
	parser = argparse.ArgumentParser()
	usage = 'usage: python %prog [options] args ...'
	parser.add_argument('-f', '--filename', action='store', dest='filename', type=str, help='[Bipartite Graph]')
	parser.add_argument('-d', '--directory', action='store', dest=None, type=str, help='[Output directory]')
	parser.add_argument('-o', '--output', action='store', dest=None, type=str, help='[Output filename]')
	parser.add_argument('-v', '--vertices', dest='vertices', nargs='+', type=int, help='[Number of vertices for each layer (default: None)]')
	parser.add_argument('-m', '--membership', action='store_true', dest='membership', default=False, help='[Membership flas]')
	parser.add_argument('-b', '--bbox', dest='bbox', action='store', nargs='+', default=[1000, 300], help='[The bounding box of the plot]')
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
	if options.membership:
		comms = 0
		for vertex in graph.vs(): vertex['membership'] = set()
		with open(os.path.splitext(options.filename)[0] + '.coverrow', 'r') as f:
			for comm, line in enumerate(f):
				for vertex in map(int, line.strip().split(' ')):
					graph.vs[int(vertex)]['membership'].add(comm)
				comms = comms + 1
		with open(os.path.splitext(options.filename)[0] + '.covercol', 'r') as f:
			for comm, line in enumerate(f):
				for vertex in map(int, line.strip().split(' ')):
					graph.vs[int(vertex)]['membership'].add(comm)
		overlapping = []
		for vertex in graph.vs():
			if len(vertex['membership']) > 1:
				overlapping.append(vertex.index)
		plot_communities(graph, options.save, options.output, graph.vs['membership'], options.bbox, comms, overlapping)
	else:
		plot_graph(graph, options.save, options.output, options.bbox)