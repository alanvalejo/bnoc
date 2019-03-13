#!/usr/bin/env python
# -*- coding: utf-8 -*-

import igraph
import args
import sys
import os
import numpy
import random
import helper
import helperigraph
import matplotlib.pyplot as plt

from itertools import izip

if __name__ == '__main__':

	# Setup parse options command line
	parser = args.setup_parser('args/plot-bipartite-matrix.json')
	options = parser.parse_args()
	args.update_json(options)
	args.check_output(options)

	# Check required args
	if options.input is None:
		parser.error('required -f [input] arg.')
	if options.vertices is None:
		parser.error('required -v [number of vertices for each layer] arg.')

	# Create bipartite graph
	graph = helperigraph.load(options.input, options.vertices)

	# Plot
	A = helperigraph.biajcent_matrix(graph)
	if options.weighted is False:
		A[A > 0] = 1
	if options.weighted:
		weight = []
		old_min = min(graph.es['weight'])
		old_max = max(graph.es['weight'])
		new_min = 1
		new_max = 10
		for edge in graph.es():
			w = edge['weight']
			weight.append(helper.remap(w, old_min, old_max, new_min, new_max))
		A[A > 0] = weight

	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')
	plt.rc('font', serif='Times')
	axes = plt.gca()
	axes.spines['right'].set_visible(False)
	axes.spines['left'].set_visible(False)
	axes.spines['top'].set_visible(False)
	axes.spines['bottom'].set_visible(False)
	axes.tick_params(axis='y', which='both', length=5, labelsize=18)
	axes.tick_params(axis='x', which='both', length=5, labelsize=18)

	plt.imshow(A, cmap='Greys', interpolation='nearest')
	plt.gca().invert_yaxis()
	if options.weighted and options.colorbar:
		cbar = plt.colorbar()
		cbar.set_ticks([new_min, new_max/2, new_max])
		cbar.set_ticklabels([str(min(graph.es['weight'])), str(max(graph.es['weight'])/2), str(max(graph.es['weight']))])
		cbar.ax.tick_params(labelsize=15)
	if options.save_pdf:
		plt.savefig(options.output + '.pdf', dpi=100, bbox_inches='tight', transparent=False, pad_inches=0)
	if options.save_png:
		plt.savefig(options.output + '.png', dpi=100, bbox_inches='tight', transparent=False, pad_inches=0)
	if options.show:
		plt.show()
