#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BNOC (Benchmarking weighted bipartite, k-partite or heterogeneous network with overlapping community structures)
==========================

Copyright (C) 2017 Alan Valejo <alanvalejo@gmail.com> All rights reserved
Copyright (C) 2017 Luzia Romanetto <luziaromanetto@gmail.com> All rights reserved
Copyright (C) 2017 Fabiana Góes <fabii.goes@gmail.com> All rights reserved

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

import models.args as args
import models.helper as helper

from models.timing import Timing
from decimal import Decimal

__maintainer__ = 'Alan Valejo'
__email__ = 'alanvalejo@gmail.com, luziaromanetto@gmail.com'
__author__ = 'Alan Valejo, Luzia Romanetto, Fabiana Góes'
__credits__ = ['Alan Valejo', 'Luzia Romanetto', 'Fabiana Góes', 'Maria Cristina Ferreira de Oliveira', 'Alneu de Andrade Lopes']
__homepage__ = 'https://github.com/alanvalejo/bnoc'
__license__ = 'GNU.GPL.v3'
__docformat__ = 'markdown en'
__version__ = '0.2.1'
__date__ = '2018-08-08'

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

            if self.options.p is None or self.options.balanced is True:
                self.generate_balanced_probabilities()

            for p in self.options.p:
                if str(numpy.sum(round(sum(p), 1))) != str(1.0):
                    self.log.warning('Warning: The sum of probabilities p1 must be equal to 1.')
                    sys.exit(1)

            if len(self.options.communities) is None:
                self.options.communities = [1] * len(self.options.vertices)

            if self.options.x is not None and isinstance(self.options.x, int):
                self.options.x = [self.options.x] * self.layers
            if self.options.y is not None and isinstance(self.options.y, int):
                self.options.y = [self.options.y] * self.layers
            if self.options.z is not None and isinstance(self.options.z, int):
                self.options.z = [self.options.z] * self.layers

            if all(isinstance(item, tuple) for item in self.options.schema):
                self.options.schema = [list(elem) for elem in self.options.schema]
            if not all(isinstance(item, list) for item in self.options.schema):
                it = iter(self.options.schema)
                self.options.schema = zip(it, it)

            if self.options.mu is not None and isinstance(self.options.mu, (int, float)):
                self.options.mu = [self.options.mu] * len(self.options.schema)
            if self.options.dispersion is not None and isinstance(self.options.dispersion, (int, float)):
                self.options.dispersion = [self.options.dispersion] * len(self.options.schema)
            if self.options.noise is not None and isinstance(self.options.noise, (int, float)):
                self.options.noise = [self.options.noise] * len(self.options.schema)

            for layer, comm in enumerate(self.options.communities):
                if comm == 0:
                    self.log.warning('The number of communities must be greater than zero.')
                    sys.exit(1)
                if self.options.communities[layer] > self.options.vertices[layer]:
                    self.log.warning('Warning: The number of communities must be less than the number of vertices.')
                    sys.exit(1)

            if self.options.x is not None and self.options.z is not None:
                if self.options.z[layer] > self.options.communities[layer]:
                    self.log.warning('Warning: Number of vertices of overlapping communities must be less than the number of communities in all layers.')
                    sys.exit(1)
                if sum(self.options.x) > 0 and sum(self.options.z) == 0:
                    self.options.z = [2] * len(self.options.x)

    def add_noise(self, matrix, noise):
        """ Insert a noise in adjacent matrix
            Noise or Threshold in (0,1]
        """

        # Removing a fraction of inter-community edges [numpy.random.seed(1)]
        num_samples = numpy.count_nonzero(matrix)
        Z = [False]
        while not any(Z): # while all elements are 'False'
            Z = numpy.random.rand(num_samples) < noise
            # Z = numpy.random.uniform(0.0, 1.0, num_samples) < noise
        Y = matrix[matrix > 0]
        removed_weights = Y[Z]
        Y[Z] = 0
        if self.options.hard:
            matrix[matrix > 0] = Y

        # Adding a fraction of intra-community edges
        num_samples = numpy.count_nonzero(matrix == 0)
        Z = [False]
        while not any(Z): # while all elements are 'False'
            # Z = numpy.random.rand(num_samples) < noise
            Z = numpy.random.uniform(0.0, 1.0, num_samples) < noise
        Y = matrix[matrix == 0]
        _mean = numpy.mean(removed_weights, dtype=numpy.float64)
        # _mean = numpy.median(removed_weights)
        if not self.options.hard:
            removed_weights = [_mean] * len(removed_weights)
        removed_weights = list(removed_weights) + ([0] * (numpy.count_nonzero(Z) - len(removed_weights)))
        Y[Z] = numpy.random.choice(removed_weights, numpy.count_nonzero(Z))
        matrix[matrix == 0] = Y

        return matrix

    def generate_balanced_probabilities(self):
        """ Generates a list of probabilities for each class when the probabilities
        are not given by the user or the balanced flag is on.
        """

        if self.options.p is None:
            self.options.p = empty_lists = [[] for i in range(self.layers)]
        for layer in range(self.layers):
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
            self.unique_comms[layer] = list(range(self.options.communities[layer]))
            self.cover[layer] = numpy.empty((self.options.communities[layer], 0)).tolist()
            for vertex, comm in enumerate(self.membership[layer]):
                self.cover[layer][comm].append(vertex + self.start_end[layer][0])

    def select_overlapping_vertices(self):
        """ Select x vertices to be member of z communities, as expected by model """

        self.overlap = [[] for i in range(self.layers)]
        if self.options.x is not None and sum(self.options.x) > 0:
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

    def save_text(self, output):

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
            edges, weights = list(zip(*dict_edges.items()))
            graph = igraph.Graph(sum(self.options.vertices), list(edges))
            graph['vertices'] = list(map(str, self.options.vertices))
            graph.es['weight'] = weights
            graph.write(output + '.gml', format='gml')

        # Save arff
        if self.options.save_arff:
            self.log.warning('Arff format still under development.')
            sys.exit(1)

    def save_npy(self, output):

        # Save npy
        if self.options.save_ncol:
            numpy.save(output + '-matrices.npy', self.matrices)

        # Save type
        if self.options.save_type:
            type = []
            for layer, vertices in enumerate(self.options.vertices):
                type.extend([layer] * vertices)
            numpy.save(output + '-type.npy', type)

        # Save overlap
        if self.options.save_overlap:
            numpy.save(output + '-overlap.npy', self.overlap)

        # Save cover
        if self.options.save_cover:
            numpy.save(output + '-cover.npy', self.cover)

        # Save membership
        membership = []
        for l in self.cover:
            cl = igraph.Cover(l)
            membership.extend(cl.membership)
        membership = list(filter(None, membership))
        if self.options.save_membership:
            numpy.save(output + '-membership.npy', self.membership)

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
                d = {
                    'output': self.options.output
                    , 'directory': self.options.directory
                    , 'extension': 'ncol'
                    , 'vertices': self.options.vertices
                    , 'communities': self.options.communities
                    , 'x': self.options.x
                    , 'z': self.options.z
                    , 'p': self.options.p
                    , 'balanced': self.options.balanced
                    , 'd': self.options.dispersion
                    , 'mu': self.options.mu
                    , 'noise': self.options.noise
                    , 'unweighted': self.options.unweighted
                    , 'normalize': self.options.normalize
                    , 'conf': self.options.conf
                    , 'show_timing': self.options.show_timing
                    , 'save_timing_csv': self.options.save_timing_csv
                    , 'save_timing_json': self.options.save_timing_json
                    , 'unique_key': self.options.unique_key, 'edges': 0
                }
                for matrix in self.matrices:
                    d['edges'] += numpy.count_nonzero(matrix)
                json.dump(d, f, indent=4)

            if self.options.output_npy:
                self.save_npy(output)
            if self.options.output_text:
                self.save_text(output)

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
